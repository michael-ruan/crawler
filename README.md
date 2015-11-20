# crawler

`crawler` is a crawler program that using `BeautifulSoup` and `urllib2`.
I use it to catch information from www.douban.com (豆瓣) and www.zhihu.com (知乎).

`douban_spider/book_spider.py` is the crawler program to get book list for a particular the keyword. It needs one parameter, for example, `$python book_spider.py bigdata`.

`douban_spider/bloom_filter.py` is a simple bloom filter, it needs two parameters, `size of array` and `number of probes`.

## Contributor
[Michael Ruan](http://www.linkedin.com/profile/view?id=218589527&trk=nav_responsive_tab_profile_pic)

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

