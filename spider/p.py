#coding=utf-8
'''
Created on 2016-8-11

@author: 研发
'''
import socket
import ssl
from pyquery import PyQuery as jq


def parsed_url(url):
    # 检查协议
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        # '://' 定位 然后取第一个 / 的位置来切片
        u = url

    # 检查默认 path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 检查端口
    port_dict = {
        'http': 80,
        'https': 443,
    }
    port = port_dict[protocol]
    if host.find(':') != -1:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def socket_by_protocol(protocol):
    if protocol == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            break
    return response


def parsed_response(r):
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body


# 复杂的逻辑全部封装成函数
def get(url):
    protocol, host, port, path = parsed_url(url)

    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost:{}\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)

    status_code, headers, body = parsed_response(r)
    if status_code == 301:
        url = headers['Location']
        return get(url)

    return status_code, headers, body

#获得页面body部分
def get_html(url):
    status_code, headers, html = get(url)
    return html


#去掉评价人数的后缀
def parse_comment_num(comment):
    suffix_num = 3
    return comment[:len(comment) - suffix_num]

#解析出字符串
def parse_words(doc, selector):
    try:
        return jq(doc(selector)[0]).text()
    except:
        return jq(doc(selector)).text()


#解析Html
def parse_body(html):
    movies = []
    doc = jq(html)('.item')
    for item in doc:
        item = jq(item)
        name = parse_words(item, '.title')#获取名字
        rating_num = parse_words(item, '.rating_num')#获取评分
        comment_num = parse_words(item, 'span:nth-child(4)')#获取评论数
        comment_num = parse_comment_num(comment_num)#截取评论数的数字部分
        inq = parse_words(item, '.inq')#获取引用语
        movie = (name, rating_num, comment_num, inq)
        movie = {
            '引用语': inq,
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
        html = get_html(url)
        movies.extend(parse_body(html))
    return movies


if __name__ == '__main__':
   movies = get_top250()
   for movie in movies:
        print(movie)
        
        


