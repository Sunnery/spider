#coding=utf-8
'''
Created on 2016-8-16

@author: 研发 papapa
'''
from pyquery import PyQuery as jq
import sys
sys.path.append("C:\\workSpace\\tools.py")
import tools

#解析Html
def parse_body(html,pageName,number):
    doc = jq(html)('.c_content_overflow')
    imgs = jq(doc('img'))
    urls = []
    for img in imgs:
        urls.append(''.join(['http://qq.yh31.com',jq(img).attr('src')]))
    return tools.saveImgsByNum(urls,pageName,number)

def get_image():
    isNext = 0
    url = 'http://qq.yh31.com/zjbq/0551964.html' 
    pageName = []
    pageName.append("jinguanzhang")
    number = 1
    while (isNext == 0):
        html = tools.getHTML(url)
        doc = jq(html)("#pe100_page_contentpage")
        next = jq(doc("a:last")).attr('href')
        nextUrl = ''.join(['http://qq.yh31.com',next])
        if (nextUrl == url):
            isNext = 1
        number = parse_body(html,pageName[0],number)
        url = nextUrl
        
if __name__ == '__main__':
    get_image()
    #tools.saveImgs([movie.get("img")],movie.get("电影名"))
        


