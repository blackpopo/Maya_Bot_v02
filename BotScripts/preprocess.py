import re
from utilities.utilitie import *
import random

class Preprocess:
    def __init__(self):
        self.last_sentence = re.compile("^[。？！].+?[。？！]")
        self.ends = re.compile("[。？！]$")

        speak_order_file_name = 'CSVFiles/PREPROCESS/SpeakOrder.csv'
        self.speak_order = [word[0] for word in read_csv(speak_order_file_name)]

        topic_file_name = 'CSVFiles/PREPROCESS/Topoic.csv'
        self.topic = [word[0] for word in read_csv(topic_file_name)]

    def preprocess(self, sentence):
        sentence = self.extract_last_sentence(sentence)
        response = self.speak_initialization(sentence)
        if response != '':
            return response, True
        return sentence, False

    def extract_last_sentence(self, sentence):
        if not self.ends.search(sentence):
            sentence = sentence + '。'
        sentence = sentence[::-1] + "。"
        re_sentence = self.last_sentence.search(sentence)
        sentence = re_sentence.group()
        sentence = sentence[::-1][1:]
        return sentence

    def speak_initialization(self, sentence):
        for word in self.speak_order:
            if sentence.startswith(word):
                return random.choice(self.topic)
        return ''

if __name__=='__main__':
    sentences = read_lines()
    preprocess = Preprocess()
    for sentence in sentences:
        response = preprocess.preprocess(sentence)