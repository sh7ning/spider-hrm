# coding=utf-8

import traceback
import sys


class Error(Exception):
    pass


class Notice(Exception):
    pass


class Handler(object):
    @staticmethod
    def handle(exctype, excvalue, exc_traceback):
        traceback.print_tb(exc_traceback, file=sys.stdout)