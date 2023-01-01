import socket, napster_msg
from dataclasses import dataclass, field
# from napster_db import DBNapsterConnector
from napster_key_manager import NapsterKeyManager


@dataclass
class P2PServer:
    """P2P server implementing the Napster protocol"""
    ip: str
    port: int
    key_manager: NapsterKeyManager = field(default_factory=lambda: NapsterKeyManager())

    def __recvall(self, sock: socket, length: int) -> bytes:
        """This private method receives as much bytes as the length parameter indicates

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

    def save_peer_content(self, data: list[str]):
        pass

    def __respond_request(self, connection: socket):
        recv_msg = napster_msg.NapsterMsg()
        recv_msg.length = int(connection.recv(4))
        recv_msg.type = int(connection.recv(4), base=16)
        recv_msg.payload = self.__recvall(
                connection, recv_msg.length).decode('utf8').split()
        try:
            assert recv_msg.parse()
        except AssertionError:
            print(f' Message payload is not well-formed, dropping received message:\n{recv_msg}')
            return
        print(f' Received message {recv_msg}')
        if recv_msg.type == 0x0010: #pubkey req
            reply = napster_msg.compose_pub_key_ack(self.key_manager)
            connection.sendall(reply.to_bytes())
            return
        elif recv_msg.type == 0x00C8: #search
            # db_conn = DBNapsterConnector()
            # keyword_list = recv_msg.get_keyword_list()
            # result_list = db_conn.search_content(keyword_list)
            # for result in result_list:
            #     reply = napster_msg.compose_response(result)
            #     connection.sendall(reply.to_bytes())
            print(f' search protocol not implemented, yet')
            return
        elif recv_msg.type == 0x0002: #login protocol
            print(f' login protocol not implemented, yet')
            return
        
    def listen(self):
        """Listens to login and client petitions"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))
        # max length of pending connections is automatically computed
        sock.listen()
        print(f'Listen on {self.ip}, {self.port}')
        while True:
            try:
                connection, sockname = sock.accept()
                print('We have accepted a connection from', sockname)
                print(' Socket name:', connection.getsockname())
                print(' Socket peer:', connection.getpeername())
                # respond client's request
                self.__respond_request(connection)
                connection.close()
            except KeyboardInterrupt:
                if connection:
                    connection.close()
                break
            except ValueError:
                print(' Server: length or type are not integer types')
