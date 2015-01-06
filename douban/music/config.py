#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import logging.config
import sys

DoubanMusicUrl = "http://music.douban.com/tag/2014"

Suffix = 'http://m.douban.com'
CommentDir = 'doubancomment/'


logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stdout,
        },
        'logfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': 'info_log',
        },
        'errfile': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': 'error_log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'logfile', 'errfile'],
            'level': 'INFO',
        },
    },
})


# vim: ts=4 sw=4 sts=4 expandtab