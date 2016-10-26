#!/usr/bin/python
import urllib, urllib2
import time
import os


#Testing the availability of internet connection
try :
    url = "https://www.google.com"
    urllib.urlopen(url)
    print("Connected")
except :
    print("Not connect")
    quit()
    
start_time = time.time()

folder = ['actions','img']

for x in folder:
    if not os.path.exists(x):
        os.makedirs(x)

import erasmus_generator
# This part download flag images of countries
import downloads

print("--- %s seconds ---" % (time.time() - start_time))