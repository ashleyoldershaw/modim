import sys
import time

sys.path.append('../../src/GUI')
from ws_client import *

#pepper_ip = '192.168.1.134' # ethernet
#pepper_port = 9101
#setServerAddr(pepper_ip, pepper_port)

setServerAddr('127.0.0.1', 9101)

def i1():
    begin()


    im.setProfile(['*', '*', 'it', '*'])
    im.setPath('../../demo/eurobotics/')

    #showurl('demo/eurobotics/index.html')

    #im.executeModality("IMAGE","img/diaglogo.jpg")

    #time.sleep(3)
    # im.init()


    a = im.ask('animal')
    print a

    #asay("You have selected "+a)

    #im.executeModality("TEXT","Hai scelto "+a)

    #time.sleep(3)
    
    im.execute(a)

    time.sleep(5)

    end()


def i2():
    begin()

    im.setProfile(['*', '*', 'it', '*'])
    im.setPath('../../demo/eurobotics/')

    im.execute('welcome')

    time.sleep(5)

    a = im.ask('color')

    im.execute(a)

    time.sleep(5)

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

run_interaction(i2)

