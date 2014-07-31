'''
File Name: data.py
Course: 15640
Project: 4
@author: Tony Liu (andrewID: hualiu)
'''

from math import sqrt
import sys

class Data:
    def distance(self, anotherData):
        '''
        Compute the distance of two data point
        @param anotherData: another data to compare
        @return: return a double or int to represet
        '''
        pass
    
    def add(self, anotherData):
        '''
        Add to data with another data
        '''
        pass
    def avg(self, num):
        '''
        calculate the average
        '''

class Point(Data):
    def __init__(self):
        self.x = 0;
        self.y = 0;
        
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
        self.belongTo = -1;
        
    def distance(self, anotherPoint):
        return sqrt((self.x - anotherPoint.x)**2 + (self.y - anotherPoint.y)**2)
    
    def add(self, anotherPoint):
        self.x += anotherPoint.x
        self.y += anotherPoint.y
        
    def avg(self, num):
        if num == 0:
            self.x = 0;
            self.y = 0;
        else:
            self.x /= num
            self.y /= num
        
    def __str__(self):
        return str(self.x)+'-'+str(self.y)+':'+str(self.belongTo)
    
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return 0
    
class DNA(Data):
    def __init__(self, dna):
        self.data = dna
        self.belongTo = -1;
    def distance(self, anotherDNA):
        retval = 0
        for i in range(len(self.data)):
            if self.data[i] != anotherDNA.data[i]:
                retval += 1
        return retval
    def __str__(self):
        return str(self.data) + " " + str(self.belongTo)
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.data)
            
            
class DNACounter:
    def __init__(self, length):
        self.counter = [{'A': 0, 'C': 0 , 'G': 0, 'T' : 0}] * length
    def add(self, dna):
        for i in range(len(dna)):
            self.counter[i][dna.data[i]] += 1
    def addCounter(self,anotherCounter):
        for i in range(len(anotherCounter)):
            self.counter[i]['A'] += anotherCounter.counter[i]['A']
            self.counter[i]['C'] += anotherCounter.counter[i]['C']
            self.counter[i]['G'] += anotherCounter.counter[i]['G']
            self.counter[i]['T'] += anotherCounter.counter[i]['T']
    def avg(self, num):
        data = []
        for i in range(len(self.counter)):
            maxLetter = 'A'
            maxFrequence = 0
            for key in self.counter[i].keys():
                if self.counter[i][key] > maxFrequence:
                    maxLetter = key
                    maxFrequence = self.counter[i][key]
            data.append(maxLetter)
        return DNA(data)
    def __str__(self):
        return str(self.counter)
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.counter)
