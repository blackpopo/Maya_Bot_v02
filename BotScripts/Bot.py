from utilities.utilitie import *
from preprocess import Preprocess
from fixed_phrase import FixedPhraseClass
from uncompleted import Uncompleted
from question import Question
from open_question import OpenQuestion
from emotion import Emotion
from aizuchi import Aizuchi

def main():
    #Class Definitions
    preprocess = Preprocess()
    fixed_phrase = FixedPhraseClass()
    uncompleted = Uncompleted()
    question = Question()
    open_question = OpenQuestion()
    emotion = Emotion()
    aizuchi = Aizuchi()
    ##########################

    cnt = 0
    sentences = read_lines()
    for sentence in sentences:
        cnt += 1
        sentence, is_topic = preprocess.preprocess(sentence)
        if not is_topic:
            response = fixed_phrase.fixed_phrase(sentence)
            if response == '':
                response = uncompleted.uncompleted(sentence)
            if response == '':
                response = question.question(sentence)
            if response == '':
                response = open_question.open_question(sentence)
            if response == '':
                response =  emotion.emotion(sentence)
            if response == '':
                response =  aizuchi.aizuchi()
                cnt -= 1
            print('Sentence: ' + sentence)
            print('Response: ' + response)
        else:
            print('Topic: ' + sentence)

    print("{} % line is created".format(cnt / len(sentences) * 100))

if __name__=='__main__':
    main()