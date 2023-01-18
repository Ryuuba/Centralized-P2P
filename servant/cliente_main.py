import argparse
import sys
sys.path.append('./servant')
from initialize import P2PClient
import getpass
import threading
import socket

#=========Tupla de socket==========
puerto = "6699"

I = socket.gethostname()
IP = socket.gethostbyname(I)
direccionCliente = (IP, int(puerto))
direccionServidor = ('172.30.5.27', int(puerto))
#print('Iniciando en {} port {}'.format(*direccionServidor))

#=========Directorio==========
miDirectorio = "/home/" + getpass.getuser() + "/Documentos"+"/Distribuciones"


if __name__ == '__main__':
    print("""====================Desplegandoo Servant===========================""")
    parser = argparse.ArgumentParser(description='Centralized P2P Client')
    parser.add_argument('-p2psock', metavar='CLIENT_SOCKET', type=tuple, default=direccionServidor, help='P2P client SOCKET')
    #parser.add_argument('-p2pp', metavar='CLIENT_PORT', type=int, default=6699, help='P2P client TCP port(default 6699)')
    parser.add_argument('-p2pdir', metavar='CLIENT_DIR', type=str, default= miDirectorio, help='P2P Client Directory (default /*user*/Documentos/Distibuciones)')
    args = parser.parse_args()
    print(f'{args.p2psock},{args.p2pdir}')
    #Hilo para el programa principal
    p2p_client = P2PClient(args.p2psock, args.p2pdir)
    p2p_client.start_connection()
    p2p_client.keyRequest()
    p2p_client.sessionRequests()
    