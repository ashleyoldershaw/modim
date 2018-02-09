
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
        self.display = display
        
    def setProfile(self, profile):
        self.profile = profile

    def setPath(self, path):
        self.path = path

    def getActionFilename(self, actionname):
        actionFullPath = os.path.join(self.path, "actions/"+actionname)
        return actionFullPath
    
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
        a = self.display.answer()
        self.display.remove_buttons()
        if (a is not None):
            a = a.rstrip()
        return a


    def executeModality(self, modality, interaction):
        if modality == 'TEXT':
            print 'display_text('+str(interaction)+')'
            self.display.display_text(interaction)

        elif modality == 'IMAGE':
            print 'display_image('+interaction+')'
            self.display.display_image(interaction)

        elif modality == 'BUTTONS':
            print 'display_buttons('+str(interaction)+')'
            self.display.display_buttons(interaction)

        elif modality == 'ASRCMD':
            print 'send_command_speech('+interaction+')'

        elif modality == 'GESTURE':
            print 'run_animation('+interaction+')'

if __name__ == "__main__":
    pass

