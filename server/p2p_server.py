import socket, napster_msg
from dataclasses import dataclass, field
from napster_db import DBNapsterConnector
from napster_key_manager import NapsterKeyManager


@dataclass
class P2PServer:
    """P2P server implementing the Napster protocol"""
    ip: str
    port: int
    __listener: socket.socket = field(default_factory=lambda: socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    __key_manager: NapsterKeyManager = field(default_factory=lambda: 
        NapsterKeyManager())
    __db_conn: DBNapsterConnector = field(default_factory=lambda: 
        DBNapsterConnector())

    def save_peer_content(self, data: list[str]):
        pass

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
        """Listens to login and client petitions"""
        self.__listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__listener.bind((self.ip, self.port))
        # max length of pending connections is automatically computed
        self.__listener.listen(max)
        print(f'Listen on {self.ip}, {self.port}')

    def accept_connection(self):
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
            client_socket (socket): The socket connecting this server with a client
        """
        try:
            while True:
                self.__respond_request(client_socket)
        except AssertionError:
            print(f' Message payload is not well-formed')
        except EOFError:
            print(f'handle_request: connection to {client_socket.getsockname()} has closed')
        except Exception as e:
            print(f'Client {client_socket.getsockname()} error: {e}')
        finally:
            client_socket.close()

    def __respond_request(self, client_socket: socket.socket):
        """Sends the corresponding message to a given request. If the code message is incorrect, then the message is dropped

        Args:
            client_socket (socket): The socket connecting this server with a client
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
        print(f' Received message\n{recv_msg}')
        assert recv_msg.parse()
        if recv_msg.type == 0x0010: # public key req
            reply = napster_msg.compose_pub_key_ack(self.__key_manager)
            client_socket.sendall(reply.to_bytes())
            return
        elif recv_msg.type == 0x0002: # login
            db_conn = DBNapsterConnector()
            user_email = db_conn.search_user_email(recv_msg.payload[0], 
                    recv_msg.payload[1])
            print(f' Received login request from {recv_msg.payload[0]} with email {user_email}')
            print(f' Login: client implementation is {recv_msg.payload[3]}')
            if user_email:
                db_conn.insert_netw_data(recv_msg.payload[0], 
                        client_socket.getpeername()[0], int(recv_msg.payload[2]))
                reply = napster_msg.compose_login_ack(user_email)
                client_socket.sendall(reply.to_bytes())
            else:
                user_email = 'napster@napster.com'
                reply = napster_msg.compose_login_ack(user_email)
                client_socket.sendall(reply.to_bytes())
                raise ValueError(f' User {recv_msg.payload[0]} is not registered')
            return
        elif recv_msg.type == 0x00C8: # search
            # db_conn = DBNapsterConnector()
            # keyword_list = recv_msg.get_keyword_list()
            # result_list = db_conn.search_content(keyword_list)
            # for result in result_list:
            #     reply = napster_msg.compose_response(result)
            #     connection.sendall(reply.to_bytes())
            print(f' search protocol not implemented, yet')
            return

