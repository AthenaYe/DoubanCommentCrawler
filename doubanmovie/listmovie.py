#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import sys
import re
import os
import time
import logging

from pyquery import PyQuery as pq

import config
import moviecom


reload(sys)
sys.setdefaultencoding('UTF-8')


def main():
    logger = logging.getLogger(__name__)
    logger.info("System start")
    douban = pq(url=config.DoubanMovieUrl)

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
                    os.system('chmod 444 '+ config.CommentDir + str(idnum))
                    continue
                os.system('chmod 444 '+ config.CommentDir + str(idnum))
            elif text == u'下一页':
                PageLoad = link
    #           print PageLoad
        if PageLoad == None:
            break
        else:
    #       print PageLoad
            douban = pq(url=config.Suffix+PageLoad)



if __name__ == "__main__":
    main()

#    print urls

# vim: ts=4 sw=4 sts=4 expandtab
