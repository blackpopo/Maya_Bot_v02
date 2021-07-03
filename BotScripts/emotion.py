import re
from collections import defaultdict

from utilities.utilitie import *

class Emotion:
    def __init__(self):
        feeling_base_file_name = 'CSVFiles/EMOTION/FeelingBase.csv'
        feeling_base_reader = read_csv(feeling_base_file_name)
        self.feeling_bases = [(re.compile('(.*)(' + word +  ')(.*)'), feeling) for word, feeling in feeling_base_reader]
        
        feeling2line_file_name = 'CSVFiles/EMOTION/Feelings2Line.csv'
        feeling2line_reader = read_csv(feeling2line_file_name)
        self.feeling2line_dict = defaultdict(list)
        for row in feeling2line_reader:
            feeling, lines = row[0], row[1:]
            self.feeling2line_dict[feeling] = lines
        
        
        feeling2line_past_file_name = 'CSVFiles/EMOTION/Feelings2Line_past.csv'
        feeling2line_past_reader = read_csv(feeling2line_past_file_name)
        self.feeling2line_past_dict = defaultdict(list)
        for row in feeling2line_past_reader:
            feeling, lines = row[0], row[1:]
            self.feeling2line_past_dict[feeling] = lines

    def emotion(self, sentence):
        self.mid_start = len(sentence)
        self.mid_end = 0
        self.before_sentence = ''
        self.after_sentence = ''
        self.mid_sentence = ''
        self.key = None
        for word, feeling in self.feeling_bases:
            re_feeling = word.search(sentence)
            if re_feeling:
                before_sentence = re_feeling.group(1)
                mid_sentence = re_feeling.group(2)
                after_sentence = re_feeling.group(3)
                mid_start, mid_end = re_feeling.span(2)
                if mid_end > self.mid_end:
                    self.before_sentence = before_sentence
                    self.after_sentence = after_sentence
                    self.mid_sentence = mid_sentence
                    self.mid_end = mid_end
                    self.mid_start = mid_start
                    self.key = feeling
                elif mid_end == self.mid_end:
                    if mid_start < self.mid_start:
                        self.before_sentence = before_sentence
                        self.after_sentence = after_sentence
                        self.mid_sentence = mid_sentence
                        self.mid_end = mid_end
                        self.mid_start = mid_start
                        self.key = feeling
                    else:
                        pass
                else:
                    pass
        if self.mid_sentence != '':
            if not is_deny(self.after_sentence) and not is_not_ok(self.after_sentence):
                if self.mid_sentence.endswith('た'):
                    return random.choice(self.feeling2line_past_dict[self.key])
                else:
                    return random.choice(self.feeling2line_dict[self.key])
        return ''

if __name__=='__main__':
    from preprocess import Preprocess
    sentences = read_lines()
    preprocess = Preprocess()
    emotion = Emotion()
    for sentence in sentences:
        response, apply = preprocess.preprocess(sentence)
        response, apply = emotion.emotion(response)
        if response != '':
            print(sentence)
            print(response)
            print('\n')
