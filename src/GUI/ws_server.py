# http://www.html.it/pag/53419/websocket-server-con-python/
# sudo -H easy_install tornado

import sys
import socket
import time
import os
import argparse
import random

#from threading import Thread
from thread2 import Thread
from threading import Lock

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

modim_websocket_server = None     # modim websocket handler
run = True                  # main_loop run flag
run_thread = None           # thread running the code
code_running = False        # code running
status = "Idle"             # robot status sent to websocket
last_answer = None
return_value = "OK"
conn_client = None          # Connected client
im = None                   # interaction manager
display_ws = None           # display ws object
robot_type = None           # None, pepper, marrtino, ...
robot_initialized = False   # if robot has been initialized

logfile = None              # log file


# Settings functions

def init_interaction_manager():
    global robot_type, robot_initialized, im, display_ws, robot
    print "Start interaction manager"
    print "  -- display init --"
    display_ws = DisplayWS()
    display_ws.cancel_answer()
    display_ws.remove_buttons()
    print "  -- robot init --"
    robot = None
    if (not robot_initialized): 
        if (robot_type=='pepper'):
            # Connection to robot
            pepper_cmd.robot = pepper_cmd.PepperRobot()
            pepper_cmd.robot.connect()
            if (pepper_cmd.robot.isConnected):
                robot_initialized = True
                robot = pepper_cmd.robot
        elif (robot_type=='marrtino'):
            pass
    im = interaction_manager.InteractionManager(display_ws, robot)


def quit_interaction_manager():
    global robot
    if (robot_type=='pepper'):
        pepper_cmd.robot.quit()


def init_GUI(robot_type,url):
    global robot
    # run in a separate thread (started before wssocket start, so it must wait before connection)
    time.sleep(3)
    if (robot_type=='pepper' and robot!=None and url!=None):
        robot.showurl(url)




def begin():
    # Note: this function is replaced by from <robot>_cmd import *
    print "WS begin"

def end():
    # Note: this function is replaced by from <robot>_cmd import *
    print "WS end"


# Basic UI functions

# Export commands, must set global variable return_value
class DisplayWS:

    def __init__(self):
        self.websocket_server = None
        self.mutex = Lock()
        self.reset_answer = False        # Request to stop waiting for answers

    def setws(self, websocket_server):
        self.websocket_server = websocket_server
    
    def websend(self, data):
        if (self.websocket_server == None):
            print('%sDisplayWS: websocket not connected.%s' %(RED,RESET))
            return
        try:
            self.mutex.acquire()
            self.websocket_server.write_message(data)
            #print(status)
        except tornado.websocket.WebSocketClosedError:
            print('%sDisplayWS: websocket connection error.%s' %(RED,RESET))
        finally:
            self.mutex.release()

    def display_text(self, data, place):
        global return_value
        cmdsend = "display_text_"+place+"_"+data
        print "web send: " + cmdsend
        self.websend(cmdsend)
        return_value = "OK"

    def display_image(self, data, place='default'):
        global return_value
        cmdsend = "display_image_"+place+"_"+data
        print "web send: " + cmdsend
        self.websend(cmdsend)
        return_value = "OK"

    def display_pdf(self, data, place='default'):
        global return_value
        cmdsend = "display_pdf_"+place+"_"+data
        print "web send: " + cmdsend
        self.websend(cmdsend)
        return_value = "OK"

    def display_imagebuttons(self, data): 
        global last_answer, return_value
        for d in data:
            self.websend("display_imagebutton_"+d+"\n")
            #time.sleep(0.01)
        last_answer = None
        return_value = "OK"

    def display_buttons(self, data): 
        global last_answer, return_value
        for d in data:
            print "WebSend: ", "display_button_"+d[0]+"$"+d[1]+"\n"
            self.websend("display_button_"+d[0]+"$"+d[1]+"\n")
            #time.sleep(0.1)
        last_answer = None
        return_value = "OK"

    def remove_buttons(self): 
        global return_value
        self.websend("remove_buttons")
        return_value = "OK"

    def answer(self):
        global last_answer, return_value
        self.reset_answer = False
        last_answer = None
        while (last_answer is None and not self.reset_answer):
            time.sleep(0.5)
        print "Answer: ",last_answer
        return_value = last_answer
        return return_value

    def setReturnValue(self, rv): # value returned to the client when remote program finishes
        global return_value
        return_value = rv

    def waitfor(self, data):
        while (self.answer()!=data and not self.reset_answer):
            time.sleep(0.5)

    def cancel_answer(self):
        self.reset_answer = True

    def ask(self, data):
        remove_buttons()
        display_buttons(data)    
        a = answer()
        remove_buttons()
        if (a is not None):
            a = a.rstrip()
        return a

    def loadUrl(self, data):
        global return_value
        cmdsend = "url_"+data
        print "web send: " + cmdsend
        self.websend(cmdsend)
        time.sleep(0.5)
        return_value = "OK"


