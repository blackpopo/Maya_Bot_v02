import re
import csv
from utilities.utilitie import *

class OpenQuestion:
    def __init__(self):
        one_phrase_open_question_file_name = 'CSVFiles/OPENQUESTION/OnePhraseOpenQuestion.csv'
        self.one_phrase_open_question_reader = read_csv(one_phrase_open_question_file_name)

        wanted_file_name = 'CSVFiles/OPENQUESTION/Want.csv'
        self.wanted_reader = read_csv(wanted_file_name)

        think_file_name = 'CSVFiles/OPENQUESTION/Think.csv'
        self.think_reader = read_csv(think_file_name)

        ikenai_file_name = 'CSVFiles/OPENQUESTION/Ikenai.csv'
        self.ikenai_reader = read_csv(ikenai_file_name)

        judge_file_name = 'CSVFiles/OPENQUESTION/Judge.csv'
        self.judge_reader = read_csv(judge_file_name)

        self.one_phrase_open_questions = [re.compile('(.*)' + phrase[0])  for phrase in self.one_phrase_open_question_reader]

        self.wanteds = [re.compile('(.*)(' + wanted[0] + ')(.*)') for wanted in self.wanted_reader]

        self.thinks = [(re.compile('(.*)' + think + '(.*)'), response) for think, response in self.think_reader]

        self.ikenais = [re.compile('(.*)(' + prefix +  ikenai[0] + ')(.*)') for prefix in ['ちゃ', 'じゃ', 'では', 'ては', 'れば'] for ikenai in self.ikenai_reader]

        self.guesses = [re.compile('(.*)' + guess + postfix + '。') for guess in ['だろう', 'でしょう', 'かも', 'かもしれません', 'かもしれない', 'かもしれなかった', 'かもしれませんでした'] \
            for postfix in [ 'けどな', 'けどね', 'しね', 'しな', 'か', 'な', 'ね', 'ぜ', 'よ', 'し', 'けど', '']]

        self.shoulds = [re.compile('(.*)' + '(べき' + post + ')(.*)') for post in [ 'だった', 'だ','です', 'でした', 'では', 'じゃ']]

        self.wishs = [re.compile('(.*)' + '(' + wish +  ')(.*)') for wish in ['たい', 'たく', 'たかった']]

        self.judges = [(re.compile('(.*)' + judge + '(.*)'), response) for judge, response in self.judge_reader]

        self.strongs = [re.compile('(.*)(' + strong + ')(.*)') for strong in ['最悪', '最良', '最悪', '最低', '駄目']]


    def open_question(self, sentence):
        response = self.one_phrase_response(sentence)
        if response != '':
            return response

        response = self.open_question_response(sentence)
        if response != '':
            return response
        return ''

    def one_phrase_response(self, sentence):
        for word in self.one_phrase_open_questions:
            if word.search(sentence):
                return 'そうなんだ。それで？'

        return ''


    def open_question_response(self, sentence):
        response = self.is_wanted(sentence)
        if response != '':
            return response
        response = self.is_think(sentence)
        if response != '':
            return response
        response = self.is_ikenai(sentence)
        if response != '':
            return response
        response = self.is_guess(sentence)
        if response != '':
            return response
        response = self.is_should(sentence)
        if response != '':
            return response
        response = self.is_wish(sentence)
        if response != '':
            return response
        response = self.is_strong(sentence)
        if response != '':
            return response
        return ''

    
    def is_wanted(self, sentence):
        for wanted in self.wanteds:
            re_wanted = wanted.search(sentence)
            if re_wanted:
                before_sentence = re_wanted.group(1)
                mid_sentence = re_wanted.group(2)
                after_sentence = re_wanted.group(3)
                if not is_not_ok(after_sentence) and not is_adjunct(before_sentence):
                    if is_deny(after_sentence):
                        if mid_sentence.endswith('た') or 'た' in after_sentence:
                            return 'どうして、そうして欲しくなかったの？'
                        else:
                            return 'どうして、そうして欲しくないの？'

                    else:
                        if mid_sentence.endswith('た') or 'た' in after_sentence:
                            return 'どうして、そうして欲しかったの？'
                        else:
                            return 'どうして、そうして欲しいの？'
                else:
                    pass
        return ''

    def is_think(self, sentence):
        for think, response in self.thinks:
            re_think = think.search(sentence)
            if re_think:
                before_sentence = re_think.group(1)
                after_sentence = re_think.group(2)
                if not is_not_ok(after_sentence) and not is_deny(after_sentence) and not is_adjunct(before_sentence):
                    return response
                else:
                    pass
        return ''
    
    def is_ikenai(self, sentence):
        for ikenai in self.ikenais:
            re_ikenai = ikenai.search(sentence)
            if re_ikenai:
                before_sentence = re_ikenai.group(1)
                mid_sentence = re_ikenai.group(2)
                after_sentence = re_ikenai.group(3)
                if not is_not_ok(after_sentence) and not is_deny(after_sentence) and not is_adjunct(before_sentence):
                    if mid_sentence.endswith('た') or 'た' in after_sentence:
                        return 'どうして、そうしてはいけなかったの？'
                    else:
                        return 'どうして、そうしていけないの？'
        return ''

    def is_guess(self, sentence):
        for guess in self.guesses:
            re_guess = guess.search(sentence)
            if re_guess:
                before_sentence = re_guess.group(1)
                if not is_adjunct(before_sentence):
                    return 'どうして、そう思うの？'
                else:
                    pass
        return ''

    def is_should(self, sentence):
        for should in self.shoulds:
            re_should = should.search(sentence)
            if re_should:
                before_sentence = re_should.group(1)
                mid_sentence = re_should.group(2)
                after_sentence = re_should.group(3)
                if not is_not_ok(after_sentence) and not is_adjunct(before_sentence):
                    if mid_sentence.endswith('じゃ') or mid_sentence.endswith('では'):
                        if 'た' in after_sentence:
                            return 'どうして、そうするべきじゃなかったの？'
                        else:
                            return 'どうして、そうするべきではないの？'

                    else:
                        if 'た' in mid_sentence:
                            return 'どうして、そうするべきだったの？'
                        else:
                            return 'どうして、そうするべきなの？'
                else:
                    pass
        return ''

    def is_wish(self, sentence):
        for wish in self.wishs:
            re_wish = wish.search(sentence)
            if re_wish:
                before_sentence = re_wish.group(1)
                mid_sentence = re_wish.group(2)
                after_sentence = re_wish.group(3)
                if len(before_sentence) > 0 and  before_sentence[-1] in 'いきしちにひりぎじぢび来居見えけせてね得寝経へめげぜでべ' and  not is_not_ok(after_sentence) and not is_adjunct(before_sentence):
                    if mid_sentence == 'たく':
                        if 'た' in after_sentence:
                            return 'どうして、そうしたくなかったの？'
                        else:
                            return 'どうして、そうしたくないの？'
                    else:
                        if 'た' in after_sentence:
                            return 'どうして、そうしたかったの？'
                        else:
                            return 'どうして、そうしたいの？'
                else:
                    pass

        return ''

    def is_strong(self, sentence):
        for judge, response in self.judges:
            re_judge = judge.search(sentence)
            if re_judge:
                before_sentence = re_judge.group(1)
                after_sentence = re_judge.group(2)
                if not is_not_ok(after_sentence) and not is_adjunct(before_sentence) and not is_deny(after_sentence):
                    return 'へー、そうなんだ。どんなところが' + response + 'の？'
                else:
                    pass

        for strong in self.strongs:
            re_strong = strong.search(sentence)
            if re_strong:
                before_sentence = re_strong.group(1)
                mid_sentence = re_strong.group(2)
                after_sentence = re_strong.group(3)
                if not is_adjunct(before_sentence):
                    if is_deny(after_sentence):
                        if 'た' in after_sentence:
                            return 'どんなところが、' + mid_sentence  + 'じゃなかったの？'
                        else:
                            return 'どんなところが、' + mid_sentence + 'じゃないの？'
                    else:
                        if 'た' in after_sentence:
                            return 'どんなところが、' + mid_sentence  + 'だったの？'
                        else:
                            return 'どんなところが、' + mid_sentence + 'なの？'
                else:
                    pass

        return ''


if __name__=='__main__':
    from preprocess import Preprocess
    from utilities.utilitie import *
    sentences = read_lines()
    preprocess = Preprocess()
    open_question = OpenQuestion()
    # sentences = ['はっきりきっぱりお断りしたい春花だ。', '今日もそうなるのか、もう帰りたい。', '私は一ノ瀬くんの容姿に対する無頓着ぶりに頭を抱えたくなった。']
    for sentence in sentences:
        sentence, apply = preprocess.preprocess(sentence)
        sentence, apply = open_question.open_question(sentence)
