
import sys
sys.path.append('../action')

import os
from actionReader import *
from actionWriter import ActionWriter
from profileMatcher import ProfileMatcher

import threading

languages = {"en" : "English", "it": "Italian"}

class InteractionManager:
    def __init__(self, display, robot):
        self.profile =  ['*', '*', '*', '*']
        self.path = '.'
        self.config = []
        self.display = display
        self.robot = robot
        self.saytime = {}
        
    def setProfile(self, profile):
        self.profile = profile
        if (self.robot!=None):
            print "Setting language to: ", languages[self.profile[2]]
            self.robot.setLanguage(languages[self.profile[2]])

    def setPath(self, path):
        self.path = path

    def getActionFilename(self, actionname):
        actionFullPath = os.path.join(self.path, "actions/"+actionname)
        return actionFullPath

    def init(self):
        initFilename = os.path.join(self.path, "init")
        self.config = ActionReader(initFilename)

        if "PROFILE" in self.config:
            self.setProfile(parseProfile(self.config["PROFILE"]))

        for key in self.config:
            if key != "PROFILE" and key != "MULTILANG":
                self.executeModality(key, self.config[key])
                
        print self.config
        
    def execute(self, actionname):
        actionFilename = self.getActionFilename(actionname)

        action = ActionReader(actionFilename)
        pm = ProfileMatcher(action, self.profile)

        threads = [] #for parallel execution of the modalities
        for key in action:
            if key == 'NAME':
                continue
            actual_interaction = pm.evalSection(key)
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

            interaction =  os.path.join(self.path, interaction)
            print 'display_image('+str(interaction)+','+place+')'
            if self.display != None:
                self.display.display_image(interaction, place)

        elif modality == 'BUTTONS':
            print 'display_buttons('+str(interaction)+')'
            if self.display != None:
                self.display.display_buttons(interaction)

        elif modality == 'ASRCMD':
            print 'send_command_speech('+interaction+')'

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


