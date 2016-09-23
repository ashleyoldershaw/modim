import os
import glob
import sys
from os.path import basename, splitext

def createWorld():
    with open('final/topic/world.py', 'w') as f:
        with open('final/topic/world.txt', 'r') as t:
            for cont in t:
                pass
                f.write(cont)

from world import *

