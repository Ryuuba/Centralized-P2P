#!/usr/bin/env python3

import argparse, socket, content_manager, search, login

def listener():
    pass

if __name__ == '__main__':
    """Reads the options to set the server"""
    parser = argparse.ArgumentParser(description='Centralized P2P server')
    parser.add_argument('-p2pip', metavar='SERVER_IP', type=str, default='localhost', help='P2P server IP (default localhost)')
    parser.add_argument('-p2pp', metavar='SERVER_PORT', type=int, default=6699, 
            help='P2P server TCP port(default 6699)')
    parser.add_argument('-dbip', metavar='DB_IP', type=str, default='localhost', 
            help='Database default IP (default localhost)')
    parser.add_argument('-dbp', metavar='DB_PORT', type=int, default=3306, 
            help='Database default port (default 3306)')
    args = parser.parse_args()
