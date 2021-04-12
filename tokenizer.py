import re
import json
import numpy as np
from collections import Counter
import os
from nltk.tokenize import word_tokenize
import nltk

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER,"dump_small.jsonln")
# Read json file
data = []
with open(my_file, 'r') as file:
    for line in file:
        data.append(json.loads(line))
        
print(f'Numero de documentos: {len(data)}')

class Tokenizer():
    def __init__(self):
        # retirados de : https://www.w3schools.com/tags/ref_attributes.asp
        # data: 03/04/2021
        html_attributes = ['accept',
         'accept-charset',
         'accesskey',
         'action',
         'align',
         'alt',
         'async',
         'autocomplete',
         'autofocus',
         'autoplay',
         'bgcolor',
         'border',
         'charset',
         'checked',
         'cite',
         'class',
         'color',
         'cols',
         'colspan',
         'content',
         'contenteditable',
         'controls',
         'coords',
         #'data', Retirado por estar afetando textos importantes (Como datas)
         'data-\*',
         'datetime',
         'default',
         'defer',
         'dir',
         'dirname',
         'disabled',
         'download',
         'draggable',
         'enctype',
         'for',
         'form',
         'formaction',
         'headers',
         'height',
         'hidden',
         'high',
         'href',
         'hreflang',
         'http-equiv',
         'id',
         'ismap',
         'kind',
         'label',
         'lang',
         'list',
         'loop',
         'low',
         'max',
         'maxlength',
         'media',
         'method',
         'min',
         'multiple',
         'muted',
         'name',
         'novalidate',
         'onabort',
         'onafterprint',
         'onbeforeprint',
         'onbeforeunload',
         'onblur',
         'oncanplay',
         'oncanplaythrough',
         'onchange',
         'onclick',
         'oncontextmenu',
         'oncopy',
         'oncuechange',
         'oncut',
         'ondblclick',
         'ondrag',
         'ondragend',
         'ondragenter',
         'ondragleave',
         'ondragover',
         'ondragstart',
         'ondrop',
         'ondurationchange',
         'onemptied',
         'onended',
         'onerror',
         'onfocus',
         'onhashchange',
         'oninput',
         'oninvalid',
         'onkeydown',
         'onkeypress',
         'onkeyup',
         'onload',
         'onloadeddata',
         'onloadedmetadata',
         'onloadstart',
         'onmousedown',
         'onmousemove',
         'onmouseout',
         'onmouseover',
         'onmouseup',
         'onmousewheel',
         'onoffline',
         'ononline',
         'onpagehide',
         'onpageshow',
         'onpaste',
         'onpause',
         'onplay',
         'onplaying',
         'onpopstate',
         'onprogress',
         'onratechange',
         'onreset',
         'onresize',
         'onscroll',
         'onsearch',
         'onseeked',
         'onseeking',
         'onselect',
         'onstalled',
         'onstorage',
         'onsubmit',
         'onsuspend',
         'ontimeupdate',
         'ontoggle',
         'onunload',
         'onvolumechange',
         'onwaiting',
         'onwheel',
         'open',
         'optimum',
         'pattern',
         'placeholder',
         'poster',
         'preload',
         'readonly',
         'rel',
         'required',
         'reversed',
         'rows',
         'rowspan',
         'sandbox',
         'scope',
         'selected',
         'shape',
         'size',
         'sizes',
         'span',
         'spellcheck',
         'src',
         'srcdoc',
         'srclang',
         'srcset',
         'start',
         'step',
         'style',
         'tabindex',
         'target',
         'title',
         'translate',
         'type',
         'usemap',
         'value',
         'width',
         'wrap']
        
        html_att_patt = r'((?:' + r'|'.join(html_attributes) + r')[=:].*?)[|}><;{}/]'
        
        self.chaves_matcher = re.compile(r'{{|}}',re.VERBOSE)
        
        self.patterns = {
            "spaces_0":r'\s\s*',
            "url":r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",
            "wiki_links":r'\[\[(?:[^|]*?\|)*?([^|]*?)\]\]',
            'html_att':html_att_patt,
            "aspas":r"""(['"]*)(.*?)\1""",
            "html":r"""<.*>|</.*>""",
            "Headers":r'=*(.*?)=*',
            "table_of_contents":r'__.*?__',
            'breaks':r'<br>|<br \>|{{break}}|{{clear}}',
            'nbsp_and_others':r'&.*?[=;|,]',
            'nowiki':r'<nowiki>|<nowiki[ ]*/>|<code>',
            'codes':r'&[#](?:\w*|\d*)',
            'math':r'<math.*?>.*?</math>',
            'vert_table':r'\{\||\|\}',
            'codes_2':r'[#].*?[ ;|]',
            'files':r'(\[\[)(?::*?File:.*?)(\||\]\])',
            'links':r'(?:autor)?link[=:].*?([|\]])',
            'alt':r'alt[=:]',
            'media_control':r'\[\[(Media\ Control\ Charts.*?)\]\]',
            'tios':r'~~*',
            'special':r'\[(?://|Special:).*]',
            "general":r'[^\w-]|ª',
            '- 1':r'\s-',
            '- 2':r'-\s',
            "numbers":r'\d*?',
            "spaces":r'\s\s*'
        }
        
        self.replies_mapping = {
            "spaces_0":r' ',
            "url":r'',
            "wiki_links":r'\1',
            'html_att':r' ',
            "aspas":r'\2',
            "html":r' ',
            "Headers":r'\1',
            "table_of_contents":r'',
            'breaks':r' ',
            'nbsp_and_others':r' ',
            'nowiki':r' ',
            'codes':r' ',
            'math':r' ',
            'vert_table':r' ',
            'codes_2':r' ',
            'files':r'/1/2 ',
            'links':r'/1',
            'alt':r' ',
            'media_control':r' ',
            'tios':r' ',
            'special':r' ',
            "general":r' ',
            '- 1':r' ',
            '- 2':r' ',
            "numbers":r'',
            "spaces":r' '
        }
        
        self.matchers = {}
        
        for key,patt in self.patterns.items():
            self.matchers[key] = re.compile(self.patterns[key],re.VERBOSE)
        

    def chaves_cleaner(self,text):
        conta = 0
        spans_proibidos = []
       
        for item in self.chaves_matcher.finditer(text):
            if item[0] == '{{':
                if conta == 0:
                    inicio = item.span()[0]
                conta += 1
            else:
                conta -= 1
                if conta == 0:
                    fim = item.span()[1]
                    spans_proibidos.append((inicio, fim))
        clean_text = ''
        inicio = 0
        for span in spans_proibidos:
            fim, novo_inicio = span
            clean_text += text[inicio:fim]
            inicio = novo_inicio
        clean_text += text[inicio:]
        return clean_text
    
    def clean_text(self,text):
        clean_text = self.chaves_cleaner(text)
        
        for matcher_name,matcher in self.matchers.items():
            clean_text = matcher.sub(self.replies_mapping[matcher_name],clean_text)
        
        return clean_text
    
    def tokenize(self,text):
        clean_text = self.clean_text(text)
        clean_text = clean_text.strip()
        tokens = clean_text.split(' ')
        return tokens

tokenizer = Tokenizer()

# Limpando todos os docs
all_cleaned_docs = []
for wiki_body in data[:]:
    all_cleaned_docs.append(tokenizer.clean_text(wiki_body["body"]))

#Tokenizando as palavras
nltk.download('punkt')

#Contando o numero de palavras
all_words_per_doc = []
for cleaned_doc in all_cleaned_docs:
    all_words_per_doc.append(word_tokenize(cleaned_doc))

all_words_per_doc_single = list()
for doc in all_words_per_doc:
    all_words_per_doc_single += set(doc)

doc_counts = Counter(all_words_per_doc_single)

doc_counts_list = list(doc_counts.items())

doc_counts_list_sorted = sorted(doc_counts_list, key=lambda x: (-x[1],x[0]))

with open("tokens.json", "w") as outfile: 
    json.dump(doc_counts_list_sorted, outfile)

print("Finished!")