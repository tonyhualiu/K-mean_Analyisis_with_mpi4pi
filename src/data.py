'''
File Name: data.py
Course: 15619
Project: 4
@author: Tony Liu (andrewID: hualiu)
'''

from math import sqrt

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
    

class Point(Data):
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
        
    def distance(self, anotherPoint):
        return sqrt((self.x - anotherPoint.x)**2 + (self.y - anotherPoint.y)**2)
    
    def add(self, anotherPoint):
        self.x += anotherPoint.x
        self.y += anotherPoint.y