#!/usr/bin/env python

import sys
import os
import socket
import importlib
import re
import argparse
import time
import inspect
import textwrap

server_ip = '127.0.0.1'
server_port = 9100
csock = None


demodir = '../../demo/eurobotics'

def setDemoDir(ddir):
    global demodir
    demodir = ddir

def cconnect():
    global csock,server_ip,server_port
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csock.connect((server_ip,server_port))

def csendfile(program):
    global csock

    BUFFER_SIZE = 200

    f = open(program,'r') 
    data = f.read() 
    f.close()

    print "Sending program...",
    csock.send(data)

    print(" done")

    rdata = csock.recv(BUFFER_SIZE)
    print "Reply: ",rdata


def csend(data):
    global csock
    if csock==None:
        cconnect()
    csock.send(data)
    time.sleep(0.5)
    try:
        rdata = csock.recv(200)
    except KeyboardInterrupt:
        rdata = "user quit"
    return rdata
    print "Reply: ",rdata

def cclose():
    global csock
    csock.close()
    print("Closed connection")
    csock = None


def run_interaction(interaction):
    lcode = inspect.getsourcelines(interaction)
    code = ""
    for l in lcode[0][1:]:
        code += l
    code = textwrap.dedent(code)
    print code
    cconnect()
    csend(code)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--serverip", type=str, default='127.0.0.1',
                        help="Server IP address.")
    parser.add_argument("--serverport", type=int, default=9100,
                        help="Server port")
    parser.add_argument("--program", type=str, default="default.py",
                        help="Program file to send")

    args = parser.parse_args()
    server_ip = args.serverip
    server_port = args.serverport 
    program = args.program

    #Starting application
    start_client(server_ip,server_port,program)
    


if __name__ == "__main__":
    main()


