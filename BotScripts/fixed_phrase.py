import re
import csv
from utilities.utilitie import *

class FixedPhraseClass:
    def __init__(self):
        self.hearsay_file_name = 'CSVFiles/FIXEDPHRASE/Hearsay.csv'
        hearsay_reader = read_csv(self.hearsay_file_name)
        self.hearsays = [hearsay[0] for hearsay in hearsay_reader]

        self.greeting_file_name = 'CSVFiles/FIXEDPHRASE/Greeting.csv'
        greeting_reader = read_csv(self.greeting_file_name)
        self.greetings = [(re.compile('^' + word + '(.*)'), response) for word, response in greeting_reader]


        self.fixed_file_names = ['CSVFiles/FIXEDPHRASE/Personal.csv']
        readers = [read_csv(csv_file) for csv_file in self.fixed_file_names]
        self.fixed_phrases = [(re.compile(row[0]), row[1]) for reader in readers for row in reader]


    def fixed_phrase(self, sentence):
        response = self.is_hearsay(sentence)
        if response != '':
            return response
        response = self.is_greeting(sentence)
        if response != '':
            return response
        response = self.is_fixed_phrase(sentence)
        if response != '':
            return response
        return ''

    def is_hearsay(self, sentence):
        for hearsay in self.hearsays:
            if hearsay in sentence:
                return 'へー、そうなんだ。それで、それで？'
        return ''

    def is_greeting(self, sentence):
        for greeting, response in self.greetings:
            re_greeting = greeting.search(sentence)
            if re_greeting:
                after_sentence = re_greeting.group(1)
                if not is_not_ok(after_sentence) and not is_deny(after_sentence):
                    return response
        return ''

    def is_fixed_phrase(self, sentence):
        for word, response in self.fixed_phrases:
            if word.search(sentence):
                return response
        return ''

if __name__=='__main__':
    sentences = read_lines()
    from preprocess import Preprocess
    preprocess = Preprocess()
    fixed_phrase = FixedPhraseClass()
    for sentence in sentences:
        sentence = preprocess.preprocess(sentence)
        sentence = fixed_phrase.fixed_phrase(sentence)
