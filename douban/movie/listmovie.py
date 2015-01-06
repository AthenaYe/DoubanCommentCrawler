#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import sys
import re
import os
import time
import logging

from pyquery import PyQuery as pq

from . import config
from . import moviecom
from ..shared import htmlgetter
from ..shared import loggerconfig


reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    logger = logging.getLogger(__name__)
    logger.info("System start")
    try:
        douban = pq(htmlgetter.getter(config.DoubanMovieUrl))
    except:
        logger.exception()
        logger.error("main list logging error")
        return
    while True:
        Body = pq(douban('div[class="movie-items list"]'))
        PageLoad = None
        MovieItems = Body("a")
        for divs in MovieItems:
            text = pq(divs).text()
            link = pq(divs).attr('href')
            if 'subject' in link:
                logger.info(link)

                idnum = re.match('/movie/subject/(\d+)/', link).group(1)
                link = config.Suffix + link

                logger.info(text)
                try:
                    moviecom.comment(text, link, idnum)
                except KeyboardInterrupt:
                    logger.info("Bye Bye")
                    return
                except:
                    logger.exception()
                    continue
                finally:
                    if os.path.exists(config.CommentDir+str(idnum)):
                        os.system('chmod 444 '+ config.CommentDir + str(idnum))
            elif text == u'下一页':
                PageLoad = link
    #           print PageLoad
        if PageLoad == None:
            break
        else:
            logger.info("nextpage:"+PageLoad)
            try:
                douban = pq(htmlgetter.getter(config.Suffix+PageLoad))
            except:
                logger.exception()
                logger.error("listmovie: flip next page time out")
                return


def test():
    print 'xxxx'


if __name__ == "__main__":
    main()

#    print urls

# vim: ts=4 sw=4 sts=4 expandtab
