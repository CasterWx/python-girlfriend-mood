#encoding=utf-8
from __future__ import unicode_literals
import jieba
import matplotlib.pyplot as plt

# 基础值
mood = 8
# 估值字典
dic = dict()
# 定值序列
nice = list()
bad  = list()
def initMoonValue():
    # MoodValue  key - value
    f = open('data/MoodValue.txt','r')
    word = f.readlines()
    print('init MoonValue data...')
    for i in word:
        sp = i.split('\t')
        dic[sp[0]] = sp[1].replace("\n","")
    print(len(dic))


def initMoonNice():
    # MoonNice value
    f = open('data/MoodNice.txt','r',encoding='gb18030',errors='ignore')
    word = f.readlines()
    print('init MoonNice data...')
    for i in word:
        nice.append(i)
    print(len(nice))


def initMoonBad():
    # MoonNice value
    f = open('data/MoodBad.txt','r',encoding='gb18030',errors='ignore')
    word = f.readlines()
    print('init MoonBad data...')
    for i in word:
        bad.append(i)
    print(len(bad))


moodlist = list()


def loadOld():
    f = open('data/old.txt','r')
    print('init old data...')
    word = f.readlines()
    for i in word :
        moodlist.append(float(i))


if __name__ == '__main__':
    #loadOld()
    moodlist.append(8)
    initMoonValue()
    initMoonNice()
    initMoonBad()
    f = open('data/old.txt','w')
    while True:
        ch = input()
        seg_list = jieba.cut(str(ch))
        words = list(seg_list)
        for i in words:
            print(i)
            if i in dic.keys():
                mood = mood + float(dic[i])
            if i in nice :
                mood = mood + 0.5
            if i in bad :
                mood = mood - 0.5
        moodlist.append(mood)
        print(moodlist)
        # save daat
        x = range(0,len(moodlist))
        plt.xlabel(u'对话')
        plt.ylabel(u'Mood')
        plt.title('女朋友情绪分析')
        plt.ylim(-20,20)
        plt.plot(x , moodlist)
        plt.show()
