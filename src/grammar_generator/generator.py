from main import generate
import glob
import os
 
 
for i in glob.glob('topics/*.txt'):
    topic_name = os.path.splitext(os.path.basename(i))[0]
    if '_' not in topic_name:
        lang = 'en-US'
        topic = topic_name
        topic_lang = topic+'_en'
        generate(topic_name, topic, topic_lang, lang)
    else:
        topic = topic_name.split('_')[0]
        topic_lang= topic_name.split('-')[0]
        lang = topic_name.split('_')[1]
        generate(topic_name, topic, topic_lang, lang)
