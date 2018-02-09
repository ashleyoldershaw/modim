import sys
import time

sys.path.append('../../src/GUI')
from ws_client import *

def interaction():
    begin()

    im.setProfile(['*', '*', 'es', '*'])
    im.setPath('../../demo/eurobotics/')
    a = im.ask('animal')
    print a

    im.executeModality("TEXT","Hai scelto "+a)

    time.sleep(3)
    
    im.execute(a)

    time.sleep(3)



    end()

def i2():
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

run_interaction(interaction)

