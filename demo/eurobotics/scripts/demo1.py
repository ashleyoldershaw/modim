import sys
import time
import os

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print "Please set MODIM_HOME environment variable to MODIM folder."
    print e
    sys.exit(1)

import ws_client
from ws_client import *

def i1():
    begin()
    im.setProfile(['*', '*', '*', '*'])
    a = im.ask('animal')
    print a
    im.execute(a)
    end()


def i2():
    begin()

    im.setProfile(['*', '*', 'it', '*'])
    im.setPath('../../demo/eurobotics/')

    im.execute('welcome')

    time.sleep(3)

    a = im.ask('color')

    im.execute(a)

    time.sleep(3)

    im.execute('goodbye')

    end()

def itest():
    display_image("dolphin")
    display_text("Ecco la nuova interfaccia MODIM")
    time.sleep(5)
    display_text("Ti piace?")
    a = ask(['Si', 'No'])
    print "Hai risposto: ",a
    if a=='Si':
        display_text("Bene. Mi fa piacere.")
    else:
        display_text("Ooops. Mi dispiace.")
    time.sleep(3)
    display_text("Arrivederci")
    end()


def i4():

    im.setProfile(['*', '*', '*', '*'])
    im.setPath('../../demo/eurobotics/')

    while True:
    
        im.init()

        a = 1
        while (a==0):
            time.sleep(1)
            a = sensorvalue('headtouch') + sensorvalue('lefthandtouch') +  sensorvalue('righthandtouch')

        im.execute("welcome")

        time.sleep(1)

        q = random.choice(['animal','color'])

        a = im.ask(q)

        im.execute(a)

        time.sleep(3)

        im.execute('goodbye')


     
    
if __name__ == "__main__":

    cmdsever_ip = '127.0.0.1'
    cmdserver_port = 9101
    demo_ip = '127.0.0.1'
    demo_port = 8000

    mws = ModimWSClient()
    mws.setCmdServerAddr(cmdsever_ip, cmdserver_port) 
    mws.setDemoServerAddr(demo_ip, demo_port) 
    #mws.setDemoPath('../../demo/eurobotics/')
    mws.run_interaction(i1)

    #run_interaction(i1)

