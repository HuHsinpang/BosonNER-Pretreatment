# ****************************************************************************** #
#                           BosonNER Data Pretreatment                           #
#                                                                                #
#  Author: Hsinpang    Email:hsinpang@alumni.hust.edu.cn   Time:2020.6.24        #
#  Envirenment: linux, python3.x                                                 #
#                                                                                #
# ****************************************************************************** #

# !/usr/bin/python
# -*-coding:utf-8 -*-
 
import random
import os
import re


# ****************************************************************************** #

def paragraph_split(origin_file=None):
    sentences_list, sent_end = [], ['；', '。', '！']
    for line in origin_file.readlines():
        sentence_items, sent_idx = re.split('([；。！])', line), 0  # 切分句子，保留分隔符
        while sent_idx < len(sentence_items):
            if sentence_items[sent_idx] not in sent_end:
                if sent_idx<len(sentence_items)-2 and sentence_items[sent_idx+1] in sent_end:
                    sentence = sentence_items[sent_idx]+sentence_items[sent_idx+1]
                    sent_idx += 1
                else:
                    sentence = sentence_items[sent_idx]
            sent_idx += 1
            sentences_list.append(sentence)
    
    return sentences_list


def train_test_split(all_list=None, shuffle=False, ratio=0.8):
    assert len(all_list)>0
    offset1 = int(len(all_list) * ratio)
    offset2 = (len(all_list)-offset1)//2 + offset1
    if shuffle:
        random.shuffle(all_list)    # 列表随机排序
    train = all_list[:offset1]
    dev = all_list[offset1:offset2]
    test = all_list[offset2:]
    return train, dev, test


def origin2tag(untagged_list=None):
    tagged_lines_list = []           # 存放标记后的数据

    for line in untagged_list:
        # print(line)               # 用来脏数据处理
        tagged_line_str, i = '', 0
        while i<len(line):          # 对于每一句原始数据，逐字进行遍历
            if line[i] == '{':      # 发现实体
                i+=2
                temp=""
                while line[i]!='}':
                    temp+=line[i]
                    i+=1
                i+=2

                tag, entity= temp.split(':')[0], temp.split(':')[1]

                if len(entity)==1:  # 针对S标记
                    tagged_line_str += entity+'/S_'+tag+' '
                else:               # 针对B、I、E标记
                    tagged_line_str += entity[0]+'/B_'+tag+' '
                    for j in range(1, len(entity)-1):
                        tagged_line_str += entity[j]+'/M_'+tag+' '
                    tagged_line_str += entity[-1]+'/E_'+tag+' '
            else:                   # 对于非实体O标记
                tagged_line_str += line[i]+'/O '
                i+=1
        tagged_lines_list.append(tagged_line_str)
    
    return tagged_lines_list


def flatten2result(input_list=None, output_file=None):
    for sentence in input_list:
        for char_tag_pair in sentence.rstrip('\n').split():
            if char_tag_pair[0] == ' ':
                continue
            else:
                output_file.write(char_tag_pair.replace('/', ' ')+'\n')
        output_file.write('\n')


def main():
    # 针对vscode等不识别绝对路径的问题
    # cur_dir = os.chdir(os.path.dirname(__file__))

    # 将段落切分成句子
    with open('./data/BosonNLP_NER_6C.txt', 'r', encoding='utf-8') as boson_origin_file:
        sentences_list = paragraph_split(boson_origin_file)

    # 按8:2切分数据集为训练集、测试集
    train_list, dev_list, test_list = train_test_split(sentences_list, shuffle=True, ratio=0.8)

    # 将实体标注转换为BIOES标注
    tagged_train_list, tagged_dev_list, tagged_test_list = origin2tag(train_list), origin2tag(dev_list), origin2tag(test_list)

    # 按照”字 tag\n“的格式，平铺所有数据,并保存
    with open('./result/boson.train.bmes', 'w', encoding='utf-8') as train_file, \
        open('./result/boson.dev.bmes', 'w', encoding='utf-8') as dev_file, \
        open('./result/boson.test.bmes', 'w', encoding='utf-8') as test_file:
        flatten2result(tagged_train_list, train_file)
        flatten2result(tagged_dev_list, dev_file)
        flatten2result(tagged_test_list, test_file)
    

if __name__ == "__main__":
    main()
