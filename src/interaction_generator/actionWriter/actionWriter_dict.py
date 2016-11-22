#!/usr/bin/python

class ActionWriter:
	def __init__(self, actionFile, action):
		self.actionFile = actionFile
		self.action = action
	
	def writeTextSection(self): #RENAME IT AS RULE
	#E.g. texts = ((profile1, text1), (profile2, text2), ...)
		for text1,text2 in self.action['TEXTS'].items():
			self.actionFile.write(text1+text2+'\n')
	
	def writeButton(self,button_key):
	#E.g. button = ('topic', buttonInstance1, buttonInstance2, ...)
	#E.g. buttong = ('green', buttong_en, buttong_es)
	#Output: green
	#        <*,*,*,*>: Green
	#	 <*,*,es,*>: Verde
		for but_topic,but_profiles in button_key:
			self.actionFile.write(but_topic+'\n')
			for profile_es,profile_en in but_profiles.items():
				self.actionFile.write(str(profile_es)+str(profile_en)+'\n')
	
	def writeButtonsSection(self): #TUTTI I BOTTONI
	#E.g. buttons = (buttong, buttonr, ...)
	#Output: complete buttons section
		self.actionFile.write('----\n')
		self.actionFile.write('BUTTONS\n')
		self.writeButton(self.action['BUTTONS'].items())
	
	#def writeRule(self):
	#E.g. rule = (profile, text)
	
	#def writeRules(self):
	#E.g. rules = ((profile1, text1), (profile2, text2), ...)
	
	def writeGrammarSection(self):
	#E.g. grammars = ((profile1, grammar1), (profile2, grammar2), ...)
		self.actionFile.write('----\n')
		self.actionFile.write('ASRCMD\n')
		for gram1,gram2 in self.action['GRAMMARS'].items():
			self.actionFile.write(gram1+gram2+'\n')
	
	def writeImageSection(self):
		for img1,img2 in self.action['IMAGES'].items():
			self.actionFile.write(img1+img2+'\n')