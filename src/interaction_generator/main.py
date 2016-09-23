import io
import os
import glob
import sys
from os.path import basename, splitext

#Creation of a python file from a text file with variable we are going to use
with open('world.py', 'w') as f:
        with open('world.txt', 'r') as t:
            for cont in t:
                pass
                f.write(cont)

from world import * #import of the variables
from itertools import islice

# ----- Generation of WHICHCONTINENT file ----- small changes to be language sensitive
with open('final/prova/text_whichcontinent', 'w') as answer:
        with open('final/topic/continent.txt', 'r') as f:
            for line in islice(f, 0, 2):
                l , r = line.rstrip('\r\n').split('->')
                r = r.strip()
                answer.write('<*, *, '+l+', *>: '+r+'\n')
            answer.write('----\n')
            answer.write('BUTTONS\n')
            lcont = 'continent_'
              
            for list_cont in cont:
                    list_cont = str(list_cont)
                    answer.write(lcont+list_cont+'\n')
                    answer.write('<*, *, es, *>: '+list_cont+'\n'+'<*, *,'+l+', *>: '+list_cont+'\n')
                    
            answer.write('----\n')

# This part generate TEXT_WHICHCOUNTRY_CONTINENT
for list_cont in cont:
    with open('final/prova/text_whichcountry_'+list_cont, 'w') as answer:
        with open('final/topic/country.txt', 'r') as f:
            for line in islice(f, 0, 2):
                l , r = line.rstrip('\r\n').split('->')
                r = r.strip()
                answer.write('<*, *, '+l+', *>: '+r+'\n')
            answer.write('----\n')
            answer.write('BUTTONS\n')
            lcountry = 'country_'
            
# -------- need to revise generation of buttons-flag -------

# This part generate IMG_COUNTRY --- NB: needs to handle '_' exception as "United_State" 
for pais in world:
     for list_count in pais:   
#         if '_' in list_count:
#                     j1=list_count.rfind('_')
#                     j2=list_count[:j1]+ list_count[j1+1:]
#                     exc_count =str(j2)         
                    with open('final/prova/image_'+list_count, 'a') as answer:
                        #with open('final/topic/image_'+list_count, 'r') as f:
                # answer.write('<*, *, *, *>: img/'+list_count+'.jpg\n')
                            list_count = str(list_count)
                            answer.write('<*, *, *, *>: img/'+list_count+'.jpg\n')
#         else:
#                     with open('final/prova/image_'+list_count, 'r+') as answer:
#                        with open('final/topic/'+list_count, 'r') as f:
#                             answer.write('<*, *, *, *>: img/'+list_count+'.jpg\n')         
                 #answer.write('----\n')

# This part generate TEXT_COUNTRY  --- NB: needs to handle '_' exception as "United_State" 
for pais in world:
      for list_count in pais: 
        with open('final/sentence_country/text_'+list_count, 'w') as answer:
         with open('final/topic/country_finalSentence.txt', 'r') as f:
            for line in islice(f, 0, 2):
                l , r = line.rstrip('\r\n').split('->')
                r = r.strip()
                answer.write('<*, *, '+l+', *>: '+r+' '+list_count+'\n')

# This part download flag images of countries
from download import download 