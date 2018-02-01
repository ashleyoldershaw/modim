from actionReader import ActionReader
from actionWriter import ActionWriter
from profileMatcher import ProfileMatcher

action = ActionReader("test")
ActionWriter(action, "testwrite")
action = ActionReader("testwrite")

profile = ['*', '*', 'es', '*']

pm = ProfileMatcher(action, profile)
pm.evalSection('TEXT')
pm.evalSection('BUTTONS')

profile = ['*', '*', 'it', '*']
pm.setProfile(profile)
pm.evalSection('TEXT')
print pm.evalSection('TEXT')
pm.evalSection('IMAGE')
pm.evalSection('BUTTONS')
print pm.evalSection('BUTTONS')
pm.evalSection('ASRCMD')
print pm.evalSection('ASRCMD')
