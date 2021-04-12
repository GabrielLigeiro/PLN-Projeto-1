import re
import json
import numpy as np
from collections import Counter
import os
from nltk.tokenize import word_tokenize
import nltk
from tokenizer import Tokenizer


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER,"dump_small.jsonln")
# Read json file
data = []
with open(my_file, 'r') as file:
    for line in file:
        data.append(json.loads(line))
        
print(f'Numero de documentos: {len(data)}')


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