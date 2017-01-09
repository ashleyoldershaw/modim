ActionWriter folder contains the tool for generating the "action" files.

ActionWriter.py contains the class "ActionWriter" that defines the procedure of generation of "text_" and "image_" action files.
These files are generated if, at least, one of their sections is defined by "action" in the testActionWriter.py file.

testActionWriter.py contains the definition of the action from which the action files will be generated.
The following is an example of its structure:

action = {
'NAME': 'whichcolor',
'TEXTS': (('<*,*,es,*>','¿Cuál es tu color preferido?'), ('<*,*,*,*>','What is your favourite color?')),
'BUTTONS': (('green', ('<*,*,es,*>','Verde'),('<*,*,*,*>','Green')), ('blue', ('<*,*,es,*>','Azul'),('<*,*,*,*>','Blue')), ('red', ('<*,*,es,*>','Rojo'),('<*,*,*,*>','Red')), ('yellow', ('<*,*,es,*>','Amarillo'),('<*,*,*,*>','Yellow')), ('orange', ('<*,*,es,*>','Naranja'),('<*,*,*,*>','Orange')), ('white', ('<*,*,es,*>','Blanco'),('<*,*,*,*>','White')), ('black', ('<*,*,es,*>','Negro'),('<*,*,*,*>','Black'))),
'GRAMMARS': (('<*,*,es,*>','[LOAD_GRAMMAR] frame_colornames|es'),('<*,*,*,*>','[LOAD_GRAMMAR] frame_colornames')),
'IMAGES': (('<*,*,es,*>','img/color_es.png'), ('<*,*,*,*>','img/color_en.png'))
}

where 'NAME' is the action name and will be the suffix of the "text_/image_" files.
"TEXTS", "BUTTONS" and "GRAMMARS" are sections for "text_" file; "IMAGES" is the "image_" file section.
Moreover, inside testActionWriter.py is possible to define the output folder of the generated action files.



