#!/usr/bin/python
# coding=utf-8

import Strategies.Hrm6 as Hrm6
from Strategies.Hrm6 import Url
import sys
from Exception import Handler

if __name__ == '__main__':
    sys.excepthook = Handler.handle

    start_page = 1
    current_url = Url.get_page_url(Url, start_page)
    Hrm6.Spider().run(current_url)

    print 'spider work done.'
