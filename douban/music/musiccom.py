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
    music = pq(htmlgetter.getter(link))
    print link
    print music
    span = pq(music('span[class="pl"]'))
    print span
    commentlink = pq(span('a')).attr('href')
    if commentlink is None:
        logger.exception("strange music"+link)
        return None
    return commentlink

def makejson(comment, name, link, user, star, f):
    print comment, name, link, user, star
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
        print link
        print startlink
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
                break;
            for lines in Body:
                lines = pq(lines)
                commentitem = pq(lines('p[class="comment-item"]')).text()
                rating = pq(lines('span[class="user-stars allstar30 rating"]')).attr('title')
                if rating is None:
                    continue
                finduser = pq(lines("a"))
                user = None
                for usernames in finduser:
                    usernames = pq(usernames)
                    href = usernames.attr("href")
                    if 'people' in href:
                        user = usernames.text()
                        break
                makejson(commentitem, name, link, user, rating, f)
            break
            musicc = pq(htmlgetter.getter(startlink + config.CommentSuffix + str(countpage)))

        time.sleep(120)
    except KeyboardInterrupt:
        logger.error("Bye")
        raise
    except:
        logger.exception("what ghost!! page: %d", countpage)
        time.sleep(120)
        raise
        return
    finally:
        f.close()
        os.system('chmod 444 '+ config.CommentDir+musicid)

# vim: ts=4 sw=4 sts=4 expandtab
