# -*- coding: UTF-8 -*-
"""Copyright 2015 Michael Ruan 
bloom filter library in python.
https://github.com/michael-ruan/crawler
"""

from BitVector import BitVector
import mmh3
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class BloomFilter(object):
    def __init__(self, array_size, hash_count):
        self.size = array_size                  #the size of bit array
        self.hash_count = hash_count            #the number of probes for each item
        self.bit_array = BitVector(size = array_size)

    def add(self, item):
        exist = True
        for seed in xrange(self.hash_count):
            result = mmh3.hash(item, seed) % self.size
            if self.bit_array[result] == 0:
                self.bit_array[result] = 1
                exist = False
        return exist

    def lookup(self, item):
        for seed in xrange(self.hash_count):
            result = mmh3.hash(item, seed) % self.size
            if self.bit_array[result] == 0:
                return False
        return True

    def __contains__(self, item):
        self.lookup(item)

    def __add__(self, bf):
        self.bit_array = self.bit_array | bf.bit_array
        return self

    def clear_all(self):
        self.bit_array.reset(0)

    def set_bit_array(self, ba):
        self.bit_array = ba

    def export_bloom(self, filename):
        with open(filename, 'wb') as f:
            f.write(str(self.size) + ":" + str(self.hash_count) + ":" + self.bit_array.get_bitvector_in_hex())


class CopyFromBloomFilter(BloomFilter):
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            line = f.read()
            content = line.strip().split(':')
            size = int(content[0])
            hash_count = int(content[1])
            bit_array = BitVector(hexstring = content[2])

            BloomFilter.__init__(self, size, hash_count)
            BloomFilter.set_bit_array(self, bit_array)


def main():
    #if there are 1000 items as n=1000, you can choose array_size=20*1000=20000
    #k=ln(2)*m/n is the best, so k=0.6931*20=14
    #error rate is 0.0000889
    bf1 = BloomFilter(20000,14)

    #Test
    print "bf1.add('apple'):    " + str(bf1.add('apple'))         #False
    print "bf1.add('apple'):    " + str(bf1.add('apple'))         #True
    print "bf1.lookup('apple'): " + str(bf1.lookup('apple'))      #True
    print "'apple' in bf1:      " + str('apple' in bf1)           #True
    print "bf1.lookup('pear'):  " + str(bf1.lookup('pear'))       #False
    print "'pear' in bf1:       " + str('pear' in bf1)            #False
    bf1.clear_all()
    print "bf1.add('apple'):    " + str(bf1.add('apple'))         #False
    bf1.export_bloom('mybloom')

    bf2 = BloomFilter(20000,14)
    print "bf2.add('tree'):     " + str(bf2.add('tree'))          #False
    print "bf2.lookup('apple'): " + str(bf2.lookup('apple'))      #False
    bf2 += bf1
    print "bf2.lookup('apple'): " + str(bf2.lookup('apple'))      #True

    bf3 = CopyFromBloomFilter('mybloom')
    print "bf3.add('apple'):    " + str(bf3.add('apple'))         #True

if __name__ == '__main__':
    main()