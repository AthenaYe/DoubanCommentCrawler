#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import sys
import re
import json
import os
import time
import logging

from pyquery import PyQuery as pq

import config
import ..shared.config
import ..shared.htmlparser

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)


def getLink(link):
    movie = pq(htmlparser.parser(link))
    aa = movie('a')
    CommentLink = None
    for divs in aa:
        CommentLink = pq(divs).attr('href')
        if 'comment' in CommentLink:
            break
    CommentLink = config.Suffix + CommentLink
    logger.debug("CommentLink: %s", CommentLink)

    return CommentLink


def makejson(CommentItems, name, link, f):
    commentdict = {}
    odd = 0
    for lines in CommentItems:
        if odd % 2 == 1:
            tmp = pq(lines).text()
            whole = re.match('-(.*) \(([1-5])', tmp)
            if not whole:
                continue
            user = whole.group(1)
            star = int(whole.group(2))
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


def comment(name, link, movieid):
    logger.info("Crawling move: %s", name)
    try:
        moviec = pq(htmlparser.parser(getLink(link)))
        f = open(config.CommentDir+movieid, 'w')
    except:
        logger.exception("wow")
        return
    countpage = 0
    PageLoad = ''
    print name
    try:
        while True:
            countpage += 1
            if countpage % 30000 == 0 and countpage != 0:
                time.sleep(120)
            Body = pq(moviec('div[class="list"]'))
            if Body.size() < 2:
                break;
            Body.pop()
            PageLoad = None
            CommentItems = Body('span')
            Page = Body('a')
            if CommentItems.size() < 4:
                break
            CommentItems.pop()
            makejson(CommentItems, name, link, f)

            for lines in Page:
    #            print pq(lines).text()
                if pq(lines).text() == u'下一页':
                    PageLoad = pq(lines).attr('href')
                    PageLoad = config.Suffix + PageLoad
                    moviec = pq(htmlparser.parser(PageLoad))
                    break
            if PageLoad == None:
                break
        time.sleep(120)
    except KeyboardInterrupt:
        logger.error("Bye")
        raise
    except:
        logger.exception("what ghost!! page: %d, %s", countpage, PageLoad)
        time.sleep(120)
        raise
        return
    finally:
        f.close()
        os.system('chmod 444 '+ config.CommentDir+movieid)



if __name__ == '__main__':
    comment(u'啥啥啥', 'http://m.douban.com/movie/subject/10463953/', 'ceshi')

# vim: ts=4 sw=4 sts=4 expandtab
