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
        return str(self.x)+'-'+str(self.y)
    
    def __repr__(self):
        return self.__str__()