# http://www.html.it/pag/53419/websocket-server-con-python/
# sudo -H easy_install tornado

import sys
import socket
import time
#from threading import Thread
from thread2 import Thread

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

sys.path.append('/home/iocchi/src/Pepper/pepper_tools/cmd_server')
import pepper_cmd
from pepper_cmd import *


# Global variables

websocket_server = None     # websocket handler
run = True                  # main_loop run flag
run_thread = None           # thread running the code
server_port = 9000          # web server port
code_running = False        # code running
status = "Idle"             # robot status sent to websocket
last_answer = None
return_value = "OK"
reset_answer = False        # Request to stop waiting for answers
conn_client = None          # Connected client




RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"


# Basic UI functions

def websend(data):
    global websocket_server
    if websocket_server==None:
        print "websocket server not connected"
        return
    try:
        websocket_server.write_message(data)
        #print(status)
    except tornado.websocket.WebSocketClosedError:
        #print('Connection closed.')
        websocket_server = None

def begin():
    global code_running
    print "Start interaction"
    code_running = True
    cancel_answer()
    remove_buttons()
    pepper_cmd.begin()

def end():
    global code_running
    code_running = False
    pepper_cmd.end()

# Export commands, must set global variable return_value
def display_text(data):
    global return_value
    websend("display_text_"+data)
    return_value = "OK"

def display_image(data):
    imgfile = "img/"+data+".jpg"
    websend("display_image_"+imgfile)


def display_imagebuttons(data): 
    global last_answer, return_value
    for d in data:
        websend("display_imagebutton_"+d)
    last_answer = None
    return_value = "OK"

def display_buttons(data): 
    global last_answer, return_value
    for d in data:
        websend("display_button_"+d)
    last_answer = None
    return_value = "OK"

def remove_buttons(): 
    global return_value
    websend("remove_buttons")
    return_value = "OK"

def answer():
    global last_answer, return_value, reset_answer
    reset_answer = False
    while (last_answer is None and not reset_answer):
        time.sleep(0.5)
        #print "Answer: ",last_answer
    return_value = last_answer
    return return_value

def cancel_answer():
    global reset_answer
    reset_answer = True

def ask(data):
    display_buttons(data)    
    a = answer()
    remove_buttons()
    if (a is not None):
        a = a.rstrip()
    return a


def sensorvalue(data):
    global return_value
    val = None
    print "Sensor ",data
    if (data=='headtouch'):
        val = pepper_cmd.headTouch
    elif (data=='frontsonar'):
        val = pepper_cmd.sonarValues[0]
    elif (data=='backsonar'):
        val = pepper_cmd.sonarValues[1]
    print "Sensor value = ",val
    return val


def client_return():
    global conn_client
    if (conn_client is None):
        return
    try:
        conn_client.send("%r\n" %return_value)
    except Exception as e:
        print(RED+"Run code: Connection error"+RESET)
        print e


def ifreset(killthread=False):
    global run_thread, code_running
    cancel_answer()
    websend("reload")
    time.sleep(0.5)
    client_return()
    if (killthread and code_running):
        run_thread.terminate()
        print "Run code thread: ",run_thread," terminated."
        code_running = False
# Run the code

def run_code(code):
    global status, return_value, conn_client
    if (code is None):
        return
    print("=== Start code run ===")
    print("Executing")
    print(code)
    try:
        status = "Executing program"
        exec(code)
    except Exception as e:
        print("CODE EXECUTION ERROR")
        print e
    status = "Idle"
    ifreset()
    print("=== End code run ===")

# TCP command server

def start_cmd_server(TCP_PORT):
    global run, return_value, run_thread, conn_client

    TCP_IP = ''
    BUFFER_SIZE = 20000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((TCP_IP,TCP_PORT))
        s.listen(1)
        run=True
    except:
        print "GUI Program Server: bind error"
        run=False        
    
    while run:
        print "%sGUI Program Server: listening on port %d %s" %(GREEN,TCP_PORT,RESET)
        connected = False
        conn_client = None
        try:
            conn_client, addr = s.accept()
            print "Connection address:", addr
            connected = True
        except KeyboardInterrupt:
            print "User quit."
            run = False
        while connected:
            try:
                data = conn_client.recv(BUFFER_SIZE)
            except:
                print "Cmd server: connection closed."
                break
            if not data: break
            print "Received: ",data

            if (data!='***STOP***'):
                run_thread = Thread(target=run_code, args=(data,))
                run_thread.start()
                print "Thread started: ",run_thread
            #run_code(data)
            #conn.send("%s\n" %return_value)

        if (conn_client is not None):
            conn_client.close()
        print "Cmd server: end connection"
        ifreset(True)




# Websocket server handler

class MyWebSocketServer(tornado.websocket.WebSocketHandler):

    def open(self):
        global websocket_server, run
        websocket_server = self
        print('New websocket connection')
       
    def on_message(self, message):
        global last_answer
        print('Input received:\n%s' % message)
        self.write_message('OK') # reply back to ws client
        # store answer for program client
        last_answer = message
  
    def on_close(self):
        print(RED+'Websocket: connection closed'+RESET)
        ifreset(True)
        websocket_server = None
  
    def on_ping(self, data):
        print('ping received: %s' %(data))
  
    def on_pong(self, data):
        print('pong received: %s' %(data))
  
    def check_origin(self, origin):
        #print("-- Request from %s" %(origin))
        return True







# Main program
  
if __name__ == "__main__":

    ws_server_port = 9000
    cmd_server_port = 9100

    # Run command server
    t = Thread(target=start_cmd_server, args=(cmd_server_port,))
    t.start()

    # Connection to robot
    print "Connecting to Pepper robot..."
    try:
        robotconnect()
    except RuntimeError:
        print(RED+"Cannot connect to robot"+RESET)

    # Run websocket server
    application = tornado.web.Application([
        (r'/websocketserver', MyWebSocketServer),])  
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(server_port)
    print("%sWebsocket server: listening on port %d %s" %(GREEN,ws_server_port,RESET))
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print(" -- Keyboard interrupt --")

    if (not websocket_server is None):
        websocket_server.close()
    print("Web server quit.")
    run = False
    print("Waiting for main loop to quit...")


