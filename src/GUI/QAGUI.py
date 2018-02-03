#!/usr/bin/env python
#

try:
   # for Python3
   import tkinter as tk
   from tkinter import *
except ImportError:
   # for Python2
   import Tkinter as tk
   from Tkinter import *

import PIL

try:
    from PIL import Image, ImageTk
except:
    print("Please install ImageTk: sudo apt-get install python-imaging-tk")

import tkFileDialog

#import cv2
import socket
import threading
import errno, time

import os
script_dir = os.path.dirname(__file__)
working_folder = script_dir

#demo_folder='' # to select the demo with a filedialog box
demo_folder=os.path.dirname('../../demo/eurobotics/') # to start directly with this demo

import glob

import sys
sys.path.append('../action')
from actionReader import *
from actionWriter import ActionWriter
from profileMatcher import ProfileMatcher

profile = ['*', '*', '*', '*'] #the default profile

#demos_filename = "demos"


# Global variables:
# net_ROS and net_speech : objects of class Network
#SPEECH_SERVER_TCP_IP = '192.168.88.31'
#SPEECH_SERVER_TCP_PORT = 5000
SPEECH_SERVER_TCP_IP = '127.0.0.1'
SPEECH_SERVER_TCP_PORT = 1800
#SPEECH_SERVER_TCP_IP = '10.0.0.1'
#SPEECH_SERVER_TCP_PORT = 1800
#ROS_SERVER_TCP_IP = '10.10.10.30'
#ROS_SERVER_TCP_IP = '192.168.43.2'
ROS_SERVER_TCP_IP = '127.0.0.1'
#ROS_SERVER_TCP_IP = '192.168.88.30' #cadomus, diago
#ROS_SERVER_TCP_IP = '192.168.88.31' #romus
#ROS_SERVER_TCP_IP = '192.168.0.204'
ROS_SERVER_TCP_PORT = 9000

# Surface tablet
#screen_width = 1430
#screen_height = 920
#topframe_w = 800
#topframe_h = 500
#buttonfontsize = 22
#hbutton = 200
#max_label_font_size = 60
#max_label_height = 300
#langbutton_size = 90

# ASUS tablet
screen_width = 1000
screen_height = 600
topframe_w = 500
topframe_h = 300
buttonfontsize = 16
hbutton = 150
max_label_font_size = 40
max_label_height = 280
langbutton_size = 60

TTSfree = True
buttonsTriggered = True


class logInteraction:
   def createLogFile(self):
      global working_folder
      if not os.path.exists(working_folder+'/logs'):
         print "Creating log folder in"+ working_folder+ '/logs'
         os.makedirs(working_folder+'/logs')
      else:
         print "Log folder already exists in"+ working_folder+ '/logs'
         
      files_in_directory = glob.glob(working_folder+'/logs/*.log')
      if len(files_in_directory) > 0:
         for index in range(len(files_in_directory)):
            files_in_directory[index] = os.path.basename(files_in_directory[index])

      demoname = os.path.basename(working_folder)
      nextsequence = 0
      if len(files_in_directory) > 0:
         nextsequence = self.findNextNumberSequence(files_in_directory,demoname)

      self.logfilename = working_folder+'/logs/'+demoname+'_%04d.log'%(nextsequence)
      print "Creating log file in: ", self.logfilename
      self.logfile = open(self.logfilename, 'w')
      

   def findNextNumberSequence(self,sequence_of_files,demoname):
      nextsequence = 0
      for f in sequence_of_files:
         #n = int(f.lstrip(demoname+'_').rstrip('.log')) #Gives problems with numbers in demoname
         l = f.split('_')
         lastpart = l[len(l)-1]
         n = int(lastpart.rstrip('.log'))
         if n >= nextsequence:
            nextsequence = n+1
      return nextsequence

   def log(self, instruction):
      print 'logging instruction'
      self.logfile.write(instruction)
      self.logfile.flush()

logger = logInteraction()


def findSemanticButton(asrmsg):
   asrword = asrmsg.split("\"")[1]
   for button in net_ROS.buttons_to_display:
      topic = button[0]
      topics = topic.split("|")
      print topics	
      if len(topics) > 1:
         if topics[1] == asrword:
            return topics[0]
      elif len(topics) <= 1:
         if topics[0] == asrword:
            return topics[0]
   return asrword         
         
      
   




