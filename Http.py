# coding=utf-8

import urllib2


# Http 辅助类
class Http(object):

    def __init__(self, url):
        self.url = url

    # 获取内容
    def get_content(self):
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36' +
                              ' (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }
            response = urllib2.Request(self.url, headers=header)
            response = urllib2.urlopen(response, timeout=10)
            return response.read().decode('gbk')
        except Exception, e:
            print self.url + '打开网站失败'
            print e
            raise e
