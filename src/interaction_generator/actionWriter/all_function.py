#!/usr/bin/python
import os
from itertools import islice
import itertools
import glob
import re


value_check = ['yes','no']


class ActionWriter:
	def __init__(self, nameOfFile):
		#open file.
   		self.actionFile = open...



	def writeButton(button):
	#E.g. button = ('topic', buttonInstance1, buttonInstance2, ...)
	#E.g. buttong = ('green', buttong_en, buttong_es)
	#Output: green
  	#        <*,*,*,*>: Green
	#	 <*,*,es,*>: Verde

		self.actionFile 

	def writeButtonsSection(buttons):
	#E.g. buttons = (buttong, buttonr, ...)
	#Output: complete buttons section


	def writeInstruction(instruction):
	#E.g. instruction = (profile, text)
	
	def writeInstructions(instructions):
	#E.g. instructions = ((profile1, text1), (profile2, text2), ...)
	
	def writeGrammarSection(grammars):
	#E.g. grammars = ((profile1, grammar1), (profile2, grammar2), ...)
	
	def writeTextSection(texts):
	#E.g. texts = ((profile1, text1), (profile2, text2), ...)

	

	
def actionWriter(path_read,path_write,topic):
    # Definition of the HEAD section
    def head_function(inc):   
        if value_list[0] == value_check[0]:
            inc.write('#Format: <age, gender, language, occupation>:"Text to say"\n')
            inc.write('#age = [adult | senior | junior]\n')
            inc.write('#gender = [m | f]\n')
            inc.write('#language = [en | fr | it | sp]\n')
            inc.write('#occupation = [student | professor | visitor]\n')
            inc.write('#write character \'*\' for default option\n') 
        if value_list[0] == value_check[1]:
            print('')
            #final.write('----\n')
    #     else:
    #         print('not valid "head" value in your text file, please check it')
        if value_list[1] == value_check[0]:
            for lang,sentence in topic.items():
                final.write('<*, *, '+lang+', *>: '+sentence+'\n')
        if value_list[1] == value_check[1]:
            print('')
    
    # Definition of the BUTTON section
    def button_function(inc):
        if value_list[2] == value_check[0]:
            inc.write('----\n')
            inc.write('BUTTONS\n')
            for element,sentence in topic.items():
                inc.write('text_TO_BE_DEFINED\n')
                inc.write('<*, *, '+element+', *>: '+sentence+'\n')
            inc.write('----\n')  
        if value_list[2] == value_check[1]:
            print('')
    
    # Definition of the GRAMMAR section
    def grammar_function(inc):
        inc.write('ASRCMD\n') 
        inc.write('<*,*,*,*>: [LOAD_GRAMMAR] frame_helps\n') #next --> to make "frame" a variable  
        inc.write('----\n')
    
    for file_read in glob.glob(os.path.join(path_read, '*.txt')):
        filename = os.path.splitext(os.path.basename(file_read))[0]
        with open(file_read, 'r') as read:
            value_list=[] 
            for line in islice(read,0,3):
                l , r = line.rstrip('\r\n').split('=')
                r = r.strip()
                value_list.append(r)
            with open(path_write+'/text_'+filename+'.txt', 'w') as final:
                head_function(final)
                button_function(final)
                grammar_function(final)
                
                
