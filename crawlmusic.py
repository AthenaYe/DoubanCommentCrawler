#!/usr/bin/env python2
# -*- coding:utf-8 -*-

__author__ = 'athena'

from pyquery import PyQuery as pq

import douban.music.listmusic as listmusic
import douban.shared.htmlgetter as htmlgetter
import douban.music.musiccom as musiccom

#musiccom.getLink('http://music.douban.com/subject/25811077/')

#test = pq(htmlgetter.getter('http://music.douban.com/tag/2014'))
listmusic.main()
#musiccom.comment("shashasha", "http://music.douban.com/subject/25811077/", "ceshi")



# vim: ts=4 sw=4 sts=4 expandtab