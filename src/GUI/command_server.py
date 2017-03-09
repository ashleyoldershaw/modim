import socket
import sys
import time
import Tkinter as tk
import tkFileDialog
import threading 
#from Tkinter import *


# Global variables:
# net_ROS and net_speech : objects of class Network
SPEECH_SERVER_TCP_IP = '127.0.0.1'
SPEECH_SERVER_TCP_PORT = 1801
ROS_SERVER_TCP_IP = '127.0.0.1'
ROS_SERVER_TCP_PORT = 9000


class App(tk.Tk):

    def __init__(self, master):

        global ceck_connection_ros
        global ceck_connection_speech
        ceck_connection_ros =  tk.StringVar()
        ceck_connection_speech = tk.StringVar()

        ceck_connection_ros.set('Not Connected')
        ceck_connection_speech.set('Not Connected')

        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = master
        options['title'] = 'This is a title'

        
        tk.Label(master, text="ROS TCP server").grid(row=0, sticky=tk.W)
        tk.Label(master, textvariable=ceck_connection_ros).grid(row=0,column=2)
        tk.Label(master, text="Speech TCP server").grid(row=1, sticky=tk.W)
        tk.Label(master, textvariable=ceck_connection_speech).grid(row=1,column=2)

        self.e1 = tk.Entry(master)
        self.e1.insert(tk.ANCHOR, ROS_SERVER_TCP_IP)
        self.e2 = tk.Entry(master, width=10)
        self.e2.insert(tk.ANCHOR, ROS_SERVER_TCP_PORT)
        self.e1.grid(row=0, column=1, sticky=tk.W)
        self.e2.grid(row=0, column=1, sticky=tk.E)
        
        self.button1 = tk.Button(master, text="Reset", command=self.reset_listener_ros)
        self.button1.grid(row=0, column=2, sticky=tk.W)
        
        self.e3 = tk.Entry(master)
        self.e3.insert(tk.ANCHOR, SPEECH_SERVER_TCP_IP)
        self.e4 = tk.Entry(master, width=10)
        self.e4.insert(tk.ANCHOR, SPEECH_SERVER_TCP_PORT)
        self.e3.grid(row=1, column=1, sticky=tk.W)
        self.e4.grid(row=1, column=1, sticky=tk.E)
        
        self.button2 = tk.Button(master, text="Reset", command=self.reset_listener_speech)
        self.button2.grid(row=1, column=2, sticky=tk.W)

        
        tk.Label(master, text="Message to GUI from ROS Server").grid(row=2, sticky=tk.W)
        self.e5 = tk.Entry(master, width=55)
        self.e5.grid(row=2, column=1, columnspan=2, sticky=tk.W)
        self.button3 = tk.Button(master, text="Send", command=self.send_message_ros)
        self.button3.grid(row=2, column=2)
        
        tk.Label(master, text="Message to GUI from SpeechServer").grid(row=3, sticky=tk.W)
        self.e6 = tk.Entry(master, width=55)  
        self.e6.grid(row=3, column=1, columnspan=2, sticky=tk.W)
        self.button4 = tk.Button(master, text="Send", command=self.send_message_speech)
        self.button4.grid(row=3, column=2)
        
        tk.Label(master, text="Messages text file (Ros)").grid(row=4, sticky=tk.W)
        self.e7 = tk.Entry(master, width=32)
        self.e7.grid(row=4, column=1, sticky=tk.W)
        self.button5 = tk.Button(master, width=5, text='Open file', command=self.askopenfile_name_ros).grid(row=4, column=2, sticky=tk.W)
        self.button6 = tk.Button(master, text="Send", command=self.send_file_messages_ros)
        self.button6.grid(row=4, column=2)
        
        tk.Label(master, text="Messages text file (Speech)").grid(row=5, sticky=tk.W)
        self.e8 = tk.Entry(master, width=32)
        self.e8.grid(row=5, column=1, sticky=tk.W)
        self.button7 = tk.Button(master, width=5, text='Open file', command=self.askopenfile_name_speech).grid(row=5, column=2, sticky=tk.W)
        self.button8 = tk.Button(master, text="Send", command=self.send_file_messages_speech)
        self.button8.grid(row=5, column=2)
        
        tk.Label(master, text="Message from RosClient").grid(row=7, column=0, columnspan=2)
        tk.Label(master, text="Message from SpeechClient").grid(row=7, column=2, columnspan=2)
        
        global rcvd_ros
        rcvd_ros=tk.StringVar()
        rcvd_ros.set("Message from GUI to ros")
        self.rootText1 = tk.Text(master, width=60, height=20)
        self.rootText1.grid(row=8, column=0, columnspan=2)
        self.rootText1.insert('1.0', rcvd_ros.get())
        self.rootText1.insert('end', '\n')
        rcvd_ros.trace_variable('w', self.update_txt_ros)
        

        
        global rcvd_speech
        rcvd_speech=tk.StringVar()
        rcvd_speech.set("Message from GUI to speech")
        self.rootText2 = tk.Text(master, width=60, height=20)
        self.rootText2.grid(row=8, column=2)
        self.rootText2.insert('1.0', rcvd_speech.get())
        self.rootText2.insert('end', '\n')
        rcvd_speech.trace('w', self.update_txt_speech)
        
       
    def askopenfile_name_ros(self):
        global flag_connection_ros
        global ros_connection

        #return tkFileDialog.askopenfile(mode='r', **self.file_opt)
        ros_mes_file_name = tkFileDialog.askopenfilename(**self.file_opt)  
        #ros_mes_file = tkFileDialog.askopenfile(mode='r', **self.file_opt)  
        self.e7.delete(0, tk.END)
        self.e7.insert(0, ros_mes_file_name)
        
        #print ros_mes_file.read()
    
    def send_file_messages_ros(self):
        global flag_connection_ros
        global ros_connection

        try:
         file =  open(self.e7.get(), 'r')
           #ros_connection.send(line)
        
         if flag_connection_ros == True:
             line = file.readline()
             while line:
                 if line.find('sleep') >= 0:
                     sec = int(line[6])
                     #print 'I am in sleep'
                     #print sec
                     time.sleep(sec)
                 else:
                     ros_connection.send(line)
                 line=file.readline() 

         file.close()

        except:
           print 'Error processing file, ceck the correctnes or try to chose another one!!!'

    def askopenfile_name_speech(self):
        global flag_connection_speech
        global speech_connection

        speech_mes_file_name = tkFileDialog.askopenfilename(**self.file_opt)  
        self.e8.delete(0, tk.END)
        self.e8.insert(0, speech_mes_file_name)
        

    def send_file_messages_speech(self):
        global flag_connection_speech
        global speech_connection

        try:
         file =  open(self.e8.get(), 'r')
           #ros_connection.send(line)
        
         if flag_connection_speech == True:
             line = file.readline()
             while line:
                 if line.find('sleep') >= 0:
                     sec = int(line[6])
                     #print 'I am in sleep'
                     #print sec
                     time.sleep(sec)
                 else:
                     speech_connection.send(line)
                 line=file.readline() 

         file.close()

        except:
           print 'Error processing file, ceck the correctnes or try to chose another one!!!'


    def update_txt_speech(self,a,b,c):
        global rcvd_speech
        self.rootText2.insert('end', rcvd_speech.get())

        self.rootText2.update_idletasks()
    
    def update_txt_ros(self,a,b,c):
        global rcvd_ros
        self.rootText1.insert('end', rcvd_ros.get())
        self.rootText1.update_idletasks()

    def send_message_ros(self):
        global flag_connection_ros
        global ros_connection

        if flag_connection_ros == True:
            ros_connection.send(self.e5.get())

    def send_message_speech(self):
        global flag_connection_speech
        global speech_connection

        if flag_connection_speech == True:
            speech_connection.send(self.e6.get())

    def reset_listener_ros(self):
        global ros_thread
        global ceck_connection_ros
        global ros_connection
        global ROS_SERVER_TCP_IP
        global ROS_SERVER_TCP_PORT
        global sock_ros


        ceck_connection_ros.set('Connection')
        sock_ros.shutdown(socket.SHUT_RDWR)
        sock_ros.close()
        
        if flag_connection_ros == True:
            ros_connection.shutdown(socket.SHUT_RDWR)
            ros_connection.close()
            pass
        
        ROS_SERVER_TCP_IP=self.e1.get()
        ROS_SERVER_TCP_PORT=int(self.e2.get())
        
        time.sleep(5)
        if not ros_thread.is_alive():
            try:
                sock_ros = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_ros.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                ros_thread = threading.Thread(name='ros_connection', target=ros_connection)
                ros_thread.start()
            except:
              print "Error: unable to start thread"

    def reset_listener_speech(self):
        global speech_thread
        global ceck_connection_speech
        global speech_connection
        global SPEECH_SERVER_TCP_IP
        global SPEECH_SERVER_TCP_PORT
        global sock_speech


        ceck_connection_speech.set('Connection')
        sock_speech.shutdown(socket.SHUT_RDWR)
        sock_speech.close()
        
        if flag_connection_speech == True:
            speech_connection.shutdown(socket.SHUT_RDWR)
            speech_connection.close()
            pass
        
        SPEECH_SERVER_TCP_IP=self.e3.get()
        SPEECH_SERVER_TCP_PORT=int(self.e4.get())
        
        time.sleep(5)
        if not speech_thread.is_alive():
            try:
                sock_speech = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_speech.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                speech_thread = threading.Thread(name='speech_connection', target=speech_connection)
                speech_thread.start()
            except:
              print "Error: unable to start thread"

    def quit(self):
       ros_thread_stop.set()
       speech_thread_stop.set()
    pass

        


        


