# -*- coding: UTF-8 -*-

import bloom_filter
import sys

# 把str编码由默认ascii（python2为ascii，python3为utf8）改为utf8
reload(sys)
sys.setdefaultencoding('utf8')

"""
Merge book list files into one, using bloom filter to remove duplicate books
"""

def main():
	file_name = 'book_list'
	bf = bloom_filter.BloomFilter(2000,14)
	with open(file_name, 'a') as fn:
		for i in range(len(sys.argv)):
			if i > 0:
				with open(sys.argv[i]) as f:
					for line in f.readlines():
						if line != '\n' and bf.add(line.strip()) == False:
							fn.write(line.strip() + '\n')


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "必须输入至少两个参数(书籍列表文件)"
	else:
		main()