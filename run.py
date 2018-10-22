#encoding=utf-8
from __future__ import unicode_literals
import jieba

if __name__=="__main__":
    ch = input()
    seg_list = jieba.cut(str(ch))
    print(", ".join(seg_list))
