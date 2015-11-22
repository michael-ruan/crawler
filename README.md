# crawler

`crawler` is a crawler program that using `BeautifulSoup` and `urllib2`.
I use it to catch information from www.douban.com (豆瓣) and www.zhihu.com (知乎).

`douban_spider/book_spider.py` is the crawler program to get book list for a particular the keyword. It needs one parameter, for example, `$python book_spider.py bigdata`, and the result is saved in file named `book_list_bigdata`.

`douban_spider/bloom_filter.py` is a simple bloom filter, it needs two parameters, `size of bit array` and `number of probes`. For more information, please look at `main()` function inside it.

`douban_spider/merge_book_lists.py` is a script to remove duplicate books usring bloom_filter, you can use it like this `$python merge_book_lists.py book_list_bigdata book_list_data`. The result is saved in file named `book_list`.

`douban_spider/reader_spider.py` is the core crawler program to get all the readers who have read at least one book shown in the book list, that is given by the parameter. Use it like this `$python reader_spider.py book_list`.

## Contributor
[Michael Ruan](http://www.linkedin.com/profile/view?id=218589527&trk=nav_responsive_tab_profile_pic) (阮崇鹤)

## Copyright & License

    The MIT License (MIT)

    Copyright (c) 2014 Chonghe Ruan

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

