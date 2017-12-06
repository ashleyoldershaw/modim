from actionReader import ActionReader
from actionWriter import ActionWriter
from profileMatcher import ProfileMatcher

action = ActionReader("test")
ActionWriter(action, "testwrite")
action = ActionReader("testwrite")

profile = ['*', '*', 'es', '*']

pm = ProfileMatcher(action, profile)
pm.evalSection('TEXTS')
pm.evalSection('BUTTONS')

profile = ['*', '*', 'it', '*']
pm.setProfile(profile)
pm.evalSection('TEXTS')
pm.evalSection('IMAGES')


