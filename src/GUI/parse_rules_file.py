import sys
import os
script_dir = os.path.dirname(__file__)

def parseProfile(str):
    profile = str.strip("\n")
    profile = profile.lstrip('<').rstrip('> ')
    profile = profile.replace(" ","").split(',')
    return profile

def parseText(str):
    #removes unncessary spaces and the text quotes (")
    text = str.replace("\"","").strip(" \t\n")
    return text

def parseRule(line):
    #divides the rule in profile and some text
    rule = ""
    myList = line.split(':',1)
    if len(myList) != 2:
        print "wrong format ... skipped"
    else:
        profile = parseProfile(myList[0])
        text_to_say = parseText(myList[1])
        rule = (profile , text_to_say)

    return rule

def parseRulesFile(file):
    print "Parsing file: %s\n" % file.name
    list_of_rules = []
    while 1:
        line = file.readline()
        if not line:
            break
        if line[0] != '#' and line[0] != '\n': #comment or empty line
            rule = parseRule(line)
            if len(rule) > 0:
                list_of_rules.append(rule)
                
    return list_of_rules

def parseRulesFileActions(file):
    #This function assumes standard actions are at the beginning of the file
    #and will finish with a "----" line
    print "Parsing file: %s\n" % file.name
    list_of_rules = []
    while 1:
        line = file.readline()
        if not line:
            break
        if line[0:4] == "----":
            break
        if line[0] != '#' and line[0] != '\n': #comment or empty line
            rule = parseRule(line)
            if len(rule) > 0:
                list_of_rules.append(rule)
            
    return list_of_rules

def parseButton(file):
    #Format to define a button:
    #keyword (= command to send to pnp)
    #list of rules
    
    keyword = ""
    list_of_rules = []
    while 1:
        currentFilePose = file.tell()
        line = file.readline()
        if not line:
            break
        if line[0:4] == "----": #end of section
            # Move the pointer back to the beginning of this line
            # so this line can be processed again later
            file.seek(currentFilePose)
            break

        if line[0] != '#' and line[0] != '\n': #comment or empty line
            if keyword == "":
                keyword = line.strip("\n") #first comes the keyword
            else:
                rule = parseRule(line)
                if len(rule) > 0:
                    list_of_rules.append(rule)
                else: #if not a proper rule we finished
                    file.seek(currentFilePose)
                    break
    
    return (keyword, list_of_rules)

def parseRulesFileButtons(file):
    #This function assumes Buttons section will start with the word BUTTONS
    #and will finish with a "----" line
    print "Parsing file: %s\n" % file.name

    in_buttons_section = False
    list_of_buttons = []
    while 1:
        currentFilePose = file.tell()
        line = file.readline()
        if not line:
            break
        if "BUTTONS" in line:
            in_buttons_section = True
            continue
        if in_buttons_section:
            if line[0:4] == "----": #end of section
                break
            if line[0] != '#' and line[0] != '\n': #comment or empty line
                file.seek(currentFilePose)
                button = parseButton(file)
                list_of_buttons.append(button)
    
    return list_of_buttons

def parseRulesFileGrammar(file):
    #This function assumes Grammar section will start with the word ASRCMD
    #and will finish with a "----" line
    print "Parsing file: %s\n" % file.name

    in_grammar_section = False
    list_of_rules = []
    while 1:
        line = file.readline()
        if not line:
            break
        if "ASRCMD" in line:
            in_grammar_section = True
            continue
        if in_grammar_section:
            if line[0:4] == "----": #end of section
                break
            if line[0] != '#' and line[0] != '\n': #comment or empty line
                 rule = parseRule(line)
                 if len(rule) > 0:
                     list_of_rules.append(rule)
    
    return list_of_rules


