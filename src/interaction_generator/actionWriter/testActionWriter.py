from actionWriter import ActionWriter
import glob
import os



action = {
'NAME': 'whichcolor',
'TEXTS': (('<*,*,es,*>','¿Cuál es tu color preferido?'), ('<*,*,*,*>','What is your favourite color?')),
'BUTTONS': (('green', ('<*,*,es,*>','Verde'),('<*,*,*,*>','Green')), ('blue', ('<*,*,es,*>','Azul'),('<*,*,*,*>','Blue')), ('red', ('<*,*,es,*>','Rojo'),('<*,*,*,*>','Red')), ('yellow', ('<*,*,es,*>','Amarillo'),('<*,*,*,*>','Yellow')), ('orange', ('<*,*,es,*>','Naranja'),('<*,*,*,*>','Orange')), ('white', ('<*,*,es,*>','Blanco'),('<*,*,*,*>','White')), ('black', ('<*,*,es,*>','Negro'),('<*,*,*,*>','Black'))),
'GRAMMARS': (('<*,*,es,*>','[LOAD_GRAMMAR] frame_colornames|es'),('<*,*,*,*>','[LOAD_GRAMMAR] frame_colornames')),
'IMAGES': (('<*,*,es,*>','img/color_es.png'), ('<*,*,*,*>','img/color_en.png'))
}


#Test program for class ActionWriter
#Given action defined above
#Write the corresponding text_ and image_ files

#1) text_ file will have sections texts, buttons and grammars (if present in 'action')
#CHIAMARE LE FUNZIONE DELLA CLASSE ACTIONWRITER

#2) image_ file will have section image (if present in 'action')

my_action = {
    'NAME': 'whichcolor',
    'TEXTS': {'<*,*,es,*> ':'\xc2\xbfCual es tu color preferido?','<*,*,*,*> ':'What is your favourite color?'},
    'BUTTONS': {'green':{'<*,*,es,*> ':'Verde','<*,*,*,*> ':'Green'}, 'blue':{'<*,*,es,*> ':'Azul','<*,*,*,*> ':'Blue'},'red':{'<*,*,es,*> ':'Rojo','<*,*,*,*> ':'Red'},'yellow':{'<*,*,es,*> ':'Amarillo','<*,*,*,*> ':'Yellow'},'orange':{'<*,*,es,*> ':'Naranja','<*,*,*,*> ':'Orange'},'white':{'<*,*,es,*> ':'Blanco','<*,*,*,*> ':'White'},'black':{'<*,*,es,*> ':'Negro','<*,*,*,*> ':'Black'}},
    'GRAMMARS': {'<*,*,es,*> ':'[LOAD_GRAMMAR] frame_colornames|es','<*,*,*,*> ':'[LOAD_GRAMMAR] frame_colornames'},
    'IMAGES': {'<*,*,es,*> ':'img/color_es.png','<*,*,*,*> ':'img/color_en.png'}
    }


path_write = 'file/'
name_file = my_action['NAME']
prefix_name = ['text_','img_']


for prefix in prefix_name:
    with open(path_write+prefix+name_file, 'w') as written_file:
    # Calling/Instantiation of the class 
        writerAct = ActionWriter(written_file,my_action)
        
        if prefix == 'text_':
    
            writerAct.writeTextSection()
            writerAct.writeButtonsSection()
            #writerAct.writeButton(my_action['BUTTONS'].items())
            writerAct.writeGrammarSection()
#    
#     
#             #writerAct.writeRules()
            
        if prefix =='img_':
            writerAct.writeImageSection()
            
        
            
    written_file.close()





#Expected result for text_whichcolor:
#<*,*,es,*>: "¿Cuál es tu color preferido?"
#<*,*,*,*>:  "What is your favourite color?"
#----
#BUTTONS
#green
#<*,*,es,*>: Verde
#<*,*,*,*>:  Green
#blue
#<*,*,es,*>: Azul
#<*,*,*,*>:  Blue
#red
#<*,*,es,*>: Rojo
#<*,*,*,*>:  Red
#yellow
#<*,*,es,*>: Amarillo
#<*,*,*,*>:  Yellow
#orange
#<*,*,es,*>: Naranja
#<*,*,*,*>:  Orange
#white
#<*,*,es,*>: Blanco
#<*,*,*,*>:  White
#black
#<*,*,es,*>: Negro
#<*,*,*,*>:  Black
#----
#ASRCMD 
#<*,*,es,*>: [LOAD_GRAMMAR] frame_colornames|es
#<*,*,*,*>:  [LOAD_GRAMMAR] frame_colornames
