#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from pprint import pprint
from json import JSONDecoder
import json
from dateutil.parser import parse
import re


lang_tag =('<*,*,it,*>','<*,*,es,*>','<*,*,en,*>')


def pick_up_json(namefile):
    with open(namefile, "r") as src:
        data= json.load(src)
        return data

def match2(afile): 
    data=pick_up_json(afile)          
    rounds_number = range(len(data['rounds']))
    for match_day in rounds_number:
        match_name = data['rounds'][match_day]['name']
        matches = data['rounds'][match_day]['matches']
        for match in matches:
            for key_match,value_match in match.items():
                if type(value_match) is dict:
                    match[key_match] = value_match['name']
                #assign a 'code' to team with None code
                    if not value_match['code']:
                        match[key_match+'code'] = (value_match['key'][:3]).upper()
                        #print match[key_match+'code']
                    else:
                        match[key_match+'code'] = value_match['code']               
        #Rewriting of the matches date
            match['date']=parse(match['date']).strftime('%d %m %Y')      
        # Add the match_day to the matches dictionary
            match['giornata']=match_name
            gen_info = dict(giornata=str(match['giornata']),
                            date=str(match['date']),
                            t1code=match['team1code'],
                            t2code=match['team2code'])
            
            
            match_info = dict(team1=match['team1'].encode('utf-8'),
                              team2=match['team2'].encode('utf-8'),
                              score1=str(match['score1']),
                              score2=str(match['score2']))
            
            a =action(gen_info,match_info)
            yield a

def result2(match_info):
    answer={}
    ans=('answer_right','answer_wrong')
    if match_info['score1'] > match_info['score2']:
        answer[match_info['team1']]=ans[0]
        answer[match_info['team2']]=ans[1]
        answer['X']=ans[1]
    if match_info['score1'] < match_info['score2']:
        answer[match_info['team2']]=ans[0]
        answer[match_info['team1']]=ans[1]
        answer['X']=ans[1]
    if match_info['score1'] == match_info['score2']:
        answer['X']=ans[0]
        answer[match_info['team2']]=ans[1]
        answer[match_info['team1']]=ans[1]
    return answer

def action_text(gen_info,match_info): 
    all_info = dict(gen_info,**match_info)
    all_info['giornata'] = re.sub('\D', '', gen_info['giornata'])
    it_question= ('Nella {giornata}^ Giornata di Campionato, chi ha vinto la partita {team1} - {team2} ?').format(**all_info)
    es_question=('En la Journada {giornata}, quién ganó el partido {team1} - {team2} ?').format(**all_info)
    en_question=('In the Matchday {giornata}, who won the match {team1} - {team2} ?').format(**all_info)
    #general_question='Which was the result of the match {team1} - {team2} ?'.format(**locals())
    all_quest = (it_question,es_question,en_question)
    texts = zip(lang_tag,all_quest)
    return texts

def action_button(match_info):
    answer = result2(match_info)
    t1_button = zip(lang_tag,(match_info['team1']+' vince',match_info['team1']+' vence',match_info['team1']+' wins'))
    draw_button = zip(lang_tag,('pareggio','debujar','draw'))
    t2_button = zip(lang_tag,(match_info['team2']+' vince',match_info['team2']+' vence',match_info['team2']+' wins'))
    all_butt = t1_button,draw_button,t2_button
    match_results = answer[match_info['team1']],answer['X'],answer[match_info['team2']]
    buttons = zip(match_results,all_butt)
    return buttons

def action_grammar():
    en_grammar = '[LOAD_GRAMMAR] frame_confirm'
    it_grammar = en_grammar+'|it'
    es_grammar = en_grammar+'|es'  
    grammars = zip(lang_tag,(it_grammar,es_grammar,en_grammar))
    return grammars

def action_name(gen_info):
    action_name = str(gen_info['date']+gen_info['t1code']+gen_info['t2code'])
    return action_name.translate(None, "^ '-._")

def action(gen_info,match_info): 
    football_action = {
    'NAME': action_name(gen_info),
    'TEXTS': action_text(gen_info, match_info),
    'BUTTONS': action_button(match_info),
    'GRAMMARS': action_grammar()
    }
    #pprint (football_action)
    return football_action

def football(in_path):
    quizzes = list()
    for root, dirs, files in os.walk(in_path):
        #print dirs
            for file in files:
                #print file
                if file == '.DS_Store':
                    continue
                league,extension = os.path.splitext(os.path.splitext(file)[0])
                lookfor = ('en','es','it')
                if league not in lookfor:
                    continue
                else:
                    namefile = os.path.join(root, file)
                    quiz = list(match2(namefile))
                quizzes = quizzes+quiz
    return quizzes
               