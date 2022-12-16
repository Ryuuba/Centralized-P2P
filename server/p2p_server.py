import socket
from dataclasses import dataclass, field

@dataclass
class P2PServer:
    """P2P server implementing the Napster protocol"""
    ip: str
    port: int

    def __recvall(this, sock, length):
        data = b''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('was expecting %d bytes but only received'
                        ' %d bytes before the socket closed'
                        % (length, len(data)))
            data += more
        return data
    
    def listen(this):
        """Listens to login and client petitions"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((this.ip, this.port))
        sock.listen(1)
        print(f'Listen on {this.ip}, {this.port}')
        while True:
            connection = None
            try:
                connection, sockname = sock.accept()
                print('We have accepted a connection from', sockname)
                print(' Socket name:', connection.getsockname())
                print(' Socket peer:', connection.getpeername())
                message = this.__recvall(connection, 16)
                print(' Incoming sixteen-octet message:', repr(message))
                connection.sendall(b'Farewell, client')
                connection.close()
                print(' Reply sent, socket closed')
            except KeyboardInterrupt:
                if connection:
                    connection.close()
                break
