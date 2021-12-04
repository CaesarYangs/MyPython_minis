# -*- coding:utf-8 -*-
import sys
import requests
import math
import io
import time
import os
from connectToNotionDB import postData
from lxml import etree
from lxml import html
import pandas as pd
import csv
from html.parser import HTMLParser

head = ('PaperName','Author','FromSchool','Time','Url')
csvfile = 'cnki9.csv'

path = csvfile
with open(path, 'a+') as f:
    csv_write = csv.writer(f)
    csv_write.writerow(head)
    f.close()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
record = 'CNKI'
articleType = "博士"
if articleType == "博士":
    ArticleType = 3
    Type = 3
else:
    ArticleType = 4
    Type = 4

page_url = 20  # 每页显示21篇论文


class POST:
    "获得url返回信息"

    def __init__(self, url='http://search.cnki.com.cn/Search/ListResult',
                 param={'searchType': 'MulityTermsSearch', 'ArticleType': ArticleType, 'ParamIsNullOrEmpty': 'true',
                        'Islegal': 'false', 'Summary': '软件', 'Type': ArticleType, 'Order': '2', 'Page': '1'}):
        self.url = url
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        self.param = param

    def response(self):
        html = requests.post(url=self.url, data=self.param, headers=self.header)
        return html.text


def get_pages(html):  # 获取总页数
    tree = etree.HTML(html)
    papers = tree.xpath('//input[@id="hidTotalCount"]/@value')[0]
    print(papers)
    pages = math.ceil(int(papers) / page_url)
    return pages


def get_paper_url(pages, post_form):
    # conn = sql_conn.conn_sql()
    # sql_conn.create_tab(conn)
    # cursor = conn.cursor()

    for i in range(1, pages + 1):
        post_form['Page'] = str(i)
        try:
            emp2 = POST(param=post_form)  # 使用默认参数
            response = emp2.response()
            tree = etree.HTML(response)
            tree_html = html.tostring(tree,encoding='utf-8').decode('utf-8')
            #print(tree_html)

        except:
            print("出错跳过")
            continue
        for num in range(1, page_url + 2):  # 每页有20个herf,xpath从1起始
            try:
                url = (tree.xpath('//div[@class="lplist"]/div[' + str(num) + ']/p/a/@href')[0])
                title = (tree.xpath('//div[@class="lplist"]/div[' + str(num) + ']/p/a/@title')[0])
                # 放在数组里面，然后每页存进txt文档一下
                author = (tree.xpath('//div[@class="lplist"]/div[' + str(num) + ']/p[3]/span[1]/@title')[0])
                describition = (tree.xpath('//div[@class="lplist"]/div[' + str(num) + ']/p[2]//text()')[0])
                school = (tree.xpath('//div[@class="lplist"]/div[' + str(num) + ']/p[3]/span[3]/@title')[0])
                time = (tree.xpath('//div[@class="lplist"]/div[' + str(num) + ']/p[3]/span[4]/text()')[0])
                datalist = [title,author,school,time,url]
                # dt = {'PaperName': title, 'PaperUrl': url, 'Author': author,'Describition':describition,'Time':time,'School':school}  # 字典
                # sql_conn.store_to_sql(dt, conn, cursor)  # 每条写入一次
                postData(title, author, url, describition, school, time)
                path = csvfile
                with open(path, 'a+') as f:
                    csv_write = csv.writer(f)
                    data_row = datalist
                    csv_write.writerow(data_row)
            except:
                continue


        # 获取结束时间
        # end = time.perf_counter()
        # print('获取文章详情页链接共用时：%s Seconds' % (end - start))


if __name__ == '__main__':
    # 获取开始时间
    start = time.perf_counter()
    # time.sleep(5)

    # 避免之前的内容重复爬取
    if os.path.exists('data-detail.txt'):
        print("存在输出文件，删除文件")
        os.remove('data-detail.txt')
        # 获取页数，可以根据搜索关键词进行url修改
    index_url = 'http://search.cnki.com.cn/Search/ListResult'
    page = '1'
    form = {'searchType': 'MulityTermsSearch', 'ArticleType': ArticleType, 'ParamIsNullOrEmpty': 'true',
            'Islegal': 'false', 'Summary': '自动驾驶', 'Type': Type, 'Order': '1', 'Page': page}
    emp1 = POST(index_url, form)  # 创建第一个类对象，用于获得返回数据
    html1 = emp1.response()
    maxpage = get_pages(html1)  # 最大页数
    maxpage = 50
    print('The total page is:', maxpage)
    get_paper_url(maxpage, form)  # 获取各检索结果文章链接