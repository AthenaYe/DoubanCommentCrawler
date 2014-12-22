#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import sys
from pyquery import PyQuery as pq

reload(sys)
sys.setdefaultencoding('UTF-8')


DoubanMovieUrl = 'http://m.douban.com/movie/tag/movies?tag=2014'
Suffix = 'http://m.douban.com'
douban = pq(url=DoubanMovieUrl)

counter = 4

while True:
#    if not counter:
#        break
#    counter -= 1
    Body = pq(douban('div[class="movie-items list"]'))
#    MovieItems = Body("a").filter(lambda i:pq(this).text() != u'下一页' and pq(this).text() != u'最后页')
#    PageLoad = Body("a").filter(lambda i:pq(this).text() == u'下一页')
#    print PageLoad
    PageLoad = None
    MovieItems = Body("a")
    for divs in MovieItems:
        text = pq(divs).text()
        link = pq(divs).attr('href')
        if 'subject' in link:
            link = link + Suffix
            print text, link
        elif text == u'下一页':
            PageLoad = link
 #           print PageLoad
    if PageLoad == None:
        break
    else:
 #       print PageLoad
        douban = pq(url=Suffix+PageLoad)
#    print urls

# vim: ts=4 sw=4 sts=4 expandtab
