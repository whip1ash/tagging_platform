#!/usr/bin/env python3
# encoding: utf-8

'''
@author: whip1ash
@contact: security@whip1ash.cn
@software: pycharm 
@file: import_wiki_data.py
@time: 2020/3/10 09:23
@desc: 导入WikipediaSpider项目输出数据的desc字段到数据库Sentence表中。

@tips:
nltk需要本地下载punkt，在python命令行中执行以下语句：
import nltk
nltk.download('punkt')

手动下载地址
https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt.zip
'''

import json
import sys
from nltk.tokenize import sent_tokenize

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","app.settings")
import django
django.setup()
from app.normal.models import Sentence

def get_json_data(file_path):
    '''
    获取json数据
    :param file_path: 文件路径
    :return: list类型
    '''
    return json.load(open(file_path))

def get_desc_list(data):
    '''
    获得desc字段的全部数据
    :param data: list
    :return: list
    '''
    res = list()

    for item in data:
        if item['desc'].strip() != '':
            res.append(item['desc'])

    return res

def sentence_token(str):
    '''
    将段落分句
    :param str: str类型，段落文字
    :return: 每句话的list集合
    '''

    return sent_tokenize(str)

def para2sen(data):
    '''
    将段落拆分成单句话。
    :param data: 包含段落的list
    :return: 每个句子组成的list
    '''
    sentence_list = list()

    for paragraph in data:
        sentence_list += sent_tokenize(paragraph)

    return strip_list(sentence_list)

def strip_list(data):
    '''
    去除字符串列表中每一项的换行符等
    :param data: input data list
    :return: processed data list
    '''
    res = list()
    for item in data:
        res.append(item.strip())

    return res

def import_sentence2database(data):

    for sentence in data:
        try:
            sen = Sentence(content=sentence,source='W')
            sen.save()
        except Exception as e:
            print(e)
            return False

    return True

if __name__ == '__main__':

    if len(sys.argv) < 2:
        path = "./output.json"
    else:
        path = sys.argv[1]

    wiki_data = get_json_data(path)
    desc_list = get_desc_list(wiki_data)
    sentences = para2sen(desc_list)

    if import_sentence2database(sentences):
        print("Import data from Wikipedia Spider success!")
    else:
        print("Import Data Failed!")



