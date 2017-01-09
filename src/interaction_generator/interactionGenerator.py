#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from interaction_file import *
#import interaction_file
from interactionFiles import interactionGenerator
import interactionFiles as iaf
####### CHOOSE THE INTERACTION YOU WANT TO GENERATE #######

#available_interactions = entertainment(),activity(),quiz_country(),quiz_football(),

## Define path where to generate the files
destination_path = 'quiz/'
interactionGenerator(iaf.quiz_Country(),destination_path)