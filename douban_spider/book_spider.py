# -*- coding: UTF-8 -*-

# 把str编码由默认ascii（python2为ascii，python3为utf8）改为utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

print
import time
import urllib2
import requests
# from bs4 import BeautifulSoup
import BeautifulSoup

print "Starting..."

file_name = 'book_list'
file_content = ''  # 最终要写到文件里的内容
file_content += 'Generate Time: ' + time.asctime()

hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
       { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

if len(sys.argv) == 1:
    print "You must input a parameter as the book name or the file name which contains names of all the books"
else:
    # url = http://book.douban.com/subject_search?search_text=bigdata&cat=1001
    # http://book.douban.com/subject_search?start=15&search_text=bigdata&cat=1001
    print("You are searching " + sys.argv[1])

print "End"