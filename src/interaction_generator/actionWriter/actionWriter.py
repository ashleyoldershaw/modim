#!/usr/bin/python
from all_function import actionWriter


path_read = 'generation_file'
path_write = 'file'

# Will be substituted by external structured data
topic = {'en':'where are you from?', 
'es':'de que pais eres?',
'it':'da dove vieni?'}


actionWriter(path_read,path_write,topic)
    