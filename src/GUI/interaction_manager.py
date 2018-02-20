
import sys
sys.path.append('../action')

import os
from actionReader import *
from actionWriter import ActionWriter
from profileMatcher import ProfileMatcher


class InteractionManager:
    def __init__(self, display):
        self.profile =  ['*', '*', '*', '*']
        self.path = '.'
        self.config = []
        self.display = display
        
    def setProfile(self, profile):
        self.profile = profile

    def setPath(self, path):
        self.path = path

    def getActionFilename(self, actionname):
        actionFullPath = os.path.join(self.path, "actions/"+actionname)
        return actionFullPath

    def init(self):
        initFilename = os.path.join(self.path, "init")
        self.config = ActionReader(initFilename)
        print self.config
        
    def execute(self, actionname):
        actionFilename = self.getActionFilename(actionname)

        action = ActionReader(actionFilename)
        pm = ProfileMatcher(action, self.profile)

        for key in action:
            if key == 'NAME':
                continue
            print key
            actual_interaction = pm.evalSection(key)
            print actual_interaction
            self.executeModality(key, actual_interaction)
        

    def ask(self, actionname):
        self.execute(actionname)
        if self.display != None:
            a = self.display.answer()
            self.display.remove_buttons()
            if (a is not None):
                a = a.rstrip()
            return a


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

if __name__ == "__main__":
    pass


