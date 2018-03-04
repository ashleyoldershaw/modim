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
server_port = 9101
csock = None

def setServerAddr(ip, port):
    global server_ip, server_port
    server_ip = ip
    server_port = port

def cconnect():
    global csock,server_ip,server_port
    print ("WS client:: connecting to %s:%d ..." %(server_ip, server_port))
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csock.connect((server_ip,server_port))
    print ("WS client:: connected to %s:%d" %(server_ip, server_port))


def csendfile(program):
    global csock

    BUFFER_SIZE = 200

    f = open(program,'r') 
    data = f.read() 
    f.close()

    print "Sending program...",
    csock.send(data)

    print("done")

    rdata = csock.recv(BUFFER_SIZE)
    print("Reply: %s" %rdata)


def csend_noblock(data):
    global csock
    if csock==None:
        cconnect()
    csock.send(data)


def csend(data):
    global csock
    if csock==None:
        cconnect()
    print ("WS client:: sending data ...")
    csock.send(data)
    print ("WS client:: data sent")

    time.sleep(0.5)

    print ("WS client:: waiting for reply ...")
    try:
        rdata = csock.recv(200)
    except KeyboardInterrupt:
        rdata = "user quit"
    except socket.error:
        rdata = "socket error"
    print "Reply: ",rdata
    return rdata

def cclose():
    global csock
    csock.close()
    print("Closed connection")
    csock = None


code = ""

def run_interaction(interaction):
    global code
    lcode = inspect.getsourcelines(interaction)
    locode = ""
    for l in lcode[0][1:]:
        locode += l
    locode = textwrap.dedent(locode)
    code += locode
    print code
    cconnect()
    csend(code)


def store_interaction(interaction):
    global code
    lcode = inspect.getsourcelines(interaction)    
    for l in lcode[0][0:]:
        code += l
    code += '\n'

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
    #start_client(server_ip,server_port,program)
    


if __name__ == "__main__":
    main()


