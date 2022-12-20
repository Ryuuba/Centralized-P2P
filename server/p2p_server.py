import socket
from dataclasses import dataclass
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

    def compose_login_ack(self) -> NapsterMsg:
        reply = NapsterMsg()
        reply.type = 0x0003
        reply.payload.append('nick@mail.com')
        reply.length = len(''.join(reply.payload))
        return reply

    def compose_search_response(self, keywords: str):
        pass

    def save_peer_content(self, data: list[str]):
        pass
    
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
                msg.type = int(connection.recv(4), base=16)
                msg.payload = self.__recvall(
                        connection, msg.length).decode('utf8').split()
                if msg.parse():
                    print(' recv msg:', msg)
                    reply = None
                    if msg.type == 0x0002:   # login msg
                        reply = self.compose_login_ack()
                    elif msg.type == 0x0064: # notification msg
                        self.save_peer_content()
                    elif msg.type == 0x00C8: # search msg
                        reply = self.compose_search_response()
                    if reply is not None:
                        print(f' ACK Response: {reply.to_bytes()}')
                        connection.sendall(reply.to_bytes())
                        print(' Reply sent, socket closed')
                    connection.close()
            except KeyboardInterrupt:
                if connection:
                    connection.close()
                break
            except ValueError:
                print(' Server: length or type are not integer types')
