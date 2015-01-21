#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

import sys
import re
import json
import os
import time
import logging
from pyquery import PyQuery as pq

from . import config
from ..shared import htmlgetter


reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

def getLink(link):
 #   logger.info('infunction getLink')
    music = pq(htmlgetter.getter(link))
 #   print link
 #   print music
    divs = pq(music('div[class="mod-hd"]'))
    aalink = divs('a')
    commentlink = None
    for aa in aalink:
        clink = pq(aa).attr('href')
        if 'comments' in clink:
            commentlink = clink
    if commentlink is None:
        logger.exception("strange music"+link)
        return None
  #  print commentlink
 #   logger.info('leaving getlink')
    return commentlink

def starparser(sstr):
    if sstr == u'力荐':
        return 5
    elif sstr == u'推荐':
        return 4
    elif sstr == u'还行':
        return 3
    elif sstr == u'较差':
        return 2
    else: return 1

def makejson(comment, name, link, user, star, f):
#    print comment, name, link, user, star
    star = starparser(star)
    commentdict = {}
    commentdict['comment'] = comment
    commentdict['moviename'] = name
    commentdict['movielink'] = link
    commentdict['user'] = user
    commentdict['rating'] = star
    f.write(json.dumps(commentdict, encoding="UTF-8", ensure_ascii=False))
    f.write('\n')


def comment(name, link, musicid):
    logger.info("Crawling music: %s", name)
    try:
        startlink = getLink(link)
    #    print link
    #    print startlink
        musicc = pq(htmlgetter.getter(startlink))
#        print("Path at terminal when executing this file")
#        print(os.getcwd() + "\n")
        f = open(config.CommentDir+musicid, 'w')
    except:
        logger.exception("wow")
        return
    countpage = 1
    logger.info(name)
    try:
        while True:
            countpage += 1
            if countpage % 30000 == 0 and countpage != 0:
                time.sleep(120)
            Body = pq(musicc('li[class="comment-item"]'))
            if Body is None:
                break
            if len(Body) < 5:
                break
            for lines in Body:
                lines = pq(lines)
             #   print lines
                commentitem = pq(lines('p[class="comment-content"]')).text()
                rating = pq(lines('span[class="comment-info"]'))('span')
                if len(rating) < 2:
                    continue
                rating = pq(rating[1]).attr('title')
                if rating is None:
                    continue
                finduser = pq(lines("a"))
                user = None
                for usernames in finduser:
                    usernames = pq(usernames)
                    href = usernames.attr("href")
                #    print usernames
                    if 'people' in href:
                    #    print href
                        user = re.match('.*/people/(.*)/', href).group(1)
                        break
                makejson(commentitem, name, link, user, rating, f)
         #   break
            musicc = pq(htmlgetter.getter(startlink + config.CommentSuffix + str(countpage)))
         #   logger.info('flip page')
        logger.info('sleeping')
        time.sleep(120)
        logger.info('end sleep')
    except KeyboardInterrupt:
        logger.error("Bye")
        raise
    except:
        logger.exception("what ghost!! error in page: %d", countpage)
        time.sleep(120)
        raise
        return
    finally:
        f.close()
        os.system('chmod 444 '+ config.CommentDir+musicid)

# vim: ts=4 sw=4 sts=4 expandtab
