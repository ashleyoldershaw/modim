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


#2) image_ file will have section image (if present in 'action')







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
