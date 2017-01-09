#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pprint import pprint
from json import JSONDecoder
import json
import re 
import itertools
from itertools import combinations


world_cont = ('Asia','Africa','North America','South America','Europe','Oceania')
lang_tag =('<*,*,it,*>','<*,*,es,*>','<*,*,en,*>')


def pick_up_json(namefile):
    with open(namefile, "r") as src:
        data= json.load(src)
        return data

def extract_info(in_path):
    basic_info = {}
    for root, dirs, files in os.walk(in_path):
        for afile in files:
            namefile = os.path.join(root, afile)
            if afile.endswith('.json'):
                with open (in_path+'basic_infos.txt','w') as wrt:
                    data = pick_up_json(namefile)
                             
                    capital = 'none'       
                    if 'Capital' in data['Government'].keys():
                        capital = re.split('[(;,]',data['Government']['Capital']['name']['text'])[0]
                    else:
                        pass
                    continent = data['Geography']['Map references']['text']
                    country = data['Government']['Country name']['conventional short form']['text']
                    area = data['Geography']['Area']['total']['text']
                    #economy = data['Economy']
                    #agriculture = economy['Agriculture - products']['text']
                    #industry = data['Economy']['Industries']['text']
                    #imports = data['Economy']['Imports - commodities']['text']
                    #exports = data['Economy']['Exports - commodities']['text']
                    basic_info[country]= continent, capital, re.sub('\D', '',area)
            ### Deleting anomalous country (es: regions, oceans and so on)
                    basic_info = {key: value for key, value in basic_info.items() if value[0] in world_cont}
                    wrt.write(str(basic_info))
                    wrt.close()
    return basic_info
                    
def choose_compare(basic_info,country1,country2):
    sizeC1 = basic_info[country1][2]
    sizeC2 = basic_info[country2][2]
    answer={}
    ans=['answer_right','answer_wrong']
    if sizeC1 > sizeC2:
        answer[country1]=ans[0]
        answer[country2]=ans[1]
    if sizeC1 < sizeC2:
        answer[country2]=ans[0]
        answer[country1]=ans[1]
    return answer

def action_button(answer,country1,country2):
    #answer = choose_compare(basic_info,country1,country2)
    t1_button = zip(lang_tag,('sì','sì','yes'))
    t2_button = zip(lang_tag,('no','no','no'))
    all_butt = t1_button,t2_button
    match_results = answer[country1],answer[country2]
    buttons = zip(match_results,all_butt)
    return buttons

def action_text(country1,country2):
    area_questionIT=('Lo Stato '+country1+' ha estensione maggiore dello Stato '+country2+'?')
    area_questionES=(country1+" es mas grande que "+country2+"?")
    area_questionEN=('Talking about area, is '+country1+' bigger than '+country2+' ?')
    all_quest = area_questionIT,area_questionES,area_questionEN
    texts = zip(lang_tag,all_quest)
    return texts

def action_grammar():
    en_grammar = '[LOAD_GRAMMAR] frame_confirm'
    it_grammar = en_grammar+'|it'
    es_grammar = en_grammar+'|es'  
    grammars = zip(lang_tag,(it_grammar,es_grammar,en_grammar))
    return grammars
    
def action(answer,country1,country2): 
    countries_action = {
    'NAME': 'area_'+(str(country1+country2)).translate(None, "^ '-._"),
    'TEXTS': action_text(country1,country2),
    'BUTTONS': action_button(answer,country1,country2),      
    'GRAMMARS': action_grammar()
    }
    return countries_action

def combination2(country_path):
    basic_info = extract_info(country_path)
    combination={}
    for country1,country2 in itertools.product(basic_info.keys(),basic_info.keys()):
        if country1==country2: continue
        ans = choose_compare(basic_info, country1, country2)
        combination[country1+country2]= action(ans,country1,country2)
        a = action(ans,country1,country2)
        yield a