import socket


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 36887  #  10,000 a 40,000
    direccionServidor = ('localhost', port)
    print('Iniciando en {} port {}'.format(*direccionServidor))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # Vincular la direccion del host y puerto juntos

    server_socket.listen(1) #configurar cuántos clientes el servidor puede escuchar simultáneamente

    while True:
        conn, direccion_cliente = server_socket.accept()  # aceptamos la nueva conexion
        print("Conectado desde: " + str(direccion_cliente)) 
        # recibir flujo de datos. no aceptará paquetes de datos mayores de 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # si no se reciben datos romper
            break
        print("Mensaje del usuario: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # Enviamos los datos al cliente

    conn.close()  # Cerramos la conexion


if __name__ == '__main__':
    server_program()