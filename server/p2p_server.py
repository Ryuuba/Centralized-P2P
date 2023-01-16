import socket, napster_msg
from dataclasses import dataclass, field
from napster_db import DBNapsterConnector
from napster_key_manager import NapsterKeyManager
from protocol_exception import NotificationException, UnregisteredUserException


@dataclass
class P2PServer:
    """Class that implement the Napster protocol (serve side)

    Attributes:
        ip (str): The IP address to bind the P2P server
        port (str): The port number to listen client's queries

    Raises:
        EOFError: Raised when the client buffer is empty
        UnregisteredUserException: Raised when an unregister user tries to log in
        ValueError: Raised when the payload of a message is not numeric
        NotificationException: Raised when a user tries to notify content without log in
    """    
    ip: str
    port: int
    __accept_notification : bool = False
    __last_user : str = ''
    __listener: socket.socket = field(default_factory=lambda: socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    __key_manager: NapsterKeyManager = field(default_factory=lambda: 
        NapsterKeyManager())
    __db_conn: DBNapsterConnector = field(default_factory=lambda: 
        DBNapsterConnector())

    def __recvall(self, sock: socket, length: int) -> bytes:
        """Receives as much bytes as the length parameter indicates

        Args:
            sock (socket): A socket to receive data to the client
            length (int): The length of the message sent by the client

        Raises:
            EOFError: The buffer must have as much bytes as the message length

        Returns:
            bytes: The message sent by the client
        """
        data = b''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('was expecting %d bytes but only received'
                        ' %d bytes before the socket closed'
                        % (length, len(data)))
            data += more
        return data
        
    def listen(self, max: int = 1):
        """Listens to login and client petitions

        Args:
            max (int, optional): Maximum number of queued connections. Defaults to 1.
        """        
        self.__listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__listener.bind((self.ip, self.port))
        # max length of pending connections is automatically computed
        self.__listener.listen(max)
        print(f'Listen on {self.ip}, {self.port}')

    def accept_connection(self):
        """Handles new connections and received CTRL+C signal to close the server program
        """        
        client_socket = None
        client_address = None
        while True:
            try:
                client_socket, client_address = self.__listener.accept()
                print('Accepted connection from', client_address)
                self.__handle_protocol(client_socket)
            except KeyboardInterrupt:
                print(' Server: program ends by CTRL+C')
                if client_socket:
                    client_socket.close()
                if self.__db_conn:
                    self.__db_conn.close()
                break

    def __handle_protocol(self, client_socket: socket.socket):
        """Handles client requests according to the Napster protocol

        Args:
            client_socket (socket.socket): The socket connecting this server with a client
        """        
        try:
            while True:
                self.__respond_request(client_socket)
        except AssertionError:
            print(f' Message payload is not well-formed')
        except EOFError:
            print(f'handle_request: connection to {client_socket.getsockname()} has closed')
        except Exception as e:
            print(f'Client {client_socket.getsockname()} error {type(e)}: {e}')
        finally:
            self.__accept_notification = False
            self.__last_user = ''
            client_socket.close()

    def __respond_pub_key_req(self, client_socket: socket.socket):
        """Composes a message encapsulating the public RSA key of this server
            client_socket (socket.socket): The socket to send the public RSA key
        """        
        reply = napster_msg.compose_pub_key_ack(self.__key_manager)
        client_socket.sendall(reply.to_bytes())
        
    def __respond_login_req(self, client_socket: socket.socket, 
            recv_msg: napster_msg.NapsterMsg):
        """Composes a message encapsulating the email of a registered user or a dummy email

        Args:
            client_socket (socket.socket): The socket to send the answer to the login request
            recv_msg (napster_msg.NapsterMsg): The client's request (login msg)

        Raises:
            UnregisteredUserException: Raised when the user is not registered in the napster database
        """        
        user_email = self.__db_conn.search_user_email(recv_msg.payload[0], 
                recv_msg.payload[1])
        print(f' Received login request from {recv_msg.payload[0]} with email {user_email}')
        print(f' Login: client implementation is {recv_msg.payload[3]}')
        if user_email:
            self.__db_conn.insert_netw_data(recv_msg.payload[0], 
                    client_socket.getpeername()[0], int(recv_msg.payload[2]))
                        
            reply = napster_msg.compose_login_ack(user_email)
            
            client_socket.sendall(reply.to_bytes())
            self.__accept_notification = True
            self.__last_user = recv_msg.payload[0]
            print("---------------------flag")
            self.__db_conn.delete_peer_content(recv_msg.payload[0])
            print("---------------------final")
        else:
            user_email = 'napster@napster.com'
            reply = napster_msg.compose_login_ack(user_email)
            client_socket.sendall(reply.to_bytes())
            raise UnregisteredUserException(recv_msg.payload[0])

    def __record_client_content(self, client_socket: socket.socket, 
            recv_msg: napster_msg.NapsterMsg):
        self.__db_conn.insert_content(
                nickname=self.__last_user,
                distro=recv_msg.payload[0],
                sha256=recv_msg.payload[1],
                size=int(recv_msg.payload[2]),
                version=recv_msg.payload[3],
                arch=recv_msg.payload[4],
                target=recv_msg.payload[5])
        self.__db_conn.insert_peer_content(
                nickname=self.__last_user,
                sha256=recv_msg.payload[1],
                url=recv_msg.payload[6])

        """Sends the corresponding message to a given request. If the code message is incorrect, then the message is dropped

        Args:
            client_socket (socket): The socket connecting this server with a client
        """
    def __respond_request(self, client_socket: socket.socket):
        """Sends the corresponding message to a given request. If the code message is incorrect, then the message is dropped

        Args:
            client_socket (socket.socket): The socket connecting this server with a client

        Raises:
            EOFError: Raised when the client buffer is empty
            ValueError: Raised when a field in the payload is not numeric
            NotificationException: Raised when a notification message is received before a login request
        """    
        recv_msg = napster_msg.NapsterMsg()
        msg_length = client_socket.recv(4)
        if not msg_length:
            raise EOFError(' The client has closed the socket')
        msg_type = client_socket.recv(4)
        if not msg_type:
            raise EOFError(f' Message kind is missing')
        if not msg_length.decode('utf8').isnumeric():
            raise ValueError(f' Message length is not numeric {msg_length}')
        if not msg_type.decode('utf8').isnumeric():
            raise ValueError(f' Message type is not numeric {msg_length}')
        recv_msg.length = int(msg_length)
        recv_msg.type = int(msg_type, base=16)
        recv_msg.payload = self.__recvall(
                    client_socket, recv_msg.length).decode('utf8').split()
        print(f'Received message\n{recv_msg}')
        assert recv_msg.parse()
        if recv_msg.type == 0x0010: # public key req
            self.__respond_pub_key_req(client_socket)
        elif recv_msg.type == 0x0002: # login
            self.__respond_login_req(client_socket, recv_msg)
        elif recv_msg.type == 0x0064: # notification
            print('Parse notification msg is OK')
            if not self.__accept_notification:
                raise NotificationException(client_socket.getpeername()[0])
            else:
                self.__record_client_content(client_socket, recv_msg)
        elif recv_msg.type == 0x00C8: # TODO implement search
            # db_conn = DBNapsterConnector()
            # keyword_list = recv_msg.get_keyword_list()
            # result_list = db_conn.search_content(keyword_list)
            # for result in result_list:
            #     reply = napster_msg.compose_response(result)
            #     connection.sendall(reply.to_bytes())
            print(f' search protocol not implemented, yet')
            return

