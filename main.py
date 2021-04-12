import json
import os
from nltk.tokenize import word_tokenize


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER,"tokens.json")
print(my_file)
# Read json file
with open(my_file) as file:
    doc_counts_list_sorted = dict(json.load(file))
    vocab = dict(sorted(doc_counts_list_sorted.items(), key=lambda item: -item[1]))
    #vocab_limited = list(vocab.keys())


LOWERCASE = [chr(x) for x in range(ord('a'), ord('z') + 1)]
UPPERCASE = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
LOWERCASE_OTHERS = ['ç', 'á', 'â', "ã",'à','é','ê','è','í','ì','ó','ô','õ']  
UPPERCASE_OTHERS = [x.upper() for x in LOWERCASE_OTHERS]
LETTERS = LOWERCASE + UPPERCASE + LOWERCASE_OTHERS + UPPERCASE_OTHERS

def edit1(text):
    words = []
    
    # Fase 1: as remoçoes.
    for p in range(len(text)):
        new_word = text[:p] + text[p + 1:]
        if len(new_word) > 0:
            words.append(new_word)
        
    # Fase 2: as adições.
    for p in range(len(text) + 1):
        for c in LETTERS:
            new_word = text[:p] + c + text[p:]
            words.append(new_word)
    
    # Fase 3: as substituições.
    for p in range(len(text)):
        orig_c = text[p]
        for c in LETTERS:
            if orig_c != c:
                new_word = text[:p] + c + text[p + 1:]
                words.append(new_word)
    
    return set(words)

def edit2(text):
    words1 = edit1(text)
    words2 = set()
    for w in words1:
        candidate_words2 = edit1(w)
        candidate_words2 -= words1
        words2.update(candidate_words2)
    words2 -= set([text])
    return words2

def corretor_string(frase):
    frase_corrigida = []
    token_frase =  word_tokenize(frase)
    for palavra in token_frase:
        if palavra in vocab:
            frase_corrigida.append(palavra)
        else:
            candidatos = []
            candidatos += \
                [w for w in edit1(palavra) if w in vocab] \
                + [w for w in edit2(palavra) if w in vocab] \
                + [palavra]
            frase_corrigida.append(candidatos[0])

    frase_corrigida_final = str()
    for palavra in frase_corrigida:
        frase_corrigida_final += palavra+" "
            
    return print(f"Sua frase corrigida é:{frase_corrigida_final}")

print("Escreva uma frase para ser corrigida:")
corretor_string(input())