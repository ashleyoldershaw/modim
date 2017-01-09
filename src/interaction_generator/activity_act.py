#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint

lang_tag =('<*,*,it,*>','<*,*,es,*>','<*,*,en,*>')

def action_text(): 
    texts = zip(lang_tag,('Ti andrebbe di fare un quiz?','¿Te apetece hacer un quiz?','Would you like to do a quiz?'))    
    return texts

def action_button():
    buttons_label = 'yes','no'
    positive_ans = 'sì','sì','yes'
    negative_ans = 'no','no','no'
    ans_pos,ans_neg = zip(lang_tag,positive_ans),zip(lang_tag,negative_ans)
    buttons = zip(buttons_label,(ans_pos,ans_neg))
    return buttons

def action_grammar(): 
    en_grammar = '[LOAD_GRAMMAR] frame_confirm'
    it_grammar = en_grammar+'|it'
    es_grammar = en_grammar+'|es'  
    grammars = zip(lang_tag,(it_grammar,es_grammar,en_grammar))
    return grammars

activity_act = {'NAME': 'activity',
        'TEXTS': action_text(),
        'BUTTONS': action_button(),
        'GRAMMARS': action_grammar()
    }
    
pprint (activity_act)