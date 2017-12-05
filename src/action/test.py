from actionReader import ActionReader
from actionWriter import ActionWriter


action = ActionReader("test")
ActionWriter(action, "testwrite")
action = ActionReader("testwrite")
