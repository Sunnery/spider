#coding=utf-8
'''
Created on 2016-8-11

@author: 研发
'''
from pyquery import PyQuery as jq
import sys
sys.path.append("C:\\workSpace\\tools.py")
import tools

#解析Html
def parse_body(html):
    movies = []
    doc = jq(html)('.item')
    for item in doc:
        item = jq(item)
        name = tools.parse_words(item, '.title')#获取名字
        order = tools.parse_words(item, 'em')#获取排名
        img = jq(item('img')[0]).attr('src')#获取imgUrl
        rating_num = tools.parse_words(item, '.rating_num')#获取评分
        comment_num = tools.parse_words(item, 'span:nth-child(4)')#获取评论数
        comment_num = tools.parse_comment_num(comment_num)#截取评论数的数字部分
        inq = tools.parse_words(item, '.inq')#获取引用语
        movie = (name, rating_num, comment_num, inq)
        movie = {
            '排名': order,
            '引用语': inq,
            'img': img,
            '评论数': comment_num,
            '评分': rating_num,
            '电影名': name
        }
        movies.append(movie)
    return movies

def get_top250():
    number_per_page = 25
    total_page_number = 1
    movies = []
    for page_no in range(total_page_number):
        url = 'https://movie.douban.com/top250?start={}&amp;filter='.format(page_no * number_per_page)
        html = tools.getHTML(url)
        movies.extend(parse_body(html))
    return movies

if __name__ == '__main__':
    movies = get_top250()
    for movie in movies:
        for(k,v) in movie.items():
            print k, v
        tools.saveImgs([movie.get("img")],movie.get("电影名"))
        print "--------------------------"
        


