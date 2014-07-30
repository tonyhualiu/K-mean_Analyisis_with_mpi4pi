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
    
class DNA(Data):
    def __init__(self, dna):
        self.data = dna
        self.counter = []
        for d in dna:
            c = DNACounter()
            c.increment(d)
            self.counter.append(c) 
    def distance(self, anotherDNA):
        retval = 0
        for i in range(len(self.data)):
            if self.data[i] != anotherDNA.data[i]:
                retval += 1
        return retval
    def add(self, anotherDNA):
        for i in range(len(self.data)):
            self.counter[i].increment(anotherDNA.data[i])
    def avg(self, num):
        for i in range(len(self.counter)):
            maxLetter = 'A'
            maxFrequence = 0
            for key in self.counter[i].counter.keys():
                if self.counter[i].counter[key] > maxFrequence:
                    maxLetter = key
                    maxFrequence = self.counter[i].counter[key]
            self.data[i] = maxLetter
    def __str__(self):
        return str(self.data)
    def __repr__(self):
        return self.__str__()
            
            
class DNACounter:
    def __init__(self):
        self.counter = {'A': 0, 'C': 0 , 'G': 0, 'T' : 0}
    def increment(self,letter):
        self.counter[letter] += 1
    def __str__(self):
        return str(self.counter)
    def __repr__(self):
        return self.__str__()
        
        
##test##
d1 = DNA(['A','C','G','T'])
d2 = DNA(['A','G','C','T'])
d3 = DNA(['A','G','C','A'])

#print d1.counter
#print d2.counter


print d1.distance(d2)

d1.add(d2)
d1.add(d3)
d1.avg(0)
print d1