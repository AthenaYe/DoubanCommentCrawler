#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import config
import sys
from pyquery import PyQuery as pq


reload(sys)
sys.setdefaultencoding('UTF-8')

def comment(name, link):
    movie = pq(url=link)
    aa = movie('a')
    CommentLink = None
    for divs in aa:
        CommentLink = pq(divs).attr('href')
        if 'comment' in CommentLink:
            break
    CommentLink = config.Suffix + CommentLink
    moviec = pq(url=CommentLink)
    while True:
        Body = pq(moviec('div[class="list"]'))
        Body.pop()
        PageLoad = None
        CommentItems = Body('span')
        Page = Body('a')
        CommentItems.pop()
        for lines in CommentItems:
            print pq(lines).text()
        for lines in Page:
#            print pq(lines).text()
            if pq(lines).text() == u'下一页':
                PageLoad = pq(lines).attr('href')
                PageLoad = config.Suffix + PageLoad
                moviec = pq(url=PageLoad)
                break
        if PageLoad == None:
            break





comment(u'小时的爱人', 'http://m.douban.com/movie/subject/21318488/?session=55b6a7d1')

# vim: ts=4 sw=4 sts=4 expandtab
