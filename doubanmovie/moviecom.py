#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import config
import sys
from pyquery import PyQuery as pq
import re
import json


reload(sys)
sys.setdefaultencoding('utf-8')

def comment(name, link, movieid):
    movie = pq(url=link)
    aa = movie('a')
    CommentLink = None
    for divs in aa:
        CommentLink = pq(divs).attr('href')
        if 'comment' in CommentLink:
            break
    CommentLink = config.Suffix + CommentLink
    moviec = pq(url=CommentLink)
    f = open(config.CommentDir+movieid, 'w')
    while True:

        commentdict = {}

        Body = pq(moviec('div[class="list"]'))
        Body.pop()
        PageLoad = None
        CommentItems = Body('span')
        Page = Body('a')
        CommentItems.pop()
        odd = 0
        for lines in CommentItems:
            if odd % 2 == 1:
                tmp = pq(lines).text()
            #    print tmp
                whole = re.match('-(.*) \(([1-5])', tmp)
                if not whole:
                    continue
                user = whole.group(1)
                star = int(whole.group(2))
                if star in [1,5]:
                    commentdict['moviename'] = name
                    commentdict['movielink'] = link
                    commentdict['user'] = user
                    commentdict['rating'] = star
                    f.write(json.dumps(commentdict, encoding="UTF-8", ensure_ascii=False))
                    f.write('\n')
                    commentdict.clear()
            else:
                commentdict['comment'] = pq(lines).text()
            odd += 1
        for lines in Page:
#            print pq(lines).text()
            if pq(lines).text() == u'下一页':
                PageLoad = pq(lines).attr('href')
                PageLoad = config.Suffix + PageLoad
                moviec = pq(url=PageLoad)
                break
        if PageLoad == None:
            break
    f.close()

if __name__ == '__main__':
    comment(u'消失的爱人', 'http://m.douban.com/movie/subject/21318488/?session=55b6a7d1', '21318488')

# vim: ts=4 sw=4 sts=4 expandtab
