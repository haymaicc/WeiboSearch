import json
import os

import PIL.Image as Image
import jieba
import numpy
from wordcloud import WordCloud

cur_path = os.path.dirname(__file__)


def chinese_jieba(txt):
    jieba.load_userdict("./dict.txt")
    wordlist_jieba = jieba.cut(txt)  # 将文本分割，返回列表
    txt_jieba = " ".join(wordlist_jieba)  # 将列表拼接为以空格为间断的字符串
    return txt_jieba


stopwords = {'用户', '组图', 'http', 'https', '1http', 'cn', '2http', 'evidens', 'Evidens', '功课', 'weibo', '真的', '微博', '感觉',
             '转发', '这个', '可以', '没有', '但是', '还是', '还有', 'com', '自己', '小说', '地图', '除了', '日常', '事情', '小时', '最近', '部门',
             '就是', '觉得', '看上去', '你们', '好像', '因为', '什么', '一点', '现在', '加入', '一个', '对比', '比较', '很多', '时候', '之证', '所以',
             '而且', '之前', '今天', '如果', '拍照', '使用', '美丽', '大家', '面膜', '那么'}  # 噪声词
# 设置背景图
# 背景图片的画布一定要设置为白色（#FFFFFF）
# 然后显示的形状为不是白色的其他颜色
# 可以用ps或画图工具将自己要显示的形状复制到一个纯白色的画布上再保存
mask_pic = numpy.array(Image.open(os.path.join(cur_path, 'in.png')))
# 设置采用的文本
with open('weibo.txt', encoding='utf-8') as fp:
    readlines = fp.readlines()
    content = ""
    for txt in readlines:
        loads = json.loads(txt)
        content = content + loads.get("content")

    txt = chinese_jieba(content)
    wordcloud = WordCloud(
        font_path='msyh.ttf',
        scale=5,
        background_color='white',  # 背景色
        max_words=200,  # 最大显示单词数
        max_font_size=100,  # 频率最大单词字体大小
        stopwords=stopwords,  # 过滤噪声词
        mask=mask_pic,  # 自定义显示的效果图
        collocations=False
    ).generate(txt)

    dict_word = wordcloud.process_text(txt)
    dict_word = sorted(dict_word.items(), key=lambda items: items[1], reverse=True)[0:50]
    print(dict_word)

    wordcloud.to_file("out.png")  # 保存为图片
    image = wordcloud.to_image()
    image.show()
