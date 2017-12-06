
class ProfileMatcher():
    def __init__(self, action, profile):
        self.setAction(action)
        self.setProfile(profile)

    def setAction(self, action):
        self.action = action

    def setProfile(self, profile):
        self.profile = profile

    def evalSection(self, sectionType):
        if sectionType == "BUTTONS":
            buttonsList = self.action[sectionType]
            finalButtons = []
            for button in buttonsList:
                buttonRules = button[1]
                best = self.look_for_best_rule(buttonRules)
                finalButtons.append((button[0], best))
            return finalButtons
        else:
            return self.look_for_best_rule(self.action[sectionType])
        
    def look_for_best_rule(self, ruleList):
        #look for more suitable rule
        candidate_profiles = []
        for rule in ruleList:
            candidate = rule[0]
            non_default_matches = 0
            for idx, field in enumerate(candidate):
                if self.profile[idx] == field or field == '*':
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
    
