import os
import urllib2
import rospy

def parseProfile(profile):
    parsedProfile = profile.lstrip('<').rstrip('> ')
    parsedProfile = parsedProfile.replace(" ","").split(',')
    return parsedProfile

def parseContent(content):
    #removes unncessary spaces and the text quotes (")
    parsedContent = content.replace("\"","").strip(" \t\n")
    return parsedContent

class ActionReader(dict):
    def __init__(self, actionFilename, demoIP='127.0.0.1', demoPort=8000):
        self.actionFile = []
        self.actionFile = None
        # open action file from file system        
        try:
            print 'opening file', actionFilename
            self.actionFile = open(actionFilename, 'rU')
        except IOError:
            print 'cannot open file', actionFilename

        if self.actionFile==None:
            # open action file from web server
            try:
                url = 'http://%s:%d/actions/%s' %(demoIP,demoPort,os.path.basename(actionFilename))
                print 'openning url', url
                self.actionFile = urllib2.urlopen(url)
                
            except IOError:
                print 'cannot open URL', url

        if self.actionFile!=None:
            #initializing action
            self['NAME'] = os.path.basename(actionFilename)
            if self['NAME'] == 'init':
                self.parseInitActionFile()
            else:
                self.parseActionFile()

    def parseActionFile(self):
        modimVariables = {
            "CHECKPOINT":"/diago_0/pnp/checkpoint",
            "INTENDED ACTION":"/diago_0/pnp/currentTask"
        }
        sectionRules = []
        sectionType = []
        for line in self.actionFile.readlines():
            line = line.replace("\"","").strip(" \t\n")
            for item in modimVariables:
                line = line.replace("#"+item+"#", rospy.get_param(modimVariables[item]).replace("_"," "))
            print (line)
            if len(line) > 0 and line[0] != '#': #comment or empty line
                if (line.startswith("TEXT") or
                    line.startswith("IMAGE") or
                    line == "BUTTONS" or
                    line == "TTS" or
                    line == "ASRCMD" or
                    line == "GESTURE"):
                    #starting section
                    sectionType = line
                    continue
                elif (line == "----"):
                    #ending section
                    self.parseSectionRules(sectionType, sectionRules)
                    sectionRules = []
                    sectionType = []
                else:
                    sectionRules.append(line)

        print self
        
    def parseSectionRules(self, sectionType, sectionRules):
        if (sectionType.startswith("TEXT") or
            sectionType.startswith("IMAGE") or
            sectionType == "ASRCMD" or
            sectionType == "TTS" or
            sectionType == "GESTURE"):
            ruleList = []
            for rule in sectionRules:
                parsedRule = self.parseRule(rule)
                if len(rule) > 0:
                    ruleList.append(parsedRule)
            self[sectionType] = ruleList
        else: #sectionType=="BUTTONS"
            ruleList = []
            keyword = ""
            newKeyword = False
            ruleListButton = []
            self[sectionType] = []
            for rule in sectionRules:
                parsedRule = self.parseRule(rule)
                if len(parsedRule) == 0:
                    if keyword != "":
                        newKeyword = True
                    else:
                        keyword = rule
                else:
                    ruleListButton.append(parsedRule)


                if newKeyword:
                    self[sectionType].append((keyword, ruleListButton))
                    keyword = rule  #new keyword
                    newKeyword = False
                    ruleListButton = []

            if keyword != "":
                self[sectionType].append((keyword, ruleListButton))


                
    def parseRule(self, rule):
        #divides the rule in profile and some content
        parsedRule = ""
        splitRule = rule.split(':',1)
        if len(splitRule) == 2:
            profile = parseProfile(splitRule[0])
            content = parseContent(splitRule[1])
            parsedRule = (profile, content)

        return parsedRule

    def parseInitActionFile(self):
        #parses the init file
        for line in self.actionFile.readlines():
            if line[0] != '\n':
                linesplit = line.strip("\n").split(":")
                if len(linesplit) == 2:
                    sectionType = linesplit[0]
                    content = parseContent(linesplit[1])
                    self[sectionType] = content
                

