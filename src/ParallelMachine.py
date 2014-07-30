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
import sys

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

def constructLocalSum(type, numOfCluster):
    '''
    Construct local sum object. E.G. [[PointSum, numberInThisCluster], [PointSum, numberInThisCluster]]
    PointSum is the point representation of sum in each cluster
    @param  type: type of the data
    @param numOfCluster: number of cluster
    @return: an initial localSum list  
    '''
    i = 0;
    local = [];
    initSum = [];
    while i < numOfCluster:
        if type == 'point':
            initSum = [Point(0,0), 0]
        elif type == 'DNA':
            pass #not implemented yet
        local.append(initSum)
        i += 1
    return local;

def toCluster(data, centroid):
    '''
    calculate the distance between the data and each of the centroid
    @param data: one data item
    @param centroid: current centroid list
    @return: index of centroid
    '''
    minIndex = 0
    minVal = sys.float_info.max
    for i in range(len(centroid)):
        tmp = data.distance(centroid[i])
        if(tmp < minVal):
            minVal = tmp
            minIndex = i
    return minIndex

def reCalculateCentroid(localSum, numOfCluster):
    '''
    node 0 recalculate the centroid array
    @param localSum: the data gathered from other nodes
    @param numOfCluster: the number of final cluster
    @return: newly constructed centroid list
    '''
    for i in range(len(localSum)):
        if i == 0:
            continue
        else:
            for j in range(numOfCluster):
                localSum[0][j][0].add(localSum[i][j][0])
                localSum[0][j][1] += (localSum[i][j][1])
    i = 0;
    centroid = [];
    while i < numOfCluster:
        localSum[0][i][0].avg(localSum[0][i][1])
        centroid.append(localSum[0][i][0])
        i += 1
    return centroid
    
def isProceed(percentage, threshold): 
    '''
    decide if to proceed
    @param percentage: list, reclustering data from each node
    @param threshold: user set threshold
    @return: true if need to proceed, false if not  
    '''
    sum = 0.0
    for i in range(len(percentage)):
        sum += percentage[i]
    if sum / len(percentage) > threshold:
        return True
    else:
        return False
##### end of helper function definitions #####

###################### main routine ############################

#get COMMandline INPUT_FILE, currently hard code
NUM_OF_CLUSTER = 2
INPUT_FILE = 'test.data'
TYPE_OF_DATA = 'point' #can be point or DNA
THRESHOLD = 0.05 # when that amount of data does not move, the iteration stops

#get MPI attributes
SIZE = MPI.COMM_WORLD.Get_size()
RANK = MPI.COMM_WORLD.Get_rank()
COMM = MPI.COMM_WORLD

#initialize time
startTime = time.time()

####### read in data from file #######
currentRank = 0
splitLength = 0 #calLineForEachProcessor(lineOfData, size)

#DataSet 
dataset = []

while currentRank < SIZE:
    if currentRank == RANK: #assign job to different node
        lineNo = currentRank + 1;
        lineCount = 0
        while True:
            line = linecache.getline(INPUT_FILE, lineNo)
            if line == '':
                break
            data = processLine(line, TYPE_OF_DATA)    #construct data from file
            dataset.append(data)    #add to dataset
            lineCount += 1
            lineNo += SIZE
        splitLength = lineCount       
    currentRank += 1
print 'processor',RANK,'data is',dataset
####### end of read in data from file #######

####### node 0 broadcast the centroid as the first k observations #######
#centroid list
centroid = []

if RANK == 0:
    centroid = dataset[:NUM_OF_CLUSTER]
else:
    centroid = None

centroid = COMM.bcast(centroid, root = 0)

print 'processor',RANK,"centroid is",centroid
####### initial centroid is ready #######

####### iterate calculation #######

proceed = True
while proceed:
    #init variable
    localSum = constructLocalSum(TYPE_OF_DATA, NUM_OF_CLUSTER)
    numOfRecluster = 0.0
    #calculate cluster belonging locally
    for data in dataset:
        belong = toCluster(data, centroid)
        if data.belongTo != belong:
            numOfRecluster += 1
            data.belongTo = belong
        localSum[belong][0].add(data)
        localSum[belong][1] += 1
    print "Processor", RANK, "localSum", localSum
    
    #send numOfRecluster to node 0 and determine if we need to proceed
    numOfRecluster /= splitLength
    numOfRecluster = COMM.gather(numOfRecluster, root=0)
    if RANK == 0:
        proceed = isProceed(numOfRecluster, THRESHOLD)
    else:
        proceed = None
    proceed = COMM.bcast(proceed, root = 0)
        
    if proceed is True:
        #send localSum to node 0 and recalculate the centroid, broadcast new centroid
        localSum = COMM.gather(localSum, root=0)
        if RANK == 0:
            print 'processor',RANK,'receive',localSum
            centroid = reCalculateCentroid(localSum, NUM_OF_CLUSTER)
            print 'new centroid is:',centroid
        else:
            centroid = None
        centroid = COMM.bcast(centroid, root = 0)
    else:
        break

print 'processor',RANK,'data:',dataset
print 'start time',startTime