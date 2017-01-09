#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

lang_tag =('<*,*,it,*>','<*,*,es,*>','<*,*,en,*>')

def action_text(): 
    texts = zip(lang_tag,('Scegli un argomento','Elija un tema','Choose a topic'))    
    return texts

def action_button():
    buttons_label = 'football','geography'
    football_ans = 'Campionati di calcio','Campeonato de fútbol','Football Championship'
    geography_ans = 'Geografia','Geografía','Geography'
    ans_fot,ans_geo = zip(lang_tag,football_ans),zip(lang_tag,geography_ans)
    buttons = zip(buttons_label,(ans_fot,ans_geo))
    return buttons

def action_grammar(): 
    en_grammar = '[LOAD_GRAMMAR] frame_activity'
    it_grammar = en_grammar+'|it'
    es_grammar = en_grammar+'|es'  
    grammars = zip(lang_tag,(it_grammar,es_grammar,en_grammar))
    return grammars

entertainment_act = {'NAME': 'whichentertainment',
        'TEXTS': action_text(),
        'BUTTONS': action_button(),
        'GRAMMARS': action_grammar()
    }

pprint(entertainment_act)