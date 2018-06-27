
import sys
sys.path.append('../action')

import os
from actionReader import *
from actionWriter import ActionWriter
from profileMatcher import ProfileMatcher

import threading

languages = {"en" : "English", "it": "Italian"}


def printError(message):
    RED   = "\033[1;31m"  
    RESET = "\033[0;0m"
    print("%s%s%s" %(RED,message,RESET))


class InteractionManager:
    def __init__(self, display, robot):
        self.profile =  ['*', '*', '*', '*']
        self.path = '.'
        self.config = []
        self.display = display
        self.robot = robot
        self.saytime = {}
        self.demoIP = '127.0.0.1' # web server containing the demo
        self.demoPort = 8000      # web server containing the demo

    def setProfile(self, profile):
        self.profile = profile
        if (self.robot!=None):
            print "Setting language to: ", languages[self.profile[2]]
            self.robot.setLanguage(languages[self.profile[2]])

    def setPath(self, path):
        self.path = path

    def setDemoServer(self, demoIP, demoPort):
        self.demoIP = demoIP
        self.demoPort = demoPort

    def getActionFilename(self, actionname):
        actionFullPath = os.path.join(self.path, "actions/"+actionname)
        return actionFullPath

    def getGrammarFilename(self, grammarname):
        grammarFullPath = os.path.join(self.path, "grammars/"+grammarname)
        return grammarFullPath
    
    def getGrammarURL(self, grammarname):
        url = 'http://%s:%d/grammars/%s' %(self.demoIP,self.demoPort,grammarname)
        return url

    def init(self):
        initFilename = os.path.join(self.path, "init")
        self.config = ActionReader(initFilename, self.demoIP, self.demoPort)

        if "PROFILE" in self.config:
            self.setProfile(parseProfile(self.config["PROFILE"]))

        for key in self.config:
            if key != "PROFILE" and key != "MULTILANG":
                self.executeModality(key, self.config[key])
                
        print self.config

    # returns the list of conditions in an action
    def listConditions(self, actionname):
        actionFilename = self.getActionFilename(actionname)
        action = ActionReader(actionFilename, self.demoIP, self.demoPort)
        pm = ProfileMatcher(action, self.profile)
        r = pm.listConditions()
        self.display.setReturnValue(r)
        return r         
        
    def execute(self, actionname):
        actionFilename = self.getActionFilename(actionname)
        action = ActionReader(actionFilename, self.demoIP, self.demoPort)
        pm = ProfileMatcher(action, self.profile)

        threads = [] #for parallel execution of the modalities
        for key in action:
            if key == 'NAME':
                continue
            actual_interaction = pm.evalSection(key)
            if (len(actual_interaction) == 0):
                continue
            #self.executeModality(key, actual_interaction)
            t = threading.Thread(target=self.executeModality, args=(key, actual_interaction))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def ask(self, actionname):
        self.execute(actionname)
        if self.display != None:
            a = self.display.answer()
            self.display.remove_buttons()
            if (a is not None):
                a = a.rstrip()
            return a


    def encode(self, interaction):
        l = min(10,len(interaction))
        return interaction[0:l]

    def executeModality(self, modality, interaction):
        if modality.startswith('TEXT'):
            vmod = modality.split('_')
            place = 'default'
            if (len(vmod)>1):
                place = vmod[1]
            print 'display_text('+str(interaction)+','+place+')'
            if self.display != None:
                self.display.display_text(interaction, place)

        elif modality.startswith('IMAGE'):
            vmod = modality.split('_')
            place = 'default'
            if (len(vmod)>1):
                place = vmod[1]

            # interaction =  os.path.join(self.path, interaction)
            print 'display_image('+str(interaction)+','+place+')'
            if self.display != None:
                self.display.display_image(interaction, place)

        elif modality == 'BUTTONS':
            print 'display_buttons('+str(interaction)+')'
            if self.display != None:
                self.display.display_buttons(interaction)

        elif modality == 'ASRCMD':
            grammarFile = None
            # try reading from file
            try:
                grammarFilename = self.getGrammarFilename(interaction)
                print 'Reading grammar file', grammarFilename
                grammarFile = open(grammarFilename, 'rU')
            except IOError:
                print "Cannot open grammar file", grammarFile

            if grammarFile==None:
                # try reading from URL
                try:
                    grammarURL = self.getGrammarURL(interaction)
                    print 'Reading grammar URL ', grammarURL
                    grammarFile = urllib2.urlopen(grammarURL)
                except:
                    print "Cannot open grammar URL", grammarURL


            if grammarFile==None:
                return

            inv_grammar = dict()
            grammar = dict()
            vocabulary = []
            for line in grammarFile.readlines():
                print 'grammar file: ',line
                try:
                    s = line.split('->')
                    words = s[0].strip().split(',')
                    words = map(str.strip, words) #removes spaces on all elements
                    key = s[1].strip()
                    grammar[key] = words
                    vocabulary.extend(words)
                    for w in words:
                        inv_grammar[w] = key
                except:
                    printError("Error in reading grammar file")

            if (self.robot!=None):
                self.robot.asr(vocabulary) # TODO check
                        

        elif modality == 'GESTURE':
            print 'run_animation('+interaction+')'
            if (self.robot != None):
                self.robot.animation(interaction)

        elif modality == "TTS":
            cod = self.encode(interaction)
            if (not cod in self.saytime):
                #self.saytime[cod]=1
                print 'say('+interaction+')'            
                if (self.robot != None):
                    self.robot.say(interaction)

        print "Finished executeModality("+modality+","+str(interaction)+")\n"

if __name__ == "__main__":
    pass


