import socket
from dataclasses import dataclass, field
from napster_msg import NapsterMsg

@dataclass
class P2PServer:
    """P2P server implementing the Napster protocol"""
    ip: str
    port: int

    def __recvall(self, sock: socket, length: int) -> bytes:
        data = b''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('was expecting %d bytes but only received'
                        ' %d bytes before the socket closed'
                        % (length, len(data)))
            data += more
        return data
    
    def listen(self):
        """Listens to login and client petitions"""
        msg = NapsterMsg()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))
        sock.listen(1)
        print(f'Listen on {self.ip}, {self.port}')
        while True:
            connection = None
            try:
                connection, sockname = sock.accept()
                print('We have accepted a connection from', sockname)
                print(' Socket name:', connection.getsockname())
                print(' Socket peer:', connection.getpeername())
                msg.length = int(connection.recv(4))
                msg.type = int(connection.recv(4))
                msg.payload = self.__recvall(
                        connection, msg.length).decode('utf8') 
                print(' message payload:', msg.payload)
                connection.sendall(b'Farewell, client')
                connection.close()
                print(' Reply sent, socket closed')
            except KeyboardInterrupt:
                if connection:
                    connection.close()
                break
