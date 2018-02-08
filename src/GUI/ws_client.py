#!/usr/bin/env python

import sys
import os
import socket
import importlib
import re
import argparse
import time


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
    csock.send(data)
    time.sleep(0.5)
    rdata = csock.recv(200)
    return rdata
    #print "Reply: ",rdata

def cclose():
    global csock
    csock.close()

    print("Closed connection")


def begin():
    cconnect()

def end():
    cclose()


def display_text(data):
    #TODO transform abstract data to concrete values
    csend("display_text('"+data+"')")    


def display_image(data):
    #TODO transform abstract data to concrete values
    #imgfile = demodir+"/img/"+data+".jpg"
    imgfile = "img/"+data+".jpg"
    csend("display_image('"+imgfile+"')")    


def ask(data):
    csend("display_buttons("+data+")")    
    a = csend("answer()")
    csend("remove_buttons()")    
    return a.rstrip()

def say(data):
    #TODO transform abstract data to concrete values
    csend("say('"+data+"')")    

def sensorvalue(data):
    a = csend("sensor('"+data+"')")
    return float(a.rstrip())

def stand():
    csend("stand()")    


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


