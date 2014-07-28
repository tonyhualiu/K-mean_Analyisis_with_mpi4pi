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
        return Point(float(line[0]), float(line[1]))
    elif type == 'DNA':
        return None #not implemented yet

##### end of helper function definitions #####

###################### main routine ############################

#get commandline input, currently hard code
numOfCluster = 2
input = 'test.data'
typeOfData = 'point' #can be point or DNA
threshold = 0.05 # when that amount of data does not move, the iteration stops

#get MPI attributes
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
comm = MPI.COMM_WORLD

#initialize time
startTime = time.time()

####### read in data from file #######
currentRank = 0
splitLength = 0 #calLineForEachProcessor(lineOfData, size)

#DataSet 
dataset = []

while currentRank < size:
    if currentRank == rank: #assign job to different node
        lineNo = currentRank + 1;
        lineCount = 0
        while True:
            line = linecache.getline(input, lineNo)
            if line == '':
                break
            data = processLine(line, typeOfData)    #construct data from file
            dataset.append(data)    #add to dataset
            lineCount += 1
            lineNo += size
        splitLength = lineCount
        print dataset        
    currentRank += 1

####### end of read in data from file #######

####### node 0 broadcast the centroid as the first k observations #######
centroid = []

if rank == 0:
    centroid = dataset[:numOfCluster]
else:
    centroid = None

centroid = comm.bcast(centroid, root = 0)
####### initial centroid is ready #######

####### iterate calculation #######

#init some variables
sumOfClusterN = []
currentThreshold = 0.0
i = 0

while i < numOfCluster:
    sumOfClusterN.append(0)

while currentThreashold > threashold:
    

print 'centroid',centroid

print 'start time',startTime