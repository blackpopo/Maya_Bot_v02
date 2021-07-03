from utilities.utilitie import *

class Uncompleted:
    def __init__(self):
        one_phrase_uncompleted_file_name = 'CSVFiles/UNCOMPLETED/OnePhraseUncompleted.csv'
        self.one_phrase_uncompleted_reader = read_csv(one_phrase_uncompleted_file_name)

        uncompleted_file_name = 'CSVFiles/UNCOMPLETED/Uncompleted.csv'
        self.uncompleted_reader = read_csv(uncompleted_file_name)

        self.except_uncompleted = ['こと。', 'んで。', 'ので。']

    def uncompleted(self, sentence):
        response = self.one_phrase_response(sentence)
        if response != '':
            return response

        response = self.uncompleted_response(sentence)
        if response != '':
            return response

        return ''

    def one_phrase_response(self, sentence):
        for word in self.one_phrase_uncompleted_reader:
            assert len(word) == 1
            word = word[0]
            if word in sentence:
                word = word[:-1] +'？'
                return word
        return ''

    def uncompleted_response(self, sentence):
        for word, response in self.uncompleted_reader:
            if word in sentence:
                for ex_word in self.except_uncompleted:
                    if ex_word in sentence:
                        return response
                return response
        return ''
