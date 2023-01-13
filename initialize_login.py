import initialize_naming
import socket
import sys

"""
Este módulo se encarga de enviar el mensaje de inicio de sesión al servidor central.
El mensaje se genera usando el móudlo initialize_naming, el cual se envía al servidor
por medio del socket de la aplicación. Se pone al módulo a escuchar la respuesta del
servidor. Si envía un reconocimiento del inicio de sesión, se ha entrado al sistema correctamente
y se termina el programa. En caso de que se mande un error, se le pedirá al usuario ingresar sus datos
de nuevo.
"""
def loginToSystem(sock: socket, server_address: tuple, port):
    connectionAck = False
    while connectionAck == False:
        loginSock = sock
        loginSock.connect(server_address)
        #Server always uses port 49999
        loginInfoMsg = initialize_naming.getUserInfo(49999)
        try:
            loginSock.sendall(bytes(loginInfoMsg, 'utf-8'))
            response = loginSock.recv(50)
        finally:
            #TODO: analyze message similarly to how server does it
            if response.decode('utf-8') == '00190003napster@napster.com':
                connectionAck = False
                #loginSock.close()
                print('No se puedo iniciar sesión. Ingresa tus datos de nuevo')
                loginSock.close()
            else:
                connectionAck = True
    return connectionAck
