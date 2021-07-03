from utilities.utilitie import *

class Question:
    def __init__(self):
        open_keyword_file_name = 'CSVFiles/QUESTION/OpenQuestionKeywords.csv'
        open_keyword_reader = read_csv(open_keyword_file_name)

        self.open_ends = [token + post for token in ['だ', 'だろう', 'です', 'でしょう']
                          for post in ['か。', 'か？', '。', '？']]

        self.question_ends =  ["かぁ", "かしらね", "かしら", "かな"]

        self.open_keywords = [re.compile('(.*)' + keyword[0] + '(.*)') for keyword in open_keyword_reader]

    def question(self, sentence):
        response = self.is_question(sentence)
        if response != '':
            return response
        return ''

    def is_question(self, sentence):
        for end in self.open_ends: #どうして、～なのだろうか？とかの内省系
            not_end = 'から' + end  #からだろう。とかでもう、答え言ってる（笑）
            if end in sentence:
                if not not_end in sentence:
                    for keyword in self.open_keywords: #疑問詞のチェック
                        re_keyword = keyword.search(sentence)
                        if re_keyword:
                            before_sentence = re_keyword.group(1)
                            after_sentence = re_keyword.group(2)
                            if not after_sentence.startswith('も') and not after_sentence.startswith('か') and not after_sentence.startswith('す') and not is_adjunct(before_sentence):
                                return 'きみはどう思っているの？'
                            else:
                                return 'へー、そうなんだ。それで？'
                else:
                     return 'へー、そうなんだ。それで？'

        for end in self.question_ends: #詠嘆のチェック
            q_end = end + '？'
            p_end = end + '。'
            if q_end in sentence or p_end in sentence:
                return 'どうして、そう思うの？'

        q_end = 'か' + '？' #疑問文で具体的に答える奴は分からないと答え、二択はググらせる。
        not_q_end = 'う' + q_end
        if q_end in sentence and not not_q_end in sentence:
            for keyword in ['なに', '何', 'だれ', '誰' ,'どこ', '何所', 'どう', 'いつ', 'どちら']:
                not_keyword = keyword + 'も'
                if keyword in sentence and not not_keyword in sentence:
                    return 'ごめんね。わかんないや。'
            else:
                return '調べてみる？'
        return ''

if __name__=='__main__':
    from preprocess import Preprocess
    from utilities.utilitie import *
    sentences = read_lines()
    preprocess = Preprocess()
    question = Question()
    # sentences = ['はっきりきっぱりお断りしたい春花だ。', '今日もそうなるのか、もう帰りたい。', '私は一ノ瀬くんの容姿に対する無頓着ぶりに頭を抱えたくなった。']
    for sentence in sentences:
        sentence = preprocess.preprocess(sentence)
        sentence, apply = question.question(sentence)
