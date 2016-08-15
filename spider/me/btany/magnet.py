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
        name = tools.parse_words(item, '.title')#获取名字
        magnet = jq(item('.title')[1]).attr('href')#获取imgUrl
        movie = {
            '标题': name,
            '磁力链接': magnet,
        }
        movies.append(movie)
    return movies

def get_bt():
    key = "国产"
    bts = []
    url = ''.join(['http://www.nimasou.net/l/',key,'-hot-desc-1'])
    html = tools.getHTML(url)
    #print html
    bts = parse_body(html)
    return bts

if __name__ == '__main__':
    bts = get_bt()
    for bt in bts:
        for(k,v) in bt.items():
            print k, v
        
        print "--------------------------"
        