#def sensorvalue(data):
#    global return_value
#    val = None
#    print "Sensor ",data
#    if (data=='headtouch'):
#        val = pepper_cmd.headTouch
#    elif (data=='frontsonar'):
#        val = pepper_cmd.sonarValues[0]
#    elif (data=='backsonar'):
#        val = pepper_cmd.sonarValues[1]
#    print "Sensor value = ",val
#    return val


def client_return():
    global conn_client, return_value, last_answer
    if (conn_client is None):
        return
    try:
        if (last_answer != None):
            conn_client.send("%s\n" %last_answer)
            last_answer = None
        else:
            conn_client.send("%s\n" %return_value)
            
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
        try:
            run_thread.terminate()
            print "Run code thread: ",run_thread," terminated."
        except:
            print "Thread already terminated"
        code_running = False


# Log function

def logdata(data):
    global logfile
    pass
#    if (logfile == None):
#        logfile = open('ws_server.log','a')
#
#    timestamp = time.now()
#    logfile.write("%s;%r\n" %(timestamp, data))
#    logfile.flush()


# Run the code

def run_code(code):
    global status, return_value, conn_client, im, code_running, last_answer
    if (code is None):
        return
    print("Executing")
    print(code)

    print("=== Start code run ===")
    try:
        status = "Executing program"
        code_running = True
        exec(code)
        code_running = False
    except Exception as e:
        print("CODE EXECUTION ERROR")
        print e
    status = "Idle"
    ifreset()
    print("=== End code run ===")


# TCP command server

def start_cmd_server(TCP_PORT):
    global run, return_value, run_thread, conn_client, code_running

    TCP_IP = ''
    BUFFER_SIZE = 20000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(3)
    try:
        s.bind((TCP_IP,TCP_PORT))
        s.listen(1)
        run=True
    except:
        print RED+"Cmd Server: bind error"+RESET
        run=False        
    
    while run:

        if (code_running):
            print("%s== Code running: %r ==%s" %(RED,code_running,RESET))
            print("%s== Killing thread !!! ==%s" %(RED,RESET))
            ifreset(True)

        print("%sCmd Server: listening on port %d %s" %(GREEN,TCP_PORT,RESET))

        connected = False
        conn_client = None
        
        while (run and not connected):
            try:
                #print "GUI Waiting for connection ..."
                conn_client, addr = s.accept()
                print "Cmd Connection address:", addr
                connected = True
            except KeyboardInterrupt:
                print "User quit."
                run = False
            except socket.timeout:
                pass
            except Excpetion as e:
                print e
                run = False


        while (run and connected):
            data = ''
            while (run and connected and ((data=='') or (data[0]!='*' and data[0]!='[' and (not '###ooo###' in data)))):
                try:
                    d = conn_client.recv(BUFFER_SIZE)
                except:
                    print "Cmd Server: connection closed."
                    connected = False
                    break
                if (d==''):
                    break
                data = data + d
                #print "Received partial data: ",data

            if (not connected):
                break
            if (data==''):
                break

            #print "Received: ",data

            if (data[0]=='*'):
                print "Control: ",data[1:]
                global last_answer
                last_answer = data[1:]
            elif (data[0]=='['):
                print "Values: ",data                
            else:
                run_thread = Thread(target=run_code, args=(data,))
                run_thread.start()
                print "Thread started: ",run_thread



    #TODO Only if not asked explict load URL        
    ifreset(True)

    if (conn_client is not None):
        conn_client.close()
        conn_client = None
    print "Cmd Server: quit"
        
 



# Modim Websocket server handler

class ModimWebSocketServer(tornado.websocket.WebSocketHandler):

    def open(self):
        global modim_websocket_server, display_ws
        modim_websocket_server = self
        print('New modim websocket connection')
        print modim_websocket_server
        display_ws.setws(modim_websocket_server)
       
    def on_message(self, message):
        global last_answer
        print('Input received:\n%s' % message)
        self.write_message('OK') # reply back to ws client
        # store answer for program client
        last_answer = message
  
    def on_close(self):
        global modim_websocket_server
        print(RED+'Modim Websocket: connection closed'+RESET)
        #TODO Only if not asked explict load URL 
        #ifreset(True)
        modim_websocket_server = None
  
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



