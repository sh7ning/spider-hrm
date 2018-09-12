# coding=utf-8

from Strategies.Strategy import Spider as BasicSpider
# import re
from Exception import Error
import Http
import bs4
import Pg


class Spider(BasicSpider):

    def run(self, page):
        print '开始爬取 Category 网页: ', page

        page_obj = Category(page)
        articles_links = page_obj.get_articles()
        self._get_pics(articles_links)

        page = page_obj.get_next_page()
        if page is not None:
            self.run(Url.basic_url + page)
        else:
            print '>>>Category爬取完成'
            return True

    @staticmethod
    def _get_pics(articles_links):
        for article_id in articles_links:
            # 文章处理
            article = Article(article_id)
            article.get_pics(articles_links[article_id])
            article.save_pics()


class Url(object):
    domain = 'http://www.hrm6.com'

    basic_url = "http://www.hrm6.com/beautyleg/2017/"

    """
    获取当前页面的url
    """
    @staticmethod
    def get_page_url(cls, page):
        return cls.basic_url + str(page) + '.html'

"""
分类的单个页面
"""


class Category(object):
    # 专辑分类页的 content
    soup = ''

    def __init__(self, page_url):
        self._get_soup(page_url)

    def get_articles(self):
        articles_links = {}

        articles = self.soup.select('div.boxs ul.img li')
        for article_tag in articles:
            try:
                # article_id 并没有什么卵用
                article_id, article_name, article_link, cover = self._parse_article(article_tag)
            except Error, e:
                print '>>>_parse_article失败'
                print e
                # 错误的专辑直接跳过不需要处理
                continue

            # print '入库专辑', article_name, cover, article_id, article_link
            try:
                article_name = article_name[22:]
                article_new_id = Pg.Repository().insert_article(article_name, cover)
                print 'article写入', article_new_id
            except Exception, e:
                print '>>>article写入失败 ', article_name, ' ', cover
                print e
                continue
            articles_links[article_new_id] = article_link

        return articles_links

    def get_next_page(self):
        # @todo 增加判断，是否存在 key: 0
        return self.soup.select('#pages > span + a')[0].get('href')

    """
    获取当前页的 bs4
    """
    def _get_soup(self, page_url):
        content = Http.Http(page_url).get_content()
        self.soup = bs4.BeautifulSoup(content, 'lxml')

    def _parse_article(self, article_tag):
        links = article_tag.select('p.p_title a')
        # 只有一个 a 标签 @todo 增加判断 防止一个 a 标签都没
        link = links[0]
        article_id, article_name, article_link = self._parse_article_link(link)

        # 获取专辑的封面
        cover = article_tag.select('a img')[0]['src']

        return article_id, article_name, article_link, cover

    """
    解析专辑链接 获取 专辑名 和 专辑链接
    """
    def _parse_article_link(self, link):
        # 专辑名
        article_name = link.get_text()

        # 专辑链接
        href = link.get('href')
        article_link = Url.domain + href

        # article_id 并没有什么卵用，直接入库采用新的 di
        article_id = 0
        # res = re.search(re.compile(r'(\w*).html'), href)
        # if res is not None:
        #     article_id = res.groups()[0]
        #
        # if article_id == 0 or href == '':
        #     raise Error('获取专辑 id|href 失败')

        return article_id, article_name, article_link


class Article(object):
    article_id = 0
    pics = list()

    def __init__(self, article_id):
        self.article_id = article_id
        # 每次初始化，不然有问题 @todo 待明白原因
        self.pics = list()

    def get_pics(self, pic_link):
        print '抓取图片', pic_link
        page_obj = Pic(pic_link)
        # 收集专辑的图片
        self.pics.append(page_obj.get_pic())
        page = page_obj.get_next_page()
        if page is not None:
            self.get_pics(Url.basic_url + page)
        else:
            print '>>>图片分页为空'
            return self

    def save_pics(self):
        data = list()
        for pic in self.pics:
            data.append((self.article_id, pic))
        pic_ids = Pg.Repository().insert_pics(data)
        print '写入图片', self.article_id, ':', pic_ids


class Pic(object):
    # 图片页 soup
    soup = ''

    def __init__(self, link):
        content = Http.Http(link).get_content()
        self.soup = bs4.BeautifulSoup(content, 'lxml')

    def get_pic(self):
        # 抓取
        return self.soup.select('#img_view > img')[0]['src']

    def get_next_page(self):
        return self.soup.select('#pages > span + a')[0].get('href')
