'''
File Name: ParallelMachine.py
Course: 15619
Project: 4
@author: Tony Liu (andrewID: hualiu)
'''

from data import *
from mpi4py import MPI 
import time
import linecache

##### helper function definitions #####
'''
def formatTime second:
    
    format the seconds into
    XX minutes XX seconds
    @param param: time in second
    @return: string after formatted
    
'''

def calLineForEachProcessor (lineOfData, size):
    '''
    calculate how many lines for one processor to read in
    @param lineOfData: how many lines in total
    @param size: how many processors
    @return: the length for each processor
    '''
    lineOfData += lineOfData % size
    return lineOfData / size

def processLine (line, type):
    '''
    read in one line and transform it into Data
    @param line: line in the csv file
    @param type: type of data
    @return: one data item
    '''
    line = line.split(',')
    if type == 'point':
        return Point(double(line[0]), double(line[1]))
    elif type == 'DNA':
        return None #not implemented yet

###################### main routine ############################

#get commandline input, currently hard code
numOfCluster = 2
lineOfData = 10
input = 'test.data'
typeOfData = 'point' #can be point or DNA

#get MPI attributes
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()

#initialize time
startTime = time.time()

#read in file
currentRank = 0
splitLength = calLineForEachProcessor(lineOfData, size)

#DataSet 
dataset = []

while currentRank < size:
    if currentRank == rank: #assign job to different node
        lineNo = 1;
        while lineNo <= splitLength:
            line = linecache.getline(input, lineno)
            if line == '':
                break
            data = processLine(line, typeOfData)
            
    currentRank++
        
        

p1 = Point(2, 2)
p2 = Point(2, 3)

p1.belongto = 1

print startTime