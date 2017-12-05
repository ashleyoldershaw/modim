

class ActionWriter():
    def __init__(self, action, actionFilename = ""):
	
	self.action = action
        if actionFilename == "":
            self.actionFile = open(self.action['NAME'], 'w')
        else:
            self.actionFile = open(actionFilename, 'w')

        self.writeActionFile()
        self.actionFile.close()

    def writeActionFile(self):
        print 	self.action

        for key in self.action.keys():
            if key != "NAME":
                self.writeSectionRules(key)

        
    def writeSectionRules(self, sectionType):
        #start section
        self.actionFile.write(sectionType+'\n')
        #rules
        if (sectionType == "BUTTONS"):
            for button in self.action["BUTTONS"]:
                if len(button) != 2:
                    continue
                
                self.actionFile.write(button[0]+'\n')
                rulesButton = button[1]
                for rule in rulesButton:
                    self.writeRule(rule)    
        else:
            for rule in self.action[sectionType]:
                self.writeRule(rule)
            
        #end section            
        self.actionFile.write('----\n')
            
            

    def writeRule(self, rule):
        if len(rule) != 2:
            return 
        profile = rule[0]
        content = rule[1]
        self.writeProfile(profile)
        self.actionFile.write(': ')
        self.writeContent(content)
        self.actionFile.write('\n')
        
        
    def writeProfile(self, profile):
	self.actionFile.write('<')
        sizeProfile = len(profile)
        i = 1
        for item in profile:
	    self.actionFile.write(item)
            if i < sizeProfile:
                self.actionFile.write(',')
            i = i+1
            
	self.actionFile.write('>')
        
    def writeContent(self, content):
        self.actionFile.write(content)
