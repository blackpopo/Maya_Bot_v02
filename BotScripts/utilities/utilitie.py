import os
import random
import csv
import re
te = re.compile('て(.)')


def read_lines():
    res_lines = list()
    src_dir = 'C://Users/Atsuya/Documents/Modern_Renai_Tanpen_norm1_mecab2'
    files = os.listdir(src_dir)
    files = random.choices(files, k=int(len(files)/15))
    for i, file in enumerate(files):
        print('{} % is finished...'.format(i/len(files)))
        with open(os.path.join(src_dir, file), 'r', encoding="utf-8") as f:
            lines = f.readlines()
        lines = [line.rstrip('\n') for line in lines]
        res_lines.extend(lines)
    random.shuffle(res_lines)
    return res_lines

def is_quote(after_sentence):
    if after_sentence.startswith('って') or after_sentence.startswith('と'):
        return True
    else:
        return False
    
def is_hearsay(after_sentence):
    if 'らし' in after_sentence or 'そう' in after_sentence or 'みたい' in after_sentence or 'よう' in after_sentence:
        return True
    return False

def is_deny(after_sentence):
    words = ['あるまい', 'あらへん', 'ございません', 'ありません']
    nais = ['ない', 'なかった', 'ず']
    if 'じゃない？' in after_sentence or after_sentence.startswith('じゃない'):
        return False
    for word in words:
        if word in after_sentence:
            return True
    for nai in nais:
        if nai in after_sentence:
            return True
    return False

def is_passive(after_sentence):
    if 'れる' in after_sentence or 'れた' in after_sentence or 'れて' in after_sentence:
        return True
    return False

def read_csv(csv_file_name):
    csv_file = open(csv_file_name, "r", encoding="utf-8")
    reader = list(csv.reader(csv_file))
    return reader

def is_conjunct(after_sentence):
    if '、' in after_sentence:
        return True
    re_tes =  te.findall(after_sentence)
    if len(re_tes) != 0:
        for re_te in re_tes:
            if re_te in ['い', 'し', 'る', 'ま']:
                pass
            else:
                return True
    return False

def is_adjunct(sentence):
    adjunct_particles = ["からには", "から", "ので", "さかい", "んで"]
    adjunct_conjunctions = ["なので", "だから", "ですから", "だからこそ", "ゆえに", "故に", "そやさかい", "よって", "従って", "したがって", "んで"]
    for word in adjunct_particles:
        if word in sentence:
            return True
    for word in adjunct_conjunctions:
        if word in sentence:
            return True
    return False

def is_not_ok(after_sentence):
    # print('Quote: ', is_quote(after_sentence))
    # print('Conjunct: ', is_quote(after_sentence))
    # print('Deny: ', is_quote(after_sentence))
    # print('Passive: ', is_quote(after_sentence))
    # print('Hearsay: ', is_quote(after_sentence))
    return is_quote(after_sentence) or is_conjunct(after_sentence) or is_passive(after_sentence) or is_hearsay(after_sentence)