import re
from utilitie import *

feeling_list = list()

escape_list = ['つい',  'まし', '悪い', 'くさい', 'くさかった','かって', 'いたい',\
               'いたかった', 'くらい', '乙', 'ます',  '思い', 'まれ']

def build_feeling_csv():
    csv_file_name = 'C:/Users/Atsuya/PycharmProjects/Maya_v01_Development/utilities/Katuyou_Resource/feeling.csv'
    csv_file = read_csv(csv_file_name)
    for item in csv_file:
        if item[0] in escape_list:
            continue
        elif item[4] == '動詞':
            if 'を' not in item[0]:
                if item[9] == '基本形':
                    feeling_list.append(item[0] + ',' + item[-1])
                elif item[9] == '連用形':
                    feeling_list.append(item[0] + 'ます,' + item[-1])
                    feeling_list.append(item[0] + 'ました,' + item[-1])
                    feeling_list.append(item[0] + 'てた,' + item[-1])
                    feeling_list.append(item[0] + 'た,' + item[-1])
                elif item[9] == '連用タ接続':
                    feeling_list.pop()
                    feeling_list.pop()
                    if item[0][-1] == 'ん':
                        feeling_list.append(item[0] + 'でた,' + item[-1])
                        feeling_list.append(item[0] + 'だ,' + item[-1])
                    else:
                        feeling_list.append(item[0] + 'てた,' + item[-1])
                        feeling_list.append(item[0] + 'た,' + item[-1])
                    # print('Invalid item {} and pop is {}'.format(item[0], before))
                else:
                    pass
            else:
                pass
        elif item[4] == '形容詞':
            if item[9] == '基本形':
                feeling_list.append(item[0] + ',' + item[-1])
            elif item[9] == '連用タ接続':
                feeling_list.append(item[0] + 'た,' + item[-1])
            else:
                pass
        elif item[4] == '助動詞':
            if item[9] == '基本形':
                feeling_list.append(item[0] + ',' + item[-1])
            elif item[9] == '連用タ接続':
                feeling_list.append(item[0] + 'た,' + item[-1])
            else:
                pass
        else:
            if len(item[0]) == 1:
                pass
            else:
                feeling_list.append(item[0] + ',' + item[-1])

    with open('../CSVFiles/EMOTION/FeelingBase.csv', 'w', encoding='utf-8') as f:
        f.writelines('\n'.join(feeling_list))

if __name__=='__main__':
    build_feeling_csv()