class Network:
   #This class starts the network and launches a thread to receive asynchronous messages
   def __init__(self, serverTcpIP, serverPort):
      self.serverTcpIP = serverTcpIP
      self.serverPort = serverPort
      self.recvmsg = ''
      self.demo_path = ''
      self.text_to_display = ''
      self.image_to_display = ''
      self.buttons_to_display = ''
      self.netStatusOk = False
      self.thread_stop= threading.Event()
      #self.initNetwork() # It will try to connect in the veirfyNetwork thread
      self.netStatusThread = threading.Thread(target=self.verifyNetwork)
      self.netStatusThread.start()
      self.parent = ''
      self.textSynthTime = time.time()
      print 'Network started.'

   def setParent(self, parent):
      self.parent = parent # mantains link to the GUI so we can generate events on it

   def verifyNetwork(self):
      while (not self.thread_stop.is_set()):
         if (not self.netStatusOk):
            print 'Trying to reconnect'
            self.initNetwork()
         else:
            secsToSleep = 1
            time.sleep(secsToSleep)
      print 'Finished verifyNetwork thread'

   def initNetwork(self):
      while (not self.thread_stop.is_set()):
         try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(1)
            self.sock.connect((self.serverTcpIP, self.serverPort))
            print "Connected to %s:%s." % (self.serverTcpIP,self.serverPort)
            self.recvThread = threading.Thread(target=self.receiveMessage)
            self.recvThread.start()
            self.netStatusOk = True
            if (self.serverPort == SPEECH_SERVER_TCP_PORT):
               # Initialization for Speech
               self.sendMessage("[CONNECT]PythonTestClient\n")
               time.sleep(0.2)
               self.sendMessage("[INIT]\n")
               #time.sleep(0.2)
               #self.sendMessage("[BEEP]880|500\n");
            break
         except socket.error as e:
            #print '[error]', e , self.serverTcpIP, ':', self.serverPort
            if (e.errno == errno.ECONNREFUSED):
               #print 'not able to connect', self.serverTcpIP, ':', self.serverPort
               secsToSleep = 5
               #print "trying to reconnect in %d seconds" % (secsToSleep)
               time.sleep(secsToSleep)
         

   def receiveMessage(self):
      #generates events to update the GUI based on the received messages
      BUFFER_SIZE = 1024
      while (not self.thread_stop.is_set()):
         try:
            self.recvmsg = self.sock.recv(BUFFER_SIZE)
         except socket.timeout:
            continue
            
         if (not self.recvmsg):
            #if there is no data something happened in the server
            self.netStatusOk = False
            break

         global profile
         global TTSfree 
         global buttonsTriggered

         print 'received: ', self.recvmsg
         if (self.recvmsg.find("OK") < 0):
            # net_ROS object will receive:
            #  'display_{text|image|video}_welcome'
            #  'say_welcome'
            #  'ask_needhelp'
            # net_speech object will receive:
            #  'ASR_text'
            self.recvmsg = self.recvmsg.replace('\x00',"").strip(' \n\r')
            splitmsg = self.recvmsg.split("_") # Example: returns ['display', 'text', 'welcome']

            print "RECEIVED: ", self.recvmsg
            #if (len(splitmsg) > 3 or len(splitmsg) < 2):
            if (self.serverPort == SPEECH_SERVER_TCP_PORT):
               if (self.recvmsg.startswith("[END_SYNTH]")):
                  print 'setting TTSfree true'
                  TTSfree = True
                  net_ROS.sendMessage("[END_SYNTH]\n\r")

                  #display buttons now that the question finished
                  if not buttonsTriggered and len(net_ROS.buttons_to_display) > 0:
                     net_ROS.parent.parent.event_generate("<<NewButtonsMessage>>", when='tail')
                     buttonsTriggered = True

                  #self.textSynthTime = time.time()+1
               #elif (time.time() > self.textSynthTime):
               elif (TTSfree):
                  if (self.recvmsg.startswith("[")):
                     net_ROS.sendMessage("ASR "+self.recvmsg+"\n\r")
                  else:                     
                     print "ASR: ", self.recvmsg
                     print net_ROS.buttons_to_display
                     outtopic = findSemanticButton(self.recvmsg)
                     net_ROS.sendMessage("ASR SEMANTICS(\""+ outtopic+"\")\n\r")
                  
                  
               else:
                  print "Ignored ASR: ", self.recvmsg
            #elif (len(splitmsg) > 3 or len(splitmsg) < 2):
            #   print "I am:", self.serverTcpIP, ":", self.serverPort
               #if (self.parent):
               #   print "Generating event"
               #   self.parent.parent.event_generate("<<clearButtonsMessage>>", when='tail')
            #   print 'There is something wrong with the message format. Example: display_[mode]_[interactionname]'
            #   continue
            else:
               print "RECEIVED from ROS server"
               logger.log("RECEIVED "+self.recvmsg+"\n")

               if (splitmsg[0] == 'display' and splitmsg[1] == 'init'):
                  # tell the GUI to initialize
                  self.parent.parent.event_generate("<<resetMessage>>", when='tail')
                  
               #elif (splitmsg[0] == 'set' and splitmsg[1] == 'demo' and len(splitmsg) == 3):
                  # tell the GUI to change demo
                  #self.demo_path = splitmsg[2];
                  #self.parent.parent.event_generate("<<changeDemoMessage>>", when='tail')

               elif (splitmsg[0] == 'display'):
                  split2 = self.recvmsg.split("_",2) #E.g. for display_text_question_animal_001 returns ['display', 'text', 'question_animal_001']
                  mode = split2[1].upper()
                  interactionname = split2[2]
                  action_filename = self.getActionFilename(interactionname)

                  action = ActionReader(action_filename)
                  pm = ProfileMatcher(action, profile)
                  if (interactionname[0]=="["):
                     #debug mode. Only TEXT
                     actual_interaction=interactionname.strip("[]")
                     self.display('TEXT', actual_interaction)
                  else: 
                     if (mode == 'TXTIMG'):
                        #Both TEXT and IMAGE mode
                        actual_interaction = pm.evalSection('TEXT')
                        self.display('TEXT', actual_interaction)
                        actual_interaction = pm.evalSection('IMAGE')
                        self.display('IMAGE', actual_interaction)
                     else:
                        actual_interaction= pm.evalSection(mode)
                        self.display(mode, actual_interaction)

               elif (splitmsg[0] == 'ask'):
                  #This instruction involves displaying a text and showing a GUI with options for the user 
                  print "ASK RECEIVED: ", self.recvmsg
                  split2 = self.recvmsg.split("_",1)
                  interactionname = split2[1]
                  action_filename = self.getActionFilename(interactionname)

                  action = ActionReader(action_filename)
                  pm = ProfileMatcher(action, profile)
                  
                  actual_interaction = pm.evalSection('TEXT')
                  self.display('TEXT', actual_interaction)
                  
                  self.buttons_to_display = pm.evalSection('BUTTONS')
                  buttonsTriggered = False

                  grammar_command = pm.evalSection('ASRCMD')
                  if len(grammar_command) > 0:
                     net_speech.sendMessage(grammar_command+"\n")

               elif (splitmsg[0] == 'askimg'):
                  #This instruction involves displaying a text and image and showing a GUI with options for the user 
                  print "ASK IMG RECEIVED: ", self.recvmsg
                  split2 = self.recvmsg.split("_",1)
                  interactionname = split2[1]
                  action_filename = self.getActionFilename(interactionname)

                  action = ActionReader(interactionname)
                  pm = ProfileMatcher(action, profile)
                           
                  actual_interaction = pm.evalSection('TEXT')
                  self.display('TEXT', actual_interaction)
                  
                  self.buttons_to_display = pm.evalSection('BUTTONS')
                  buttonsTriggered = False

                  grammar_command = pm.evalSection('ASRCMD')
                  if len(grammar_command) > 0:
                     net_speech.sendMessage(grammar_command+"\n")

                  actual_interaction = pm.evalSection('IMAGE')
                  self.display('IMAGE', actual_interaction)
                  
               elif (splitmsg[0] == 'say' and  len(splitmsg) == 2):
                  # if (say_something) coming from tcp_interface: 
                  interactionname = splitmsg[1]
                  if (interactionname[0]=="["):
                     #debug mode. Only TEXT
                     actual_interaction=interactionname.strip("[]")
                     self.sayMessage([actual_interaction])
                  else:
                     action_filename = self.getActionFilename(interactionname)
                     action = ActionReader(action_filename)
                     pm = ProfileMatcher(action, profile)

                     #  look for the string to say according to user profile
                     actual_interaction = pm.evalSection('TEXT')
                     if (len(actual_interaction)>0):
                        list_of_texts = actual_interaction.split("|")
                        self.sayMessage(list_of_texts)
               
               elif (splitmsg[0] == 'set' and splitmsg[1] == 'profile' and len(splitmsg) == 3):
                  # tell the GUI to change demo
                  profile = splitmsg[2];
                  
               elif (splitmsg[0] == 'beep'):
                  net_speech.sendMessage("[BEEP]880|500\n");

               else:
                  print 'Unrecognized instruction'
                  continue


      print 'Finished receive thread'

   def getActionFilename(self, interactionname):
      #rules_filename = "_".join([mode, interactionname])
      #to correctly load the file if the GUI is not executed from the current dir
      rules_fullfilename = os.path.join(working_folder, "actions/"+interactionname)
   
      return rules_fullfilename

   def display(self, mode, actual_interaction):
      print actual_interaction
      if (len(actual_interaction)>0):
         # if (text) : show actual_interaction as a label in the GUI
         if (mode == 'TEXT'):
            list_of_texts = actual_interaction.split("|")
            self.text_to_display = list_of_texts[0]
            self.parent.ltext.event_generate("<<NewTextMessage>>", when='tail')
            self.sayMessage(list_of_texts)
      
         # if (image) : show image in actual_interaction as an image in the GUI
         if (mode == 'IMAGE'):
            self.image_to_display = actual_interaction
            self.parent.rimg.event_generate("<<NewImgMessage>>", when='tail')
      
         # if (video) : ...TODO

   def sayMessage(self, list_of_texts):
      global TTSfree

      text_say = []
      if (len(list_of_texts)>1):
         text_say = list_of_texts[1]
      else:
         text_say = list_of_texts[0]
      #self.textSynthTime = time.time()+3
      print 'setting TTSfree FALSE'
      TTSfree = False
      
      if (len(text_say)>1):
        print "[SAY] "+text_say+"|"+profile[2]
        net_speech.sendMessage("[SAY] "+text_say+"|"+profile[2])
      else:
        TTSfree = True
        net_ROS.sendMessage("[END_SYNTH]\n\r")
        

   def getNewMessage(self):
      return self.recvmsg

   def getDemoPath(self):
      return self.demo_path

   def getTextToDisplay(self):
      return self.text_to_display

   def getImgToDisplay(self):
      return self.image_to_display

   def getButtonsToDisplay(self):
      return self.buttons_to_display

   def sendMessage(self, message):
      if (self.netStatusOk):
         print "Sending: ", message
         self.sock.send(message)
      
   def closeConnection(self):
      self.thread_stop.set()
      print 'Finishing threads...'
      time.sleep(5)
      if self.netStatusOk:
         if (self.recvThread.isAlive() or self.netStatusThread.isAlive()):
            print 'ups.. some thread still alive'
      
      self.sock.close()
      print "Connection to %s:%s closed." % (self.serverTcpIP,self.serverPort)
      
