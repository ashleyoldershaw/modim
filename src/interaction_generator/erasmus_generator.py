import re
from translate import Translator

#Testing the availability of internet connection


# # Old world vocabulary
# # world = {'africa','america','asia','europe'}
# # africa ={'af1':'Algeria','af2':'Egypt','af3':'Ghana','af4':'Sudan','af5':'Tunisia','af6':'Zambia'}
# # america ={'am1':'Argentina','am2':'Bolivia','am3':'Brazil','am4':'Ecuador','am5':'Mexico','am6':'Peru','am7':'Trinidad_and_Tobago','am8':'United_States','am9':'Venezuela'}
# # asia ={'as1':'Azerbaijan','as2':'Bangladesh','as3':'China','as4':'India','as5':'Indonesia','as6':'Iran','as7':'Iraq','as8':'Kazakhstan','as9':'Pakistan','as10':'Russia','as11':'Syria','as12':'Turkey','as13':'Vietnam'}
# # europe ={'eu1':'Estonia','eu2':'France','eu3':'Germany','eu4':'Greece','eu5':'Montenegro','eu6':'Portugal','eu7':'Spain','eu8':'United_Kingdom'}
# #  
# 
# #Creation of a vocabulary for world
world = {'africa':['Algeria','Egypt','Ghana','Sudan','Tunisia','Zambia'],
'america':['Argentina','Bolivia','Brazil','Ecuador','Mexico','Peru','Trinidad_and_Tobago','United_States','Venezuela'],
'asia':['Azerbaijan','Bangladesh','China','India','Indonesia','Iran','Iraq','Kazakhstan','Pakistan','Russia','Syria','Turkey','Vietnam'],
'europe':['Estonia','France','Germany','Greece','Montenegro','Portugal','Spain','United_Kingdom']
}

#Creation of a function for the translation in italian, french, spanish
def tradWorld(untraslated):
    line_to_lang = ["en","it","fr","es"]
    d = {}
    for ltl in line_to_lang:
        d[ltl] = Translator(to_lang=ltl).translate(untraslated).encode('utf-8')
    return d

#Function that generate the file text_whichcontinent
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
     

#Function that generate the files text_whichcountry_Continent
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
            sentence1=('I have found this nice image of ') +country.replace('_', ' ') # we can think of randomly read/choose a sentence from a file or a list of sentences
            for ltl, trad in tradWorld(sentence1.encode('utf-8')).items(): #  ENCODING TO BE VERIFIED
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
          
