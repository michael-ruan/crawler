# -*- coding: UTF-8 -*-

import sys
import time
import requests
from bs4 import BeautifulSoup
from progressbar import *

# 把str编码由默认ascii（python2为ascii，python3为utf8）改为utf8
reload(sys)
sys.setdefaultencoding('utf8')


current_page = 1 	#当前页数
num_each_page = 15 	#每一页展示书籍数目
url = "http://book.douban.com/subject_search?start={page}&search_text={key}&cat=1001"
data = []
totle = 0 			#总书籍数目
totle_valid = 0 	#计算总书籍数目标志，若为1，则表示已计算，下次不用再计算
scaned_num = 0 		#已抓取数目


def get_page(current_page):
	global totle
	global totle_valid
	global scaned_num
	hds = [{'User-Agent':'Baiduspider+(+http://www.baidu.com/search/spider.html)'}, 
	{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'},
	{'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
	{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
		
	current_url = url.format(page = (current_page - 1) * num_each_page, key = sys.argv[1])

	source_code = requests.get(current_url, headers=hds[current_page % 4])
	if source_code.status_code != requests.codes.ok:
		print "Get response: " + source_code.status_code

	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, "html.parser")

	div = soup.find('div', id='content')

	if div.find('div', class_='trr'):
		if totle_valid == 0:
			totle_str = div.find('div', {'class', 'trr'}).string.strip()
			number = int(totle_str.encode('utf8').split("共", 1)[-1])
			if number >= 1:
				totle = number
				totle_valid = 1

	book_list = div.findAll('li', class_="subject-item")

	book_info = []
	for book in book_list:
		book_dic = {}
		if book.find('div', attrs={'class': 'info'}):
			my_div = book.find('div', {'class': 'info'})
			book_dic['book_name'] = my_div.h2.a['title']	#书名
			book_dic['book_href'] = my_div.h2.a['href']		#书链接

			if my_div.find('span', attrs={'class': 'rating_nums'}):
				book_dic['book_rating'] = my_div.find('span', {'class': 'rating_nums'}).string.strip()	#书评分
			else:
				book_dic['book_rating'] = 0

			#书的评论
			# if my_div.find('span', attrs={'class': 'pl'}):
			# book_dic['book_stars'] = my_div.find('span', attrs={'class': 'pl'}).string.strip()

		scaned_num += 1

		book_info.append(book_dic)
		write_file(book_dic['book_name'] + "*$*" + book_dic['book_href'] + "*$*" + str(book_dic['book_rating']) ) 



def write_file(book_info):
	file_name = 'book_list_' + sys.argv[1]
	file_content = ''
	file_content += "%s\n" % book_info
		
	f = open(file_name, 'a')
	f.write(file_content)
	f.close()
		

def start():
	global current_page

	pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()
	while True:
		get_page(current_page)
		time.sleep(5)
		pbar.update(float(scaned_num) / float(totle) * 100)
		
		if totle != 0:
			current_page += 1
		if scaned_num >= totle:
			break
		if current_page >= totle:
			break

	pbar.finish()


def main():
	print "=============================="
	print "搜索关键词为" + sys.argv[1] + "的书籍"
	print "生成时间：" + time.asctime()
	print "=============================="

	start()



if __name__ == '__main__':
	if len(sys.argv) == 1:
		print "必须输入一个参数(关键词)"
	else:
		main()