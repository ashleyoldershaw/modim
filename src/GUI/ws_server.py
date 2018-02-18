# http://www.html.it/pag/53419/websocket-server-con-python/
# sudo -H easy_install tornado

import sys
import socket
import time
import os
import argparse
#from threading import Thread
from thread2 import Thread

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"



#from interaction_manager import InteractionManager
import interaction_manager

# Global variables

websocket_server = None     # websocket handler
run = True                  # main_loop run flag
run_thread = None           # thread running the code
code_running = False        # code running
status = "Idle"             # robot status sent to websocket
last_answer = None
return_value = "OK"
reset_answer = False        # Request to stop waiting for answers
conn_client = None          # Connected client
im = None                   # interaction manager
display_ws = None           # display ws object
robot_type = None           # None, pepper, marrtino, ...
robot_initialized = False   # if robot has been initialized



# Settings functions

def init_robot():
    global robot_type, robot_initialized

    if (not robot_initialized): 
        if (robot_type=='pepper'):
            # Connection to robot
            print("Connecting to Pepper robot...")
            try:
                pepper_cmd.robotconnect()
            except RuntimeError:
                print(RED+"Cannot connect to robot"+RESET)
            print("%sConnected to Pepper robot%s" %(GREEN,RESET))

            pepper_cmd.begin()
            robot_initialized = False
        elif (robot_type=='marrtino'):
            print("%sTODO marrtino initialization.%s" %(RED,RESET))
            sys.exit(0)
    


def begin():
    global code_running, im, display_ws
    print "Start interaction"
    code_running = True
    display_ws.cancel_answer()
    display_ws.remove_buttons()
    im = interaction_manager.InteractionManager(display_ws)
    init_robot()    

def end():
    global code_running
    code_running = False
    pepper_cmd.end()

# Basic UI functions

# Export commands, must set global variable return_value
class DisplayWS:

    def __init__(self):
        self.websocket_server = None

    def setws(self, websocket_server):
        self.websocket_server = websocket_server
    
    def websend(self, data):
        if (self.websocket_server == None):
            print('DisplayWS: websocket not connected.')
            return
        try:
            self.websocket_server.write_message(data)
            #print(status)
        except tornado.websocket.WebSocketClosedError:
            print('DisplayWS: websocket connection error.')

    def display_text(self, data):
        global return_value
        print "web send: " + "display_text_"+data
        self.websend("display_text_"+data)
        return_value = "OK"

    def display_image(self, data):
        self.websend("display_image_"+data)


    def display_imagebuttons(self, data): 
        global last_answer, return_value
        for d in data:
            self.websend("display_imagebutton_"+d)
        last_answer = None
        return_value = "OK"

    def display_buttons(self, data): 
        global last_answer, return_value
        for d in data:
            self.websend("display_button_"+d[0]+"_"+d[1])
        last_answer = None
        return_value = "OK"

    def remove_buttons(self): 
        global return_value
        self.websend("remove_buttons")
        return_value = "OK"

    def answer(self):
        global last_answer, return_value, reset_answer
        reset_answer = False
        while (last_answer is None and not reset_answer):
            time.sleep(0.5)
            #print "Answer: ",last_answer
        return_value = last_answer
        return return_value

    def cancel_answer(self):
        global reset_answer
        reset_answer = True

    def ask(self, data):
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
    global run_thread, code_running, display_ws
    display_ws.cancel_answer()
    #display_ws.websend("reload")
    time.sleep(0.5)
    client_return()
    if (killthread and code_running):
        run_thread.terminate()
        print "Run code thread: ",run_thread," terminated."
        code_running = False



# Run the code

def run_code(code):
    global status, return_value, conn_client, im
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
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.settimeout(3)
    try:
        s.bind((TCP_IP,TCP_PORT))
        s.listen(1)
        run=True
    except:
        print RED+"GUI Program Server: bind error"+RESET
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
        except socket.timeout:
            pass
        except:
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
        global websocket_server, display_ws
        websocket_server = self
        print('New websocket connection')
        print websocket_server
        display_ws.setws(websocket_server)
       
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

    def sendJS(self, data):
        try:
            self.write_message(data)
            #print(status)
        except tornado.websocket.WebSocketClosedError:
            print(RED+'Web socket: connection error.'+RESET)




# Main program
  






if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-wsport", type=str, default=9100,
                        help="WS Server port.")
    parser.add_argument("-cmdport", type=int, default=9101,
                        help="Command Server port")
    parser.add_argument("-robot", type=str, default=None,
                        help="Robot type [None, pepper, marrtino]")

    args = parser.parse_args()

    ws_server_port = args.wsport
    cmd_server_port = args.cmdport
    robot_type = args.robot

    if (robot_type=='pepper'):
        try:
            pepper_tools_dir = os.getenv("PEPPER_TOOLS_HOME")
            sys.path.append(pepper_tools_dir+'/cmd_server')
            import pepper_cmd
            from pepper_cmd import *
        except:
            print("%sSet environment_variable PEPPER_TOOLS_HOME to pepper_tools directory.%s" %(RED,RESET))
            sys.exit(0)
    if (robot_type=='marrtino'):
        print("%sTODO: marrtino import...%s" %(RED,RESET))
        sys.exit(0)

    # Run command server
    t = Thread(target=start_cmd_server, args=(cmd_server_port,))
    t.start()

    # Display object
    display_ws = DisplayWS()

    # Run websocket server
    application = tornado.web.Application([
        (r'/websocketserver', MyWebSocketServer),])  
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(ws_server_port)
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


