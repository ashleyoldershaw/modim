#http://www.nationsonline.org/flags/armenia_flag.gif
# nation = 'china'
# testfile = urllib.URLopener()
# testfile.retrieve('http://www.nationsonline.org/flags/'+nation+'_flag.gif', nation+'_flag_small.gif')
import os
import urllib
import urlparse

def download():
    with open('world.py', 'w') as f:
        with open('world.txt', 'r') as t:
            for cont in t:
                pass
                f.write(cont)

from world import *


    
os.chdir('final/img/') 
for continent in world:
         for country in continent:
              
 # This will download the all the flags of all countries 
             try:
                 testfile = urllib.URLopener()
                 testfile.retrieve('http://www.nationsonline.org/flags_big/'+country+'_lgflag.gif', country+'_flag_big.gif') 
             except:
                 testfile.retrieve('http://www.nationsonline.org/flags_big/'+country+'_lgflag.jpg', country+'_flag_big.gif')
                 #print('flags downloaded in img folder')