class profileSelectionGUI(object):

   def __init__(self, parent):
      self.toplevel = tk.Toplevel(parent)
      self.chosen_profile = ''
      if (len(sys.argv) > 1):
         profiles_filename = sys.argv[1]
      else:
         profiles_filename = "instance"
      try:
         profiles_filename = os.path.join(working_folder, profiles_filename)
         f = open(profiles_filename, 'r')
      except IOError:
         print 'cannot open', profiles_filename
      else:

         def callback(text):
            self.chosen_profile = parseProfile(text)
            self.toplevel.destroy()

         #this is something temporal, we take just the 4 first profiles and show them in a grid
         # maxProfiles = 4
         # i=0
         # sizegrid = 2
         # for line in f:
         #    if (i == maxProfiles):
         #       break
         #    line = line.strip("\n")
         #    btn = tk.Button(self.toplevel, text=line, font=("Helvetica", buttonfontsize), command=lambda line=line: callback(line)).grid(row=i/sizegrid, column=i%sizegrid, sticky='EWNS')
         #    i +=1

         #this shows all profiles as a list
         for line in f:
            line = line.strip("\n")
            btn = tk.Button(self.toplevel, text=line, command=lambda line=line: callback(line))
            btn.pack()
            
         f.close()

   def show(self):
      self.toplevel.deiconify()
      self.toplevel.wait_window()
      return self.chosen_profile

