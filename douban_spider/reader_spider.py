# -*- coding: UTF-8 -*-

import sys
import time
import threading
import requests
from bs4 import BeautifulSoup
from progressbar import *
import fcntl
import random

# 把str编码由默认ascii（python2为ascii，python3为utf8）改为utf8
reload(sys)
sys.setdefaultencoding('utf8')

thread_num = 5		#线程个数
scaned_book = 0 	#完成抓取读者的书数目
totle_book = 0



class GetReaderThread(threading.Thread):
	def __init__(self, my_book_list, pbar):
		super(GetReaderThread, self).__init__()
		self.book_list = my_book_list
		self.readers = []
		self.scaned_num = 0
		self.item_each_page = 20 	#每一页展示书籍数目
		self.totle_reader = 0
		self.totle_valid = 0
		self.pbar = pbar

	def run(self):
		for book in self.book_list:
			current_page = 1
			self.totle_reader = 0
			self.totle_valid = 0

			book_info = book.strip().split('*$*', 3)

			while True:
				self.get_reader(book_info[0], book_info[1], book_info[2], current_page)
				if self.totle_reader != 0:
					current_page += 1
				if self.scaned_num >= self.totle_reader:
					break
				if current_page * self.item_each_page >= self.totle_reader:
					break
				time.sleep(3)
			scaned_num = 0	#reset scaned_num

		self.write_file(self.readers)
		global scaned_book
		global totle_book
		scaned_book += 1
		self.pbar.update(float(scaned_book) * 100 / float(totle_book))


	def get_reader(self, book_name, book_url, book_rating, current_page):
		url = book_url + 'collections?start={page}'
		hds = [{'User-Agent':'Baiduspider+(+http://www.baidu.com/search/spider.html)'}, 
			{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
			{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}, 
			{'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0'}, 
			{'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)'}, 
			{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER'}, 
			{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'}, 
			{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0'}]
		
		current_url = url.format(page = (current_page - 1) * self.item_each_page)

		source_code = requests.get(current_url, headers=hds[random.randint(0, 9)])
		if source_code.status_code != requests.codes.ok:
			print "Get response: " + source_code.status_code

		plain_text = source_code.text
		soup = BeautifulSoup(plain_text, "html.parser")

		#计算读者人数
		span_content = soup.find('span', id='collections_bar')

		if span_content:
			if self.totle_valid == 0:
				totle_str = span_content.span.string.strip()
				number = int(filter(str.isdigit, totle_str.encode('utf8')))
				if number >= 1:
					self.totle_reader = number
					self.totle_valid = 1

		#统计读者信息
		div_content = soup.find('div', id='collections_tab')
		if div_content.find('div', class_='sub_ins'):
			
			trs = div_content.find('div', attrs={'class': 'sub_ins'}).findAll('tr', class_="")
			for tr in trs:
				reader_dic = {}
				reader_dic['book_name'] = book_name
				reader_dic['book_rating'] = book_rating
				reader_dic['reader_href'] = tr.find('td', attrs={'width': '80'}).a['href']
				reader_dic['reader_name'] = tr.find('td', attrs={'width': '80'}).a.img['alt']
				reader_dic['reader_review'] = tr.find('p', attrs={'class': ''}).string.strip()
				self.readers.append(reader_dic)

			self.scaned_num += 1

	def write_file(self, readers):
		file_name = 'reader_list'
		file_content = ''

		for reader in readers:
			reader_info = reader['book_name'] + "*$*" + reader['book_rating'] + "*$*" + reader['reader_name'] + "*$*" + reader['reader_href'] + "*$*" + reader['reader_review']
			file_content += "%s\n" % reader_info


		with open(file_name, 'a') as f:
			fcntl.flock(f, fcntl.LOCK_EX)
			f.write(file_content)
			fcntl.flock(f, fcntl.LOCK_UN)


def read_book_list(filename):
	global totle_book
	book_list = [[] for i in range(thread_num)]
	i = 0
	with open(filename) as f:
		for line in f.readlines():
			n = i % thread_num
			if line != '\n':
				book_list[n].append(line.strip())
				totle_book += 1
				i += 1
	return book_list


def main():
	print "=============================="
	print "搜索读过书籍列表里书籍的读者"
	print "Generate time: " + time.asctime()
	print "=============================="

	pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()
	book_list = read_book_list(sys.argv[1])
	thread_pool = []
	for n in range(thread_num):
		if book_list[n] is not None:
			t = GetReaderThread(book_list[n], pbar)
			thread_pool.append(t)
			t.setDaemon(True)
			t.start()
	for t in thread_pool:
		t.join()

	pbar.finish()
	print "Completed! The readers are saved in 'reader_list'"


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print "必须输入至少一个参数(书籍列表文件)"
	else:
		main()