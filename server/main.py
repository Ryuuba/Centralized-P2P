#!/usr/bin/env python3

import argparse
from p2p_server import P2PServer

if __name__ == '__main__':
    """Reads the options to set the server"""
    parser = argparse.ArgumentParser(description='Centralized P2P server')
    parser.add_argument('-p2pip', metavar='SERVER_IP', type=str, default='172.30.5.27', help='P2P server IP (default localhost)')
    parser.add_argument('-p2pp', metavar='SERVER_PORT', type=int, default=6699, 
            help='P2P server TCP port(default 6699)')
    parser.add_argument('-dbuser', metavar='DB_USER', type=str, default='root', 
            help='Database user (default root)')
    parser.add_argument('-dbip', metavar='DB_IP', type=str, default='172.30.5.27', 
            help='Database IP (default localhost)')
    parser.add_argument('-dbp', metavar='DB_PORT', type=int, default=3306, 
            help='Database port (default 3306)')
    args = parser.parse_args()
    print(f'{args.p2pip}, {args.p2pp}')
    p2p_server = P2PServer(args.p2pip, args.p2pp)
    p2p_server.listen()
    port = p2p_server.accept_connection()
