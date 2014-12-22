#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup as bt

douban  = urllib2.urlopen('http://m.douban.com/movie/tag/movies?tag=2014').read()
soup = bt(douban)
for links in soup.find_all('a'):
    link = links.get('href')
    if not link:
        continue
    if 'subject' in link:
        subject = urllib2.urlopen('http://m.douban.com/'+link).read()
        tmpsoup = bt(subject)
        for tmplinks in tmpsoup.find_all('a'):
            tmplink = tmplinks.get('href')
            if not tmplink:
                continue
            if 'comments' in tmplink:
                comment = urllib2.urlopen('http://m.douban.com/'+tmplink)
                print comment.geturl()

# vim: ts=4 sw=4 sts=4 expandtab
