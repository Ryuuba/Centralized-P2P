import socket


def client_program():
    host = socket.gethostname()  # ya que ambos códigos se ejecutan en la misma PC
    port = 5000  # numero de puerto del socket server
    print("Iniciando en "+host+" con puerto "+port)
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # conectar al servidor

    message = input(" -> ")  # Entrada de mensaje para enviar

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # Enviar el mensaje al servidor
        data = client_socket.recv(1024).decode()  # Recibir la respuesta del servidor

        print('Received from server: ' + data)

        message = input(" -> ")

    client_socket.close()  # Cerrar la conexion
