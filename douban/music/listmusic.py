#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

import re
import os
import time
import sys
import logging
from pyquery import PyQuery as pq

from . import config
from ..shared import htmlgetter
from . import musiccom


reload(sys)
sys.setdefaultencoding('utf-8')


def test():
    print ('asdasda')

def main():
    logger = logging.getLogger(__name__)
    logger.info("System start")
    try:
        douban = pq(htmlgetter.getter(config.DoubanMusicUrl))
    except:
        logger.exception("main list logging error")
        return

    while True:
        Page = pq(douban('div[class="paginator"]'))
        MovieItems = douban('div[class="pl2"]')
        for divs in MovieItems:
            divs = pq(divs)
            divs = divs("a")
            text = pq(divs).text()
            link = pq(divs).attr('href')
            if 'subject' in link:
                logger.info(link)
                idnum = re.match('.*/subject/(\d+)/', link).group(1)
                logger.info(text)
                try:
                    musiccom.comment(text, link, idnum)
                #    print text
                except KeyboardInterrupt:
                    logger.info("Bye Bye")
                    return
                except:
                    logger.exception('what')
                    continue
                finally:
                    if os.path.exists(config.CommentDir+str(idnum)):
                        os.system('chmod 444 '+ config.CommentDir + str(idnum))
        PageLoad = pq(Page('a')[-1]).attr('href')
        print PageLoad
    #    break
        if PageLoad == None:
            break
        else:
            logger.info("nextpage:"+PageLoad)
            try:
                douban = pq(htmlgetter.getter(PageLoad))
            except:
                logger.exception()
                logger.error("listmovie: flip next page time out")
                return



# vim: ts=4 sw=4 sts=4 expandtab
