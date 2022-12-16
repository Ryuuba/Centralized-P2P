import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 49999)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen(1)
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(100)
            print('received {!r}'.format(data))
            if data:
                print('sending data back to the client')
                connection.sendall(bytes('ACK', 'utf-8'))
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()