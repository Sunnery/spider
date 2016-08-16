#coding=utf-8
'''
Created on 2016-8-15

@author: 研发
'''
from pyquery import PyQuery as jq
import sys
sys.path.append("C:\\workSpace\\tools.py")
import tools

#解析Html
def parse_body(html):
    movies = []
    doc = jq(html)('.x-item')
    for item in doc:
        item = jq(item)
        name = tools.parse_words(item, '.title')
        magnet = jq(item('.title')[1]).attr('href')
        print '名称          ：',name
        print '磁力链接: ',magnet
        print '--------------------------------------------------------------'
    return movies

def get_bt():
    key = "a"
    for i in range(1,10+1):
        url = ''.join(['http://www.nimasou.net/l/',key,'-hot-desc-',str(i)])
        html = tools.getHTML(url)
        bts = parse_body(html)
    return bts

if __name__ == '__main__':
    bts = get_bt()
        


