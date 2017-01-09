import re
from translate import Translator

# #Creation of a vocabulary for world
world = {'africa':['Algeria','Egypt','Ghana','Sudan','Tunisia','Zambia'],
'america':['Argentina','Bolivia','Brazil','Ecuador','Mexico','Peru','Trinidad_and_Tobago','United_States','Venezuela'],
'asia':['Azerbaijan','Bangladesh','China','India','Indonesia','Iran','Iraq','Kazakhstan','Pakistan','Russia','Syria','Turkey','Vietnam'],
'europe':['Estonia','France','Germany','Greece','Montenegro','Portugal','Spain','United_Kingdom']
}

#Function for online translation to italian, french, spanish
def tradWorld(untraslated):
    line_to_lang = ["en","it","fr","es"]
    d = {}
    for ltl in line_to_lang:
        d[ltl] = Translator(to_lang=ltl).translate(untraslated).encode('utf-8')
    return d

#Function for generating file text_whichcontinent
def generateContinent(questContinent):
    namefile = 'actions/text_whichcontinent'
    with open(namefile, 'w') as the_file:
        for ltl, trad in tradWorld(questContinent).items():
            the_file.write('<*, *,'+ltl+', *>: '+trad+'\n')
        the_file.write('----\n')
        the_file.write('BUTTONS\n')
        for continent in world.keys():
            the_file.write('continent_' + continent + '\n')
            for ltl, trad in tradWorld(continent).items():
                the_file.write('<*, *,'+ltl+', *>:'+re.sub('[,.]','',trad.capitalize())+' \n')
        the_file.write('----\n')
    #whichcontinent.close()
     

#Function for generating file text_whichcountry_Continent
def generateCountry(questCountry):
    for continent in world:
        namefile = 'actions/text_whichcountry_'+continent
        with open(namefile, 'w') as the_file:
            for ltl, trad in tradWorld(questCountry).items():
                the_file.write('<*, *,'+ltl+', *>: '+trad+'\n')
            the_file.write('----\n')
            the_file.write('BUTTONS\n')
             
            for country in world[continent]:
                co1 = re.sub('[_]', '', country)
                #co1 = country.replace('_', '')
                the_file.write('country_' + co1 + '\n')
                the_file.write('img/' + country + '_flag_big.gif\n')            
            the_file.write('----\n')
        #whichcontinent.close()
 

for continent in world.values():
    for country in continent:
        co1 = country.replace('_', '')
        #Generation of file text_"country"
        namefile = 'actions/text_'+ co1
        with open(namefile, 'w') as the_file:
            #co1 = re.sub('[_]', ' ', country)
            sentence1=('I have found this nice image of ') +country.replace('_', ' ')
            for ltl, trad in tradWorld(sentence1.encode('utf-8')).items():
                the_file.write('<*, *,'+ltl+', *>: '+trad+'\n')           
        #the_file.write('----\n')
     
        #Generation of file img_"country"
        namefile = 'actions/image_'+ co1
        with open(namefile, 'w') as the_file:
            the_file.write('<*, *, *, *>: img/' + co1 +'.jpg\n') 
        #the_file.write('----\n')

whichcontinent = open('topic/whichcontinent.txt', 'r')
generateContinent(whichcontinent.readline())
whichcountry = open('topic/whichcountry.txt', 'r')
generateCountry(whichcountry.readline())
          