class languageSelectionGUI(object):

   def __init__(self, parent):
      self.toplevel = tk.Toplevel(parent)
      self.chosen_profile = ''
      if (len(sys.argv) > 1):
         lang_profiles_filename = sys.argv[1]
      else:
         lang_profiles_filename = "lang_instance"

      lang_profiles_filename = os.path.join(working_folder, lang_profiles_filename)
      lang_action = ActionReader(lang_profiles_filename)

      def callback(text, button):
         self.chosen_profile = text
         self.button = button
         self.toplevel.destroy()

      list_of_rules = lang_action['IMAGE']
      print list_of_rules
      
      for profile in list_of_rules:
         language = profile[0]
         rel_path = profile[1]
         abs_file_path = os.path.join(working_folder, rel_path)
         imgbutton = PIL.Image.open(abs_file_path)
         w, h = imgbutton.size            
         imgbutton_resized = setHeight(w, h, hbutton, imgbutton, True)
         phbutton = ImageTk.PhotoImage(imgbutton_resized)
         btn = tk.Button(self.toplevel, image=phbutton, command=lambda language=language, button=imgbutton_resized: callback(language, button))
         btn.image = phbutton
         btn.pack(side=LEFT)
         

   def show(self):
      self.toplevel.deiconify()
      self.toplevel.wait_window()
      return (self.chosen_profile, self.button)