class CtrlWebSocketServer(tornado.websocket.WebSocketHandler):

    def open(self):
        print('New ctrl websocket connection')
       
    def on_message(self, message):
        global last_answer
        print('InCtrl input received:\n%s' % message)
        last_answer = message
  
    def on_close(self):
        print(RED+'Ctrl websocket: connection closed'+RESET)

    def check_origin(self, origin):
        #print("-- Request from %s" %(origin))
        return True


# Code Websocket server handler

class CodeWebSocketServer(tornado.websocket.WebSocketHandler):

    def open(self):
        print('New Code connection')
       
    def on_message(self, message):
        global code, status, robot
        if (message=='stop'):
            print('Stop code and robot')
            robot.stop_request = True
            robot.stop()
        else:
            print('Code received:\n%s' % message)
            if (status=='Idle'):
                t = Thread(target=run_code, args=(message,))
                t.start()
            else:
                print('Program running. This code is discarded.')
        self.write_message('OK')
  
    def on_close(self):
        print('Code Connection closed')
  
    def on_ping(self, data):
        print('ping received: %s' %(data))
  
    def on_pong(self, data):
        print('pong received: %s' %(data))
  
    def check_origin(self, origin):
        #print("-- Request from %s" %(origin))
        return True


# Main program

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-modimwsport", type=str, default=9100,
                        help="MODIM WS Server port.")
    parser.add_argument("-codewsport", type=str, default=9010,
                        help="Code WS Server port.")
    parser.add_argument("-cmdport", type=int, default=9101,
                        help="Command Server port")
    parser.add_argument("-robot", type=str, default=None,
                        help="Robot type [None, pepper, marrtino]")
    parser.add_argument("-url", type=str, default=None,
                        help="URL of main HTML file")

    args = parser.parse_args()

    modim_ws_server_port = args.modimwsport
    code_ws_server_port = args.codewsport
    cmd_server_port = args.cmdport
    robot_type = args.robot

    if (robot_type=='pepper'):
        try:
            pepper_tools_dir = os.getenv("PEPPER_TOOLS_HOME")
            sys.path.append(pepper_tools_dir+'/cmd_server')
            import pepper_cmd
            from pepper_cmd import *
        except Exception as e:
            print e
            print("%sSet environment_variable PEPPER_TOOLS_HOME to pepper_tools directory.%s" %(RED,RESET))
            sys.exit(0)
    elif (robot_type=='marrtino'):
        try:
            marrtino_apps_dir = os.getenv("MARRTINO_APPS_HOME")
            sys.path.append(marrtino_apps_dir+'/program')
            import robot_cmd_ros
            from robot_cmd_ros import *
        except:
            print("%sSet environment_variable MARRTINO_APPS_HOME to marrtino_apps directory.%s" %(RED,RESET))
            sys.exit(0)



    # Run command server
    t = Thread(target=start_cmd_server, args=(cmd_server_port,))
    t.start()

    # Init robot display object and IM
    init_interaction_manager()

    # Run websocket server
    application1 = tornado.web.Application([
        (r'/modimwebsocketserver', ModimWebSocketServer),])  
    http_server = tornado.httpserver.HTTPServer(application1)
    http_server.listen(modim_ws_server_port)
    print("%sModim Websocket server: listening on port %d %s" %(GREEN,modim_ws_server_port,RESET))

    application2 = tornado.web.Application([
        (r'/ctrlwebsocketserver', CtrlWebSocketServer),])  
    ctrl_ws_server_port = modim_ws_server_port + 10
    http_server2 = tornado.httpserver.HTTPServer(application2)
    http_server2.listen(ctrl_ws_server_port)
    print("%sCtrl websocket server: listening on port %d %s" %(GREEN,ctrl_ws_server_port,RESET))

    application3 = tornado.web.Application([
        (r'/websocketserver', CodeWebSocketServer),])  
    http_server = tornado.httpserver.HTTPServer(application3)
    http_server.listen(code_ws_server_port)
    print("%sCode Websocket server: listening on port %d %s" %(GREEN,code_ws_server_port,RESET))


    # Init GUI
    t_initgui = Thread(target=init_GUI, args=(robot_type, args.url,))
    t_initgui.start()

    # Start websocket server
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print(" -- Keyboard interrupt --")
    try:
        modim_websocket_server.close()
    except:
        pass

    global logfile
    if (logfile != None):
        logfile.close()

    print("Web server quit.")
    run = False

    quit_interaction_manager()

    print("Waiting for main loop to quit...")

    sys.exit(0)

