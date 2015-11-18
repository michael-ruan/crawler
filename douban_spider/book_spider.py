# -*- coding: UTF-8 -*-

# 把str编码由默认ascii（python2为ascii，python3为utf8）改为utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import time
import urllib2
import requests
import re
from bs4 import BeautifulSoup
# import bs4


# class BookSpider(object):
# 	"""根据关键词抓取书籍信息"""

	# def __init__(self):
	# 	super(BookSpider, self).__init__()
	# 	self.current_page = 1
	# 	self.num_each_page = 15
	# 	self.url = "http://book.douban.com/subject_search?start={page}&search_text={key}&cat=1001"
	# 	self.data = []
	# 	self.totle = 0

current_page = 1
num_each_page = 15
url = "http://book.douban.com/subject_search?start={page}&search_text={key}&cat=1001"
data = []
totle = 0


def get_page(current_page):
	hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
	{ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
	{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
		
	current_url = url.format(page = (current_page - 1) * num_each_page, key = sys.argv[1])
	

	source_code = requests.get(current_url, headers = hds[current_page % 3])
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, "html.parser")

	# soup = BeautifulSoup(content, "html.parser")
	div = soup.find('div', id='content')
	if div.find('div', class_='trr'):
		totle_str = div.find('div', {'class', 'trr'}).string.strip()
		number = int(totle_str.encode('utf8').split("共", 1)[-1])
		if number >= 1
			totle = number
	book_list = div.findAll('li', class_="subject-item")

	book_info = []
	for book in book_list:
		valid = 0    #6分及10人评价以上的书籍置1
		book_dic = {}
		# my_div = book.find('div', attrs={'class': 'info'})
		if book.find('div', attrs={'class': 'info'}):
			my_div = book.find('div', {'class': 'info'})
			book_dic['book_name'] = my_div.h2.a['title']
			book_dic['book_href'] = my_div.h2.a['href']

			print book_dic['book_name']
			write_file(book_dic['book_name'])

			if my_div.find('span', attrs={'class': 'rating_nums'}):
				book_dic['book_rating'] = my_div.find('span', {'class': 'rating_nums'}).string.strip()
				print book_dic['book_rating']
				if float(book_dic['book_rating']) >= 6.0:
					valid = 1

			# if my_div.find('span', attrs={'class': 'pl'}):
			# book_dic['book_stars'] = my_div.find('span', attrs={'class': 'pl'}).string.strip()


		if valid == 1:
			book_info.append(book_dic)
			# print book_info
			# write_file(book_info)

		
def write_file(book_info):
	file_name = 'book_list'
	file_content = ''  # 最终要写到文件里的内容
	# file_content += "==============================\n"
	# file_content += "搜索关键词为" + sys.argv[1] + "的书籍\n"	
	# file_content += "只保留6分及10人评价以上的书籍\n"
	# file_content += "生成时间：" + time.asctime() + "\n"
	# file_content += "==============================\n"
	file_content += "%s\n" % book_info
		
	f = open(file_name, 'a')
	f.write(file_content)
	f.close()
		

def start():
	get_page(current_page)


def main():
	print "=============================="
	print "搜索关键词为" + sys.argv[1] + "的书籍"
	print "只保留6分及10人评价以上的书籍"
	print "生成时间：" + time.asctime()
	print "=============================="

	# book_spider = BookSpider()
	# book_spider.get_page(book_spider.current_page)
	# book_spider.start()
	start()



if __name__ == '__main__':
	if len(sys.argv) == 1:
		print "必须输入一个参数(关键词)"
	else:
		main()