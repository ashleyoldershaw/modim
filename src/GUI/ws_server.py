# http://www.html.it/pag/53419/websocket-server-con-python/
# sudo -H easy_install tornado

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import time
from threading import Thread

#from dummy_robot import begin,end,forward,backward,left,right

#import sys
#sys.path.append('../program')



# Global variables

websocket_server = None     # websocket handler
run = True                  # main_loop run flag
server_port = 9000          # web server port
code = None
status = "Idle"             # robot status sent to websocket
last_answer = None
return_value = "OK"

# Basic UI functions

def websend(data):
    global websocket_server
    try:
        websocket_server.write_message(data)
        #print(status)
    except tornado.websocket.WebSocketClosedError:
        #print('Connection closed.')
        websocket_server = None

# Export commands, must set global variable return_value
def display_text(data):
    global return_value
    websend("display_text_"+data)
    return_value = "OK"

def display_image(data):
    global return_value
    websend("display_image_"+data)
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
    global last_answer, return_value
    while (last_answer is None):
        time.sleep(0.5)
        print "Answer: ",last_answer
    return_value = last_answer



# TCP command server

def run_code(code):
    global status
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
    print("=== End code run ===")


def start_cmd_server(TCP_PORT):
    global run, return_value

    TCP_IP = ''
    BUFFER_SIZE = 20000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    s.listen(1)

    run=True

    while run:
        print "GUI Program Server: listening on port", TCP_PORT
        connected = False
        conn = None
        try:
            conn, addr = s.accept()
            print "Connection address:", addr
            connected = True
        except KeyboardInterrupt:
            print "User quit."
            run = False
        while connected:
            try:
                data = conn.recv(BUFFER_SIZE)
            except:
                print "Connection closed."
                break
            if not data: break
            print "Received: ",data

            #t = Thread(target=run_code, args=(data,))
            #t.start()

            run_code(data)
            conn.send("%s\n" %return_value)

        if (conn is not None):
            conn.close()
        print "Closed connection"






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
        print('Connection closed')
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


    # Run websocket server
    application = tornado.web.Application([
        (r'/websocketserver', MyWebSocketServer),])  
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(server_port)
    print("Websocket server: listening on port %d" %(ws_server_port))
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print(" -- Keyboard interrupt --")

    if (not websocket_server is None):
        websocket_server.close()
    print("Web server quit.")
    run = False
    print("Waiting for main loop to quit...")


