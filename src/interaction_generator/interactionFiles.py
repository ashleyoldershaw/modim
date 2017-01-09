#!/usr/bin/env python
# -*- coding: utf-8 -*-

from interactionWriter import interactionWriter

def entertainment():
    from entertainment_act import entertainment_act
    return entertainment_act
    
def activity():
    from activity_act import activity_act
    return activity_act

def quiz_Football():
    import quiz_football as football
    football_path = 'databases/football.json/'
    quiz_football = football.football(football_path)
    #print type(quiz_football)
    return quiz_football

def quiz_Country():
    import quiz_country as country
    country_path = 'databases/factbook.json/'
    quiz_country = list(country.combination2(country_path))
    #print type(quiz_country)
    return quiz_country



def interactionGenerator(which_interaction,destination_path):
    
    if type(which_interaction) is dict:
        writerAct = interactionWriter(which_interaction)
        writerAct.writeAction(destination_path)
        print 'Interaction files generated succesfully'
        exit()
    if type(which_interaction) is list:
        print type(which_interaction)
        for item in which_interaction:
            writerAct = interactionWriter(item)
            writerAct.writeAction(destination_path)
        print 'Interaction files generated succesfully'
    else:
        print 'Error type, no interaction generated'
        