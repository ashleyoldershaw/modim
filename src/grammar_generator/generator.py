from lxml import etree
from __builtin__ import file
from io import open
import os

def generate_grammar_file(filename, save_directory):
    basename = os.path.basename(filename)
    topic_name = os.path.splitext(basename)[0]
    if '_' not in topic_name:
        lang = 'en-US'
        topic = topic_name
        topic_lang = topic+'_en'
    else:
        topic = topic_name.split('_')[0]
        topic_lang= topic_name.split('-')[0]
        lang = topic_name.split('_')[1]

    f = open(filename, 'r', encoding="utf-8")
    generate(f, save_directory, topic_name, topic, topic_lang, lang)
    

def generate(f, save_directory, topic_name, topic, topic_lang, lang):
    def write_xml(filename, xmldoc):
        print etree.tostring(xmldoc, pretty_print=True)
        xmldoc.write(filename, pretty_print=True, xml_declaration=True, encoding='utf-8')

    ns = {'xml': 'http://www.w3.org/XML/1998/namespace'}
   
    
# Here we create the GRAMMAR file
    # Create the root element
    root = etree.Element('grammar', {'version': '1.0',
                                    '{'+ns['xml']+'}lang': ''+lang+'',
                                    'xmlns': 'http://www.w3.org/2001/06/grammar',
                                    'tag-format': 'semantics/1.0',
                                    'root': 'main',
                                    'mode': 'voice'},
                         nsmap=ns)
    
    # Make a new document tree
    doc = etree.ElementTree(root)
    
    # Add the subelements
    rule1 = etree.SubElement(root, 'rule', id='main', scope='public')
    item1 = etree.SubElement(rule1, 'item')
    # da aggiungere lang             -----------------------------------------------------------------
    ruleref = etree.SubElement(item1, 'ruleref', uri='#'+topic+'')
    tag1 = etree.SubElement(item1, 'tag')
    # da aggiungere lang------------------------------------------------------------------------------
    tag1.text = 'out = "['+topic+',[impVp,[" + rules.'+topic+' + "]]]"'
    rule2 = etree.SubElement(root, 'rule', id=topic, scope='public') 
    oneof = etree.SubElement(rule2, 'one-of')
        

    for line in f:
        ls = line.rstrip('\r\n')
        if (not len(ls)>0):
            continue
        l, r = ls.split('->')
        r = r.strip()
        for m in l.split(','):
            item2 = etree.SubElement(oneof, 'item')
            item2.text = m.strip()
            tag2 = etree.SubElement(item2, 'tag')
            tag2.text = u'out="[target,[vb,[none,0.5]]],[answer,[nn,[{},0.5]]]"'.format(r)
                
    write_xml(save_directory+'/'+topic_lang+'.grxml', doc) 
    
    # -----------------------------------------
    # Here we create the FRAME file
    root = etree.Element('grammar', {'version': '1.0',
                                    '{'+ns['xml']+'}lang': ''+lang+'',
                                    'xmlns': 'http://www.w3.org/2001/06/grammar',
                                    'tag-format': 'semantics/1.0',
                                    'root': 'main',
                                    'mode': 'voice'},
                         nsmap=ns)
    
    # Make a new document tree
    doc = etree.ElementTree(root)
    
    # Add the subelements
    rule = etree.SubElement(root, 'rule', id='main', scope='public')
    oneof = etree.SubElement(rule, 'one-of')
    item = etree.SubElement(oneof, 'item')
    ruleref = etree.SubElement(item, 'ruleref', uri='#commands')
    tag = etree.SubElement(item, 'tag')
    tag.text = 'out = "[s," + rules.commands + "]";'
    rule1 = etree.SubElement(root, 'rule', id='commands', scope='public')
    ruleref = etree.SubElement(rule1, 'ruleref', uri='#preamble')
    oneof1 = etree.SubElement(rule1, 'one-of')
    item1 = etree.SubElement(oneof1, 'item')
    ruleref1 = etree.SubElement(item1, 'ruleref', uri= topic_lang+'.grxml#main')
    ruleref2 = etree.SubElement(rule1, 'ruleref', uri='#preamble')
    tag1 = etree.SubElement(rule1, 'tag')
    tag1.text = 'out = rules.main;'
    rule3 = etree.SubElement(root, 'rule', id='preamble', scope='public')
    ruleref3 = etree.SubElement(rule3, 'ruleref', special='GARBAGE')
    
    write_xml(save_directory+'/'+'frame_'+topic_lang+'.grxml', doc) 
    
    # -----------------------------------------
    # Here we create the XML file
    root = etree.Element('frame', name=topic)
    doc = etree.ElementTree(root)
     
    # Add the subelements
    elements = etree.SubElement(root, 'elements')
    fe = etree.SubElement(elements, 'fe', 
                                    arg='1',
                                    name='answer',
                                    type='core')
     
    command = etree.SubElement(root,'command')
    signature = etree.SubElement(command, 'signature')
    signature.text=topic.upper()
     
    write_xml(save_directory+'/'+topic+'.xml', doc)
     
