# -*- coding: UTF-8 -*-

from BitVector import BitVector
import mmh3
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MyBloomFilter(object):
    def __init__(self, array_size, hash_count):
        self.size = array_size                  #the size of array
        self.hash_count = hash_count            #the number of probes for each item
        self.bit_array = BitVector(size = array_size)


    def add(self, item):
        for seed in xrange(self.hash_count):
            result = mmh3.hash(item, seed) % self.size
            self.bit_array[result] = 1


    def lookup(self, item):
        for seed in xrange(self.hash_count):
            result = mmh3.hash(item, seed) % self.size
            if self.bit_array[result] == 0:
                return False
        return True