def look_for_best_rule(list_of_rules, profile):
    #look for more suitable rule
    candidate_profiles = []
    for rule in list_of_rules:
        candidate = rule[0]
        non_default_matches = 0
        for idx, field in enumerate(candidate):
            if profile[idx] == field or field == '*':
                if field != '*':
                    non_default_matches += 1
                if idx == len(candidate)-1:
                    #all fields matched, adding as candidate
                    candidate_profiles.append((rule,non_default_matches))
            else:
                break
    
    def getKey(item):
        return item[1]

    sorted_profiles = sorted(candidate_profiles, key=getKey, reverse=True)
    print "CANDIDATE PROFILES"
    for candidate in sorted_profiles: print candidate

    if len(sorted_profiles)>0:
        print "BEST CANDIDATE"
        print sorted_profiles[0][0]
    else:
        print "No match found"

    if len(sorted_profiles)>0:
        return sorted_profiles[0][0][1]
    else:
        return ""
    
# function eval_personalization_rules (input_file) : string = right part of the rule
def eval_personalization_rules_actions (rules_filename, profile):

    try:
        print 'openning ', rules_filename
        f = open(rules_filename, 'rU')
    except IOError:
        print 'cannot open', rules_filename
        return ''
    else:
        list_of_rules = parseRulesFileActions(f)
        print "LIST OF RULES"
        for rule in list_of_rules: print(rule)    
        
        f.close()

    #profile = parseProfile(profile_string)
    print "INPUT PROFILE", profile

    #look for more suitable rule
    return look_for_best_rule(list_of_rules, profile)


def eval_personalization_rules_buttons (rules_filename, profile):

    try:
        print 'openning ', rules_filename
        f = open(rules_filename, 'rU')
    except IOError:
        print 'cannot open', rules_filename
        return ''
    else:
        list_of_buttons = parseRulesFileButtons(f)
        print "LIST OF BUTTONS"
        for button in list_of_buttons: print(button)
        
        f.close()

    #profile = parseProfile(profile_string)
    print "INPUT PROFILE", profile

    final_buttons = []
    #look for more suitable rule for each button
    for button in list_of_buttons:
        list_of_button_rules = button[1]
        best = look_for_best_rule(list_of_button_rules, profile)
        final_buttons.append((button[0], best))


    print final_buttons
    return final_buttons

def eval_personalization_rules_grammar (rules_filename, profile):

    try:
        print 'openning ', rules_filename
        f = open(rules_filename, 'rU')
    except IOError:
        print 'cannot open', rules_filename
        return ''
    else:
        list_of_rules = parseRulesFileGrammar(f)
        print "LIST OF RULES"
        for rule in list_of_rules: print(rule)    
        
        f.close()

    #profile = parseProfile(profile_string)
    print "INPUT PROFILE", profile

    #look for more suitable rule
    return look_for_best_rule(list_of_rules, profile)


def parse_demo_list_file (demos_filename):
    try:
        print 'openning ', demos_filename
        filedemo = open(demos_filename, 'rU')
    except IOError:
        print 'cannot open', demos_filename
        return ''
    else:
        
        list_of_env = []
        list_of_demos = []
        current_demo_env = []
        while 1:
            line = filedemo.readline()
            if not line:
                if len(list_of_demos)>0:
                    list_of_env.append((current_demo_env, list_of_demos))
                break
            if line[0] == '<':
                #new environment
                if len(list_of_demos)>0:
                    list_of_env.append((current_demo_env, list_of_demos))
                list_of_demos = []

                line = line.strip("\n")
                current_demo_env = line.lstrip('<').rstrip('>')
            else:
                demo_name = line.strip("\n")
                list_of_demos.append(demo_name)
    
        filedemo.close()
        print list_of_env
        return list_of_env

def parse_init_file (init_filename):
    try:
        print 'openning ', init_filename
        fileinit = open(init_filename, 'rU')
    except IOError:
        print 'cannot open', init_filename
        return ''
    else:

	config = dict()
	while 1:
            line = fileinit.readline()
            if not line:
                break
            if line[0] != '\n':
                line = line.strip("\n").split(":")
                text = parseText(line[1])
                config[line[0]] = text

        return config





