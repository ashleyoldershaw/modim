import os.path
import sys

#this simple converter assumes old demo text_files written following the same structure: text, buttons, asrcmd
#with new format all sections must finish with the caracters '----'

#actionlist = ['bear', 'bird', 'black', 'blue', 'cat', 'dog', 'dolphin',
#              'green', 'horse', 'orange', 'red', 'white', 'yellow', 'animal',
#              'color', 'goodbye', 'welcome']


def generateFiles(actionlist):

    for action in actionlist:   
        actionfile = open(action, 'w')

        if os.path.isfile('text_'+action):
            textactionfile = open('text_'+action, 'r')
            actionfile.write("TEXT\n")
            lastline = '0'
            for line in textactionfile:
                if len(line) > 0 and line[0] != '#' and line[0] != '\n':
                    if line == "BUTTONS" or line == "ASRCMD":
                        actionfile.write("----\n")
                    actionfile.write(line)
                    lastline = line
            if lastline[0] != '-':
                actionfile.write("----\n")
        if os.path.isfile('image_'+action):
            imageactionfile = open('image_'+action, 'r')
            actionfile.write("IMAGE\n")
            lastline = '0'
            for line in imageactionfile:
                if len(line) > 0 and line[0] != '#' and line[0] != '\n':
                    actionfile.write(line)
                    lastline = line
            if lastline[0] != '-':
                actionfile.write("----\n")
        actionfile.close()

    


def main():
    if len(sys.argv) != 2:
        print "Provide a file containing the list of actions, one action per line"
        return

    print "openning", sys.argv[1]
    try:
        actionsfile = open(sys.argv[1], 'r')
    except:
        print "could not open", sys.argv[1]
        exit()
        
    actionlist = []
    for line in actionsfile:
        action = line.strip()
        if os.path.isfile('text_'+action) or os.path.isfile('image_'+action):
            actionlist.append(action)
        else:
            print "Action ", action, " not found"

    generateFiles(actionlist)

if __name__ == "__main__":
    main()