class demoSelectionGUI(object):

   def __init__(self, parent):
      global working_folder
      #if demo_folder=='':
      working_folder = tkFileDialog.askdirectory(parent=parent, initialdir=working_folder, title='Please select the demo directory')
      #else:
      #  working_folder = demo_folder    
      if len(working_folder) > 0:
         print "Demo selected: %s" % working_folder








      

def resize(w, h, w_box, h_box, pil_image, use_antialiasing):
   '''
   resize a pil_image object so it will fit into
   a box of size w_box times h_box, but retain aspect ratio
   '''
   f1 = 1.0*w_box/w  # 1.0 forces float division in Python2
   f2 = 1.0*h_box/h
   factor = min([f1, f2])
   # use best down-sizing filter
   width = int(w*factor)
   height = int(h*factor)
   if (use_antialiasing):
      return pil_image.resize((width, height), Image.ANTIALIAS) #this is really slow (~3-4s depending on size)
   else:
      return pil_image.resize((width, height), Image.NEAREST)

def setHeight(w, h, h_box, image, use_antialiasing):
   '''
   resize an image with height h maintaining aspect ratio
   '''
   factor = 1.0*h_box/h
   width = int(w*factor)
   height = int(h*factor)
   if (use_antialiasing):
      return image.resize((width, height), Image.ANTIALIAS) #this is really slow (~3-4s depending on size)
   else:
      return image.resize((width, height), Image.NEAREST)
         
def setWidth(w, h, w_box, image, use_antialiasing):
   '''
   resize an image with width w maintaining aspect ratio
   '''
   factor = (1.0*w_box)/(1.0*w)
   width = int(w*factor)
   height = int(h*factor)
   if (use_antialiasing):
      return image.resize((width, height), Image.ANTIALIAS) #this is really slow (~3-4s depending on size)
   else:
      return image.resize((width, height), Image.NEAREST)