def ros_connection():
    
    global ceck_connection_ros
    global rcvd_ros
    global ros_connection
    global ros_client_addres
    global flag_connection_ros

    #print "Thread ros started 1"
    ros_server_address=(ROS_SERVER_TCP_IP,ROS_SERVER_TCP_PORT)
    sock_ros.bind(ros_server_address)
    print >>sys.stderr, 'Starting up ROS server on %s port %s \n' % sock_ros.getsockname()
    sock_ros.listen(1)

    print >>sys.stderr, 'ROS server is waiting for a connection \n'

    while(not ros_thread_stop.is_set()):

        try:
            #print >>sys.stderr, 'Ros server is waiting for a connection \n'
            ros_connection, ros_client_address = sock_ros.accept()
            ceck_connection_ros.set('Connected')
            flag_connection_ros = True
        
        except socket.timeout:
           continue
        
        except:
            print 'ROS socket closed'
            return

        try:
            print >> sys.stderr, 'client connected:', ros_client_address
            BUFFER_SIZE = 1024
            while(not ros_thread_stop.is_set()):
                data = ros_connection.recv(BUFFER_SIZE)
                if data:
                    print >>sys.stderr, 'received "%s" \n' % data 
                    rcvd_ros.set(data+'\n')
                elif data == '':
                    print ' Connection closed'
                    ceck_connection_ros.set('Not Connected')
                    ros_connection.close()
                    break
        except:
            print 'ROS connetion socket closed'
            return
    
    

