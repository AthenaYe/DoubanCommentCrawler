#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import sys
import requests
import requests.exceptions
from pyquery import PyQuery as pq
from lxml import etree
import time
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

def parser(link):

    def _parser(link):
        link = requests.get(link, timeout=100)
#        xml = link.text.encode('utf-8')
#        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
#        h = etree.fromstring(xml, parser=parser)
#        return etree.tostring(h, encoding='utf-8')
        return link.text.encode('utf-8')

    for _ in range(5):
        try:
            ret = _parser(link)
        except requests.ConnectionError:
            time.sleep(10)
            continue
        except requests.exceptions.Timeout:
            time.sleep(10)
            continue
        else:
            return ret
    raise requests.ConnectionError("Connection Error")


# vim: ts=4 sw=4 sts=4 expandtab