class GUI(tk.Frame):

   def __init__(self, parent):
      global working_folder
      tk.Frame.__init__(self, parent)
      self.parent = parent
      net_ROS.setParent(self)
      net_speech.setParent(self)
      
      self.parent.title("Q&A GUI")
      self.parent.resizable(width=FALSE, height=FALSE)
      self.parent.bind("<<NewButtonsMessage>>", self.displayButtons)
      self.parent.bind("<<clearButtonsMessage>>", self.clearButtons)  
      self.parent.bind("<<resetMessage>>", self.resetGUICallback)
      #self.parent.bind("<<changeDemoMessage>>", self.changeDemo)
      self.parent.bind("<p>", self.profileSelection)
      self.parent.bind("<l>", self.languageSelection)
      self.parent.bind("<Button-3>", self.popup)
      self.parent.bind("<Button-1>", self.screentouched)

      self.pack(expand=100)
      
      self.buttonsList = []  
      
      #demoSelectionGUI(self.parent)
      working_folder = demo_folder
      self.initDemo()

      self.initUI()


   def initDemo(self):
      #global working_folder
      #working_folder = os.path.join(script_dir, demopath)
      #print demopath
      print "working folder: ", working_folder

      init_filename = os.path.join(working_folder, "init")
      self.config = ActionReader(init_filename)
      print self.config

      self.question = StringVar()
      self.question.set(self.config['WELCOMEMSG'])
      if (self.config.get('GRAMMAR') != None):
         grammar = "[LOAD_GRAMMAR] " + self.config['GRAMMAR'] +"\n"
         net_speech.sendMessage(grammar)
      global profile
      profile = parseProfile(self.config['PROFILE'])

   def initUI(self):
      logger.createLogFile()
      
      multilang = self.config['MULTILANG']
      if (multilang == 'YES'):
         self.profileframe = Frame(self)
         self.profileframe.configure(background='white')
         self.profileframe.pack(fill = tk.X)

      self.topframe = Frame(self)
      self.topframe.configure(background='white')
      self.topframe.pack(fill = tk.X)
      self.middleframe = Frame(self)
      self.middleframe.configure(background='white')
      self.middleframe.pack(fill = tk.X)
      self.bottomframe = Frame(self)
      self.bottomframe.configure(background='white')
      self.bottomframe.pack(fill = tk.X, expand=True)

      # PROFILE FRAME
      # Profile selection button
      if (multilang == 'YES'):
         lang_file = os.path.join(working_folder, "lang_instance")
         lang_action = ActionReader(lang_file)
         pm = ProfileMatcher(lang_action, profile)
         actual_interaction = pm.evalSection('IMAGE')
         abs_file_path = os.path.join(working_folder, actual_interaction)
         imgbutton = PIL.Image.open(abs_file_path)
         w, h = imgbutton.size            
         imgbutton_resized = setHeight(w, h, langbutton_size, imgbutton, True)
         phbutton = ImageTk.PhotoImage(imgbutton_resized)
         self.profilebutton = Button(self.profileframe, image=phbutton, command=self.languageSelection)
         self.profilebutton.image = phbutton
         self.profilebutton.configure(background='white')
         self.profilebutton.pack(side=RIGHT, fill='x')

      # TOP FRAME
      # Video
      width = topframe_w  # 800, 500
      height = topframe_h
      if (False):
         #rel_path = 'videos/rives_delorne.mp4'
         rel_path = 'videos/diag.mp4'
         abs_file_path = os.path.join(working_folder, rel_path)
         self.video = cv2.VideoCapture(abs_file_path)
         self.video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
         self.video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
         fps = self.video.get(cv2.cv.CV_CAP_PROP_FPS)
         time_rate = int(1/fps*1000)
         
         self.lvideo = tk.Label(self.topframe)
         #self.lvideo.bind("<<updateVideoFrame>>", self.updateVideoFrame)
         self.lvideo.pack(side = LEFT)

         #self.timerThread = threading.Thread(target=self.frameTimer, args = (fps,))
         #self.timerThread.start()
         #self.thread_stop = threading.Event()

         def show_frame():
            retval, frame = self.video.read()
            if (retval): # true = still frames to read
               start = time.time() 
               cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
               h, w = cv2image.shape[:2]
               img = Image.fromarray(cv2image)
               im_resized = setHeight(w, h, height, img, False)
               imgtk = ImageTk.PhotoImage(image=im_resized)
               finish = time.time()
               #print "time_rate: ", time_rate, " time consumed: " , finish - start
               needToSleep = int((time_rate*0.001 - (finish - start))*1000)
               self.lvideo.imgtk = imgtk
               self.lvideo.configure(image=imgtk)
               #print needToSleep
               if needToSleep > 0:
                    self.lvideo.after(needToSleep, show_frame)
               else:
                    self.lvideo.after(20, show_frame)
            else:
                self.video.release()
               
         show_frame()

      else:
         # Left Image
         rel_path = self.config['LEFTIMG']
         abs_file_path = os.path.join(working_folder, rel_path)
         img = PIL.Image.open(abs_file_path)
         w, h = img.size
         #if (1.0*w/(width/2.0) > 2.0*h/height):
         #    im_resized = setWidth(w, h, width/2, img, True)
         #else:
         #    im_resized = setHeight(w, h, height/2, img, True)

         #im_resized = setWidth(w, h, width/2, img, True)
         im_resized = resize(w, h, width, height, img, True)
         imgtk = ImageTk.PhotoImage(image=im_resized)
         self.limg = Label(self.topframe, image=imgtk)
         self.limg.configure(background='white')
         self.limg.image = imgtk
         self.limg.pack(side=LEFT) 
          
      # Right Image
      rel_path = self.config['RIGHTIMG']
      abs_file_path = os.path.join(working_folder, rel_path)
      img = PIL.Image.open(abs_file_path)
      w, h = img.size
      #im_resized = self.setHeight(w, h, height, img, True)
      #if (1.0*w/(width/2.0) > 1.0*h/height):
      #   im_resized = setWidth(w, h, width/2, img, True)
      #else:
      #   im_resized = setHeight(w, h, height, img, True) # was height/2
      im_resized = resize(w, h, width, height, img, True)
      #im_resized = setWidth(w, h, width/2, img, True)
      imgtk = ImageTk.PhotoImage(image=im_resized)
      self.rimg = Label(self.topframe, image=imgtk)
      self.rimg.configure(background='white')
      self.rimg.image = imgtk
      self.rimg.bind("<<NewImgMessage>>", self.updateImg)
      self.rimg.pack(side=RIGHT) 

      # MIDDLE FRAME
      # Label
      self.ltext = Label(self.middleframe, textvariable=self.question, font=("Helvetica", max_label_font_size), wraplength=screen_width,background='white')
      self.setSizeTextLabel()
      self.ltext.bind("<<NewTextMessage>>", self.updateLabel)
      self.ltext.pack()

      # BOTTOM FRAME
      # Buttons will be shown only if a question of yes|no is received

      # MENU RIGHT-CLICK BUTTON
      self.aMenu = tk.Menu(self.parent, tearoff=0)
      self.aMenu.add_command(label="Load demo", command=self.loadDemo)
      
   def loadDemo(self):
      demoSelectionGUI(self)
      self.initDemo()
      self.resetGUI()
      
   def popup(self, event):
      self.aMenu.post(event.x_root, event.y_root)

   def screentouched(self, event):
      print "Screen touched"
      net_ROS.sendMessage("BUTTON screentouched\n\r")

   def setSizeTextLabel(self):
      defaultsize = max_label_font_size
      fits = False
      maxwidth, maxheight = screen_width, max_label_height
      while (not fits):
         self.ltext.config(font=("Helvetica", defaultsize))
         if (self.ltext.winfo_reqwidth() < maxwidth and self.ltext.winfo_reqheight() < maxheight):
            fits = True
            
         defaultsize=defaultsize-5

   def updateLabel(self, event):
      self.parent.event_generate("<<clearButtonsMessage>>")
      print 'Event triggered. updateLabel'
      self.question.set(net_ROS.getTextToDisplay())
      self.setSizeTextLabel()
      
      
   def updateImg(self, event):
      print 'Event triggered. updateImg'
      img_name = net_ROS.getImgToDisplay()
      abs_file_path = os.path.join(working_folder, img_name)
      img = PIL.Image.open(abs_file_path)
      w, h = img.size
      width = topframe_w
      height = topframe_h
      #im_resized = setHeight(w, h, height, img, True)
      im_resized = resize(w, h, width, height, img, True)
      imgtk = ImageTk.PhotoImage(image=im_resized)
      self.rimg.configure(image = imgtk)
      self.rimg.image = imgtk
      
   def frameTimer(self, fps):
      #time_rate in ms to show the images in the video
      time_rate = int(1/fps*1000)
      print "FPS: ", fps, " TIME RATE: ", time_rate
      while (not self.thread_stop.is_set()):
         start = time.time()
         #print "starts:", start
         if (self.video.isOpened()):
            #this function consumes (blocks) the time to process the event (updateVideoFrame in this case)
            self.lvideo.event_generate("<<updateVideoFrame>>")
            finish = time.time()
            #print "finishes: ", finish - start
            #we substract the consumed time to the time needed to sleep between frames
            needToSleep = time_rate*0.001 - (finish - start)
            print "needToSleep", needToSleep
            if (needToSleep>0):
               time.sleep(needToSleep)
         else:
            #video closed, nothing else to show
            break

      print "Finished frameTimer thread"

   def updateVideoFrame(self, event):
      print 'Event triggered. updateVideoFrame'
      start = time.time()
      width, height = 500, 375

      if (self.video.isOpened()):
         retval, frame = self.video.read()
         if (retval): # true = still frames to read
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            h, w = cv2image.shape[:2]
            img = Image.fromarray(cv2image)
            im_resized = setHeight(w, h, height, img, False)
            imgtk = ImageTk.PhotoImage(image=im_resized)
            self.lvideo.configure(image = imgtk)
            self.lvideo.imgtk = imgtk
         else:
            #finished reading the file
            self.video.release()
            
      print "this function takes: " , time.time() - start, "seconds"

   def languageSelection(self):
      global profile
      (selection, button) = languageSelectionGUI(self).show()
      w, h = button.size            
      imgbutton_resized = setHeight(w, h, langbutton_size, button, True)
      phbutton = ImageTk.PhotoImage(imgbutton_resized)
      self.profilebutton.configure(image = phbutton)
      self.profilebutton.image = phbutton
      print "Selection: " , selection
      if (len(selection) > 0):
         profile = selection
      print "New profile: " , profile


   def profileSelection(self, event):
      print "Key p pressed"
      global profile
      selection = profileSelectionGUI(self).show()
      print "Selection: " , selection
      if (len(selection) > 0):
         profile = selection
      print "New profile: " , profile

   def clearButtons(self, event):
      print 'Event triggered. clearButtons'
      for index in range(len(self.buttonsList)):
         self.bottomframe.grid_columnconfigure(index, weight=0)

      for btn in self.buttonsList:
         btn.destroy()
      self.buttonsList = []

   def buttonsCallback(self, text):
      self.chosen_button_action = text
      print "User selection: " , self.chosen_button_action

      topic = self.chosen_button_action.split("|")[0]
      net_ROS.sendMessage("BUTTON "+topic+"\n\r")

      logger.log("BUTTON "+topic+"\n")
      self.parent.event_generate("<<clearButtonsMessage>>")

   def displayButtons(self, event):
      print 'Event triggered. displayButtons'
      self.buttonsList = []
      self.buttonsToDisplay = net_ROS.getButtonsToDisplay()
      max_reqheight = 0
      
      buttonid = 0
      maxsizegrid = 7
      if len(self.buttonsToDisplay) > maxsizegrid:
         if len(self.buttonsToDisplay)/2 <= maxsizegrid:
            sizegrid = len(self.buttonsToDisplay)/2
         else:
            sizegrid = maxsizegrid
      else:
         sizegrid = len(self.buttonsToDisplay)

      for button in self.buttonsToDisplay:
         print button
         command = button[0]
         display = button[1]

         if display[0:4] == "img/":
            rel_path = display
            abs_file_path = os.path.join(working_folder, rel_path)
            imgbutton = PIL.Image.open(abs_file_path)
            w, h = imgbutton.size            
            #imgbutton_resized = self.setHeight(w, h, hbutton, imgbutton, True)
            button_width = (screen_width-80)/sizegrid
            imgbutton_resized = resize(w, h, button_width, hbutton, imgbutton, True)
            phbutton = ImageTk.PhotoImage(imgbutton_resized)
            btn = tk.Button(self.bottomframe, image=phbutton, command=lambda command=command: self.buttonsCallback(command))
            btn.image = phbutton
            #column= buttonid%sizegrid
            #btn.grid(row=buttonid/sizegrid, column=column,  sticky=W+E+N+S)
            #btn.configure(background='white', activebackground='white')
            #self.bottomframe.grid_columnconfigure(column, weight=1)
            #buttonid +=1
         else:
            btn = tk.Button(self.bottomframe, text=display, font=("Helvetica", buttonfontsize), wraplength=screen_width/len(self.buttonsToDisplay), command=lambda command=command: self.buttonsCallback(command))
            #btn.configure(background='white', activebackground='white', width=60/len(self.buttonsToDisplay))
            #btn.pack(side=LEFT, fill=tk.X)

         column= buttonid%sizegrid
         btn.grid(row=buttonid/sizegrid, column=column, sticky=N+S+W+E)
         btn.configure(background='white', activebackground='white')
         self.buttonsList.append(btn)
         self.bottomframe.grid_columnconfigure(column, weight=1)
         buttonid +=1

         #if btn.winfo_reqheight() > max_reqheight:
            #max_reqheight = btn.winfo_reqheight()
      
      #TODO: check this works independently if the buttons contain text or images  
      #for button in self.buttonsList:
      #   button.config(height=max_reqheight/10) #so all buttons are of the same height