def speech_connection():
    
    global ceck_connection_speech
    global rcvd_speech
    global speech_connection
    global speech_client_addres
    global flag_connection_speech

    print "Thread speech started"
    speech_server_address=(SPEECH_SERVER_TCP_IP,SPEECH_SERVER_TCP_PORT)
    sock_speech.bind(speech_server_address)
    print >>sys.stderr, 'Starting up Speech server on %s port %s \n' % sock_speech.getsockname()
    sock_speech.listen(1)

    print >>sys.stderr, 'Speech server is waiting for a connection \n'
    while(not speech_thread_stop.is_set()):

        try:
            #print >>sys.stderr, 'Speech server is waiting for a connection \n'
            speech_connection, speech_client_address = sock_speech.accept()
            ceck_connection_speech.set('Connected')
            flag_connection_speech = True
           
        except socket.timeout:
           continue
        except:
            #sock_speech.close()
            print "Speech socket closed"
            return

        try:
            print >> sys.stderr, 'client connected:', speech_client_address
            BUFFER_SIZE = 1024
            while(not speech_thread_stop.is_set()):
                try:
                   data = speech_connection.recv(BUFFER_SIZE)
                except sock_speech.timeout:
                   continue
                if data:
                    print >>sys.stderr, 'received "%s" \n' % data
                    rcvd_speech.set(data+'\n')
                elif data == '':
                    print 'Connection closed'
                    ceck_connection_speech.set('Not Connected')
                    speech_connection.close()
                    break
        except:
             #connection.close()
             print 'Speech connection socket closed'
             return



flag_connection_ros = False
flag_connection_speech = False

ros_thread_stop= threading.Event()
speech_thread_stop= threading.Event()

sock_ros = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_ros.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
sock_ros.settimeout(1)

sock_speech = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_speech.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
sock_speech.settimeout(1)

def main():
    
    global ros_thread
    global speech_thread

    try:
        ros_thread = threading.Thread(name='ros_connection', target=ros_connection)
        speech_thread = threading.Thread(name='speech_connection', target=speech_connection)
        
        ros_thread.start()
        speech_thread.start()
    except:
        print "Error: unable to start threads"
    
    
    root = tk.Tk()
    root.title('COACHES TEST GUI')
    app = App(root)
    root.mainloop()

    app.quit()

if __name__ == '__main__':
   main()
