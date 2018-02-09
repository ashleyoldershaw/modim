
import sys
sys.path.append('../action')

import os
from actionReader import *
from actionWriter import ActionWriter
from profileMatcher import ProfileMatcher
  
class InteractionManager:
    def __init__(self):
        self.profile =  ['*', '*', '*', '*']
        self.path = '.'
        
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
        

    def executeModality(self, modality, interaction):
        if modality == 'TEXT':
            print 'display_text('+str(interaction)+')'
        elif modality == 'IMAGE':
            print 'display_image('+interaction+')'
        elif modality == 'BUTTONS':
            print 'display_buttons('+str(interaction)+')'
        elif modality == 'ASRCMD':
            print 'send_command_speech('+interaction+')'
        elif modality == 'GESTURE':
            print 'run_animation('+interaction+')'
