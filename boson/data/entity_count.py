# !/usr/bin/python
# -*-coding:utf-8 -*-
import glob2


def count(filepath):
    """
    filepath: 文件所在目录
    """
    for file in glob2.glob(filepath+'*.bmes'):
        file_name = file.split('/')[-1].rstrip('.bmes')
        char_num, sent_num = 0, 0
        entities_num, entity_len = [], 0
        
        with open(file, 'r', encoding='utf-8') as fin:
            lines = fin.readlines()
            char_num = len(lines)
            for line in lines:
                if len(line.strip()) < 3:
                    sent_num += 1
                    continue
                elif ' O' in line:
                    continue

                entity_len += 1
                if 'S-' in line or 'E-' in line:
                    if entity_len > len(entities_num):
                        entities_num += [0 for i in range(entity_len-len(entities_num))]
                    entities_num[entity_len-1] += 1
                    entity_len = 0
        
        with open('count.txt', 'a', encoding='utf-8') as fout:
            entities_sum = sum(entities_num)
            fout.write(file_name+':\tchar_num:'+str(char_num-sent_num)+'\tsent_num:'+str(sent_num)+'\tentity_num:'+str(entities_sum))
            count_str = ','.join(list(map(str, entities_num)))
            count_rate = ','.join(list(map(str, map(lambda x: round(x/entities_sum,4), entities_num))))
            fout.write('\ndetail:'+count_str+'\n'+count_rate+'\n\n')


if __name__ == "__main__":
    bmesdir = './'
    count(bmesdir)