#   def changeDemo(self, event):
#      print 'Event triggered. changeDemo'

#      pathdemo = net_ROS.getDemoPath()
#      self.initDemo(pathdemo)
#      self.resetGUI()


   def resetGUI(self):
      print 'resetGUI'
      self.question.set(self.config['WELCOMEMSG'])
      
      if (self.config.get('GRAMMAR') != None):
         grammar = "[LOAD_GRAMMAR]" + self.config['GRAMMAR'] +"\n"
         net_speech.sendMessage(grammar)

      global profile
      if (self.config.get('PROFILE') != None):
         profile = parseProfile(self.config['PROFILE'])

      #reset frames
      if (self.config.get('MULTILANG') == 'YES'):
         self.profileframe.destroy()
      self.topframe.destroy()
      self.middleframe.destroy()
      self.bottomframe.destroy()
      
      self.initUI()


   def resetGUICallback(self, event):
      print 'Event triggered. resetGUI'
      self.resetGUI()

   def quit(self):
      #self.thread_stop.set()
      print "Quit. Please wait..."
      time.sleep(5)
      net_ROS.closeConnection()
      net_speech.closeConnection()
      pass

# global variables used in Tk
net_speech = Network(SPEECH_SERVER_TCP_IP, SPEECH_SERVER_TCP_PORT)
net_ROS = Network(ROS_SERVER_TCP_IP, ROS_SERVER_TCP_PORT)

def main():
   root = tk.Tk()
   f = GUI(root)
   screen_resolution = str(screen_width)+'x'+str(screen_height)    
   root.geometry(screen_resolution+"+0+0")
   root.configure(background='white')
   root.mainloop()
   f.quit()

if __name__ == '__main__':
   main()
