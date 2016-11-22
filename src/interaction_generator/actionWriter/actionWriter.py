#!/usr/bin/python

class ActionWriter():
	
	def __init__(self,action):
		
		self.action = action
		
		
 	def writeAction(self, actionFile):
  		if 'IMAGES' in self.action.keys():
  			self.actionFile = open(actionFile+'img_'+self.action['NAME']+'.txt', 'w')
 		 	self.writeImageSection()
 			self.actionFile.close()

		dict_keys, section_key = set(self.action.keys()), ['TEXTS','BUTTONS','GRAMMARS']
		print 'keys of your action is the '+str(dict_keys)
		if [item for item in section_key if item in dict_keys]:
			print 'text_'+str(self.action['NAME'])+' will have these sections'+str([item for item in section_key if item in dict_keys])
			self.actionFile = open(actionFile+'text_'+self.action['NAME']+'.txt', 'w')
			self.writeTextSection()
			self.writeButtonsSection()
			self.writeGrammarSection()
			self.actionFile.close()
			
	def writeRule(self,param):
		profile,text = param
		print param
		self.actionFile.write(profile+': '+text+'\n')
		
	def writeRuleSection(self,section):
		print section
		for item in section:
			print item
			self.writeRule(item)

	def writeImageSection(self):
		self.writeRuleSection(self.action['IMAGES'])

 	def writeTextSection(self):
 		#E.g. texts = ((profile1, text1), (profile2, text2), ...)
		if 'TEXTS' in self.action.keys():
			self.writeRuleSection(self.action['TEXTS'])
		else:
			pass

	def writeButton(self,button_value):
		#E.g. button = ('topic', buttonInstance1, buttonInstance2, ...)
		#E.g. buttong = ('green', buttong_en, buttong_es)
		#Output: green
		#        <*,*,*,*>: Green
		#	 <*,*,es,*>: Verde
		topic,text = button_value[0], button_value[1:]
		self.actionFile.write(topic+'\n')
		for text1,text2 in text:
			self.actionFile.write(text1+': '+text2+'\n')
			
	def writeButtonsSection(self):
		#E.g. buttons = (buttong, buttonr, ...)
		#Output: complete buttons section
		self.actionFile.write('----\n')
		if 'BUTTONS' in self.action.keys():
			self.actionFile.write('BUTTONS\n')
			for button in self.action['BUTTONS']:
				self.writeButton(button)

	def writeGrammarSection(self):
		#E.g. grammars = ((profile1, grammar1), (profile2, grammar2), ...)
		self.actionFile.write('----\n')
		if 'GRAMMARS' in self.action.keys():
			self.actionFile.write('ASRCMD\n')
			self.writeRuleSection(self.action['GRAMMARS'])
		else:
			pass
	
	