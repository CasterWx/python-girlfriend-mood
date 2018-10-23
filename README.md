## 直男眼里 的 没有对象也要谈恋爱之女朋友的情绪监控 之 分词

> Blog : [Antzuhl](http://www.cnblogs.com/LexMoon/)

> Github : [CasterWx](https://github.com/CasterWx)


:kissing_closed_eyes::kissing_closed_eyes:  通过女朋友的一句话分析她的心情 。

Analyze her mood through her girlfriend's words .


## 第一章 分词

### 1、JieBa库
>“结巴”中文分词：做最好的 Python 中文分词组件

>"Jieba" (Chinese for "to stutter") Chinese text segmentation: built to be the best Python Chinese word segmentation module.

### 2、特点
 * 支持三种分词模式：
     * 精确模式，试图将句子最精确地切开，适合文本分析；
     * 全模式，把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；
     * 搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。

 * 支持繁体分词
 * 支持自定义词典
 * MIT 授权协议

### 3、算法
 * 基于前缀词典实现高效的词图扫描，生成句子中汉字所有可能成词情况所构成的有向无环图 (DAG)
 * 采用了动态规划查找最大概率路径, 找出基于词频的最大切分组合
 * 对于未登录词，采用了基于汉字成词能力的 HMM 模型，使用了 Viterbi 算法

### 4、主要功能

####   1) 分词
 * `jieba.cut` 方法接受三个输入参数: 需要分词的字符串；cut_all 参数用来控制是否采用全模式；HMM 参数用来控制是否使用 HMM 模型
 * `jieba.cut_for_search` 方法接受两个参数：需要分词的字符串；是否使用 HMM 模型。该方法适合用于搜索引擎构建倒排索引的分词，粒度比较细
 * 待分词的字符串可以是 unicode 或 UTF-8 字符串、GBK 字符串。注意：不建议直接输入 GBK 字符串，可能无法预料地错误解码成 UTF-8
 * `jieba.cut` 以及 `jieba.cut_for_search` 返回的结构都是一个可迭代的 generator，可以使用 for 循环来获得分词后得到的每一个词语(unicode)，或者用
 * `jieba.lcut` 以及 `jieba.lcut_for_search` 直接返回 list
 * `jieba.Tokenizer(dictionary=DEFAULT_DICT)` 新建自定义分词器，可用于同时使用不同词典。`jieba.dt` 为默认分词器，所有全局分词相关函数都是该分词器的映射。
```python
seg_list = jieba.cut("我要有女朋友了", cut_all=True)
print("全模式: " + "/ ".join(seg_list))  # 全模式

seg_list = jieba.cut("我要有女朋友了", cut_all=False)
print("默认模式: " + "/ ".join(seg_list))  # 默认模式

seg_list = jieba.cut("我要有女朋友了")
print(", ".join(seg_list))

seg_list = jieba.cut_for_search("我要有女朋友了，然后我要打爆室友的狗头")  # 搜索引擎模式
print("搜索引擎模式: "+", ".join(seg_list))  
```
output :
```
全模式: 我/ 要/ 有/ 女朋友/ 朋友/ 了
默认模式: 我要/ 有/ 女朋友/ 了
我要, 有, 女朋友, 了
搜索引擎模式: 我要, 有, 朋友, 女朋友, 了, ，, 然后, 我要, 打爆, 室友, 的, 狗头
```
####   2) 添加自定义词典
 >载入词典
 * 开发者可以指定自己自定义的词典，以便包含 jieba 词库里没有的词。虽然 jieba 有新词识别能力，但是自行添加新词可以保证更高的正确率
 * 用法： jieba.load_userdict(file_name) # file_name 为文件类对象或自定义词典的路径
 * 词典格式和 `dict.txt` 一样，一个词占一行；每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒。`file_name` 若为路径或二进制方式打开的文件，则文件必须为 UTF-8 编码。
 * 词频省略时使用自动计算的能保证分出该词的词频。
```python
print('/'.join(jieba.cut('这个东梨会不会被分开呢。', HMM=False)))
# 添加字典
print(jieba.suggest_freq(('东梨'), True)) # 添加一个词语'东梨'
print('/'.join(jieba.cut('这个东梨会不会被分开呢。', HMM=False)))
```
output :
```
这个/东/梨/会/不会/被/分开/呢/。
这个/东梨/会/不会/被/分开/呢/。
```

 >调整词典

* 使用 `add_word(word, freq=None, tag=None)` 和 `del_word(word)` 可在程序中动态修改词典。
* 使用 `suggest_freq(segment, tune=True)` 可调节单个词语的词频，使其能（或不能）被分出来。

* 注意：自动计算的词频在使用 HMM 新词发现功能时可能无效。

####   3) 关键词提取
> 基于 TF-IDF 算法的关键词抽取

`import jieba.analyse`

* jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
  * sentence 为待提取的文本
  * topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
  * withWeight 为是否一并返回关键词权重值，默认值为 False
  * allowPOS 仅包括指定词性的词，默认值为空，即不筛选
* jieba.analyse.TFIDF(idf_path=None) 新建 TFIDF 实例，idf_path 为 IDF 频率文件

```python
s = "操作系统（Operation System，简称OS）是管理计算机硬件与软件资源的程序，是计算机系统的内核与基石；操作系统本质上是运行在计算机上的软件程序 ；为用户提供一个与系统交互的操作界面 ；操作系统分内核与外壳（我们可以把外壳理解成围绕着内核的应用程序，而内核就是能操作硬件的程序）。"
for x, w in jieba.analyse.extract_tags(s, withWeight=True):
    print('%s %s' % (x, w))

print('-'*40)
print(' TextRank')
print('-'*40)

for x, w in jieba.analyse.textrank(s, withWeight=True):
    print('%s %s' % (x, w))
```
output :
```
内核 1.0625279118105262
操作系统 0.7315222629276317
外壳 0.4645002019336842
软件程序 0.36580730663157895
软件资源 0.34756659135263157
程序 0.3333060550794737
操作界面 0.32345367735526315
Operation 0.31459914481315787
System 0.31459914481315787
OS 0.31459914481315787
计算机硬件 0.2800679240526316
应用程序 0.2763021123763158
计算机系统 0.23982068182078944
交互 0.23731251919447366
基石 0.23595272944342105
硬件 0.22168984473789474
本质 0.18271527055526315
用户 0.1795351598005263
计算机 0.1790732744968421
围绕 0.177282393885
----------------------------------------
 TextRank
----------------------------------------
内核 1.0
程序 0.5362199524590612
系统 0.48948949335129555
提供 0.48602227553244165
围绕 0.4446670737747918
运行 0.4225011310851474
管理 0.4151898395341863
基石 0.4131936048253403
计算机系统 0.38302557644090945
硬件 0.36775003601316436
操作 0.36615155530109056
本质 0.3554627436547271
计算机硬件 0.3491604047032015
理解 0.3433887505596043
外壳 0.3419635842574655
应用程序 0.33616306371021853
用户 0.33122514947879544
交互 0.3287196036788538
计算机 0.23122054865622482
简称 0.22777433887730136
```
####   4) 词性标注
* `jieba.posseg.POSTokenizer(tokenizer=None)` 新建自定义分词器，`tokenizer` 参数可指定内部使用的 `jieba.Tokenizer` 分词器。`jieba.posseg.dt` 为默认词性标注分词器。
* 标注句子分词后每个词的词性，采用和 ictclas 兼容的标记法。
* 用法示例
```python
words = jieba.posseg.cut("我爱北京天安门")
for word, flag in words:
    print('%s %s' % (word, flag))
print('='*40)
```
output :
```
我 r
爱 v
北京 ns
天安门 ns
```
####   5) 并行分词
* 原理：将目标文本按行分隔后，把各行文本分配到多个 Python 进程并行分词，然后归并结果，从而获得分词速度的可观提升
* 基于 python 自带的 multiprocessing 模块，目前暂不支持 Windows
* 用法：
    * `jieba.enable_parallel(4)` # 开启并行分词模式，参数为并行进程数
    * `jieba.disable_parallel()` # 关闭并行分词模式

####   6) Tokenize：返回词语在原文的起止位置
* 注意，输入参数只接受 unicode
* 默认模式
```python
print(' 默认模式')
print('-'*40)
result = jieba.tokenize('永和服装饰品有限公司')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))

print('-'*40)
print(' 搜索模式')
print('-'*40)

result = jieba.tokenize('永和服装饰品有限公司', mode='search')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))
```
output :
```
word 永和		 start: 0 		 end:2
word 服装		 start: 2 		 end:4
word 饰品		 start: 4 		 end:6
word 有限公司		 start: 6 		 end:10
----------------------------------------
 搜索模式
----------------------------------------
word 永和		 start: 0 		 end:2
word 服装		 start: 2 		 end:4
word 饰品		 start: 4 		 end:6
word 有限		 start: 6 		 end:8
word 公司		 start: 8 		 end:10
word 有限公司		 start: 6 		 end:10
```

### 5、一个完整的分词可运行实例
目录结构
> jieba是我们要导入的第三方库，在项目中我直接把它放在了里面。
```
│  run.py
│
└─jieba
    │  dict.txt
    │  _compat.py
    │  __init__.py
    │  __main__.py
    │
    ├─analyse
    │  │  analyzer.py
    │  │  idf.txt
    │  │  textrank.py
    │  │  tfidf.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          analyzer.cpython-37.pyc
    │          textrank.cpython-37.pyc
    │          tfidf.cpython-37.pyc
    │          __init__.cpython-37.pyc
    │
    ├─finalseg
    │  │  prob_emit.p
    │  │  prob_emit.py
    │  │  prob_start.p
    │  │  prob_start.py
    │  │  prob_trans.p
    │  │  prob_trans.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          prob_emit.cpython-37.pyc
    │          prob_start.cpython-37.pyc
    │          prob_trans.cpython-37.pyc
    │          __init__.cpython-37.pyc
    │
    ├─posseg
    │  │  char_state_tab.p
    │  │  char_state_tab.py
    │  │  prob_emit.p
    │  │  prob_emit.py
    │  │  prob_start.p
    │  │  prob_start.py
    │  │  prob_trans.p
    │  │  prob_trans.py
    │  │  viterbi.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          char_state_tab.cpython-37.pyc
    │          prob_emit.cpython-37.pyc
    │          prob_start.cpython-37.pyc
    │          prob_trans.cpython-37.pyc
    │          viterbi.cpython-37.pyc
    │          __init__.cpython-37.pyc
    │
    └─__pycache__
            _compat.cpython-37.pyc
            __init__.cpython-37.pyc
```

run.py中编写代码，并且调用jieba库实现分词。

run.py
```python
#encoding=utf-8
from __future__ import unicode_literals
import jieba

if __name__=="__main__":
    ch = input()
    seg_list = jieba.cut(str(ch))
    print(", ".join(seg_list))
```
在此处输入"我马上就要有女朋友了"。

即可得到输出结果如下。
> 我, 马上, 就要, 有, 女朋友, 了

### 6、代码地址
    Github : [https://github.com/CasterWx/python-girlfriend-mood](https://github.com/CasterWx/python-girlfriend-mood)
