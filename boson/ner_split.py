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
import random
random.seed(0)


# ****************************************************************************** #

def paragraph_split(tagged_paragraph_list=None):
    sentences_list, sent_split = [], ["。/O", "！/O", "？/O", "；/O"]
    for paragraph in tagged_paragraph_list:
        temp = ''
        for sent in re.split('([ 。 ！ ？ ；]/[O])', paragraph):
            if sent not in sent_split:
                temp += sent
            else:
                if temp!='':
                    sentences_list.append(temp+sent)
                    temp = ''
                else:
                    continue
    return sentences_list


def file_split(all_list=None, shuffle=False, ratio=0.8):
    assert len(all_list)>0
    offset1 = int(len(all_list) * ratio)
    offset2 = (len(all_list)-offset1)//2 + offset1
    if shuffle:
        random.shuffle(all_list)    # 列表随机排序
    train = all_list[:offset1]
    dev = all_list[offset1:offset2]
    test = all_list[offset2:]
    return train, dev, test


def origin2tag(untagged_file=None):
    tagged_paragraph_list = []          # 存放标记后的数据

    for paragraph in untagged_file.readlines():
        # print(line)               # 当出现错误时，打印进行脏数据处理
        tagged_paragraph_str, i = '', 0
        while i<len(paragraph.rstrip('\n')):          # 对于每一句原始数据，逐字进行遍历
            if len(paragraph[i].strip()) == 0 or paragraph[i] == ' ' or paragraph[i]=='	' or paragraph[i]==' ':
                i += 1
            elif paragraph[i] == '{':      # 发现实体
                i+=2
                temp=""
                while paragraph[i]!='}':
                    temp+=paragraph[i]
                    i+=1
                i+=2

                tag, entity= temp.split(':')[0], temp.split(':')[1].strip()

                if len(entity)==1:  # 针对S标记
                    tagged_paragraph_str += entity+'/S-'+tag+' '
                else:               # 针对B、I、E标记
                    entity = entity.replace(' ', '_')
                    tagged_paragraph_str += entity[0]+'/B-'+tag+' '
                    for j in range(1, len(entity)-1):
                        tagged_paragraph_str += entity[j]+'/M-'+tag+' '
                    tagged_paragraph_str += entity[-1]+'/E-'+tag+' '
            else:                   # 对于非实体O标记
                tagged_paragraph_str += paragraph[i]+'/O '
                i += 1
        tagged_paragraph_list.append(tagged_paragraph_str)
    
    return tagged_paragraph_list


def flatten2result(input_list=None, output_file=None):
    for sentence in input_list:
        for char_tag_pair in sentence.rstrip('\n').split():
            # if len(char_tag_pair[0].strip()) == 0  or char_tag_pair[0] == ' ' or char_tag_pair[0]=='	' or char_tag_pair[0]==' ' or char_tag_pair[0]=='':
            if char_tag_pair.lstrip()[0] == '/':
                continue
            else:
                output_file.write(char_tag_pair.replace('/', ' ')+'\n')
        output_file.write('\n')


def main():
    # 针对vscode等不识别绝对路径的问题
    # cur_dir = os.chdir(os.path.dirname(__file__))

    # 将段落切分成句子
    with open('./data/BosonNLP_NER_6C.txt', 'r', encoding='utf-8') as boson_origin_file:
        tagged_paragraph_list = origin2tag(boson_origin_file)
        sentences_list = paragraph_split(tagged_paragraph_list)

        # 按8:2切分数据集为训练集、测试集
        train_list, dev_list, test_list = file_split(sentences_list, shuffle=True, ratio=0.8)

        # 按照”字 tag\n“的格式，平铺所有数据,并保存
        with open('./result/boson.train.bmes', 'w', encoding='utf-8') as train_file, \
            open('./result/boson.dev.bmes', 'w', encoding='utf-8') as dev_file, \
            open('./result/boson.test.bmes', 'w', encoding='utf-8') as test_file:
            flatten2result(train_list, train_file)
            flatten2result(dev_list, dev_file)
            flatten2result(test_list, test_file)
    

if __name__ == "__main__":
    main()

