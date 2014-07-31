'''
File Name: ParallelMachine.py
Course: 15640
Project: 4
@author: Tony Liu (andrewID: hualiu)
'''

from data import *
from mpi4py import MPI 
import time
import linecache
import sys

##### helper function definitions #####

def formatTime():
    return time.strftime("%Y-%m-%d_%H-%M-%S",time.gmtime())

def writeLog(event, logFile):
    '''
    format the seconds into
    XX minutes XX seconds
    @param msg: log message
    @param logPath: the path of logfile 
    '''
    logFile.write(formatTime() + '\t' + event)
    logFile.write('\n')


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
    if type == 'point':
        line = line.split(',')
        return Point(float(line[0]), float(line[1]))
    elif type == 'DNA':
        line = list(line.strip())
        return DNA(line)

def constructLocalSum(type, numOfCluster, lengthOfDNA):
    '''
    Construct local sum object. E.G. [[PointSum, numberInThisCluster], [PointSum, numberInThisCluster]]
    PointSum is the point representation of sum in each cluster
    @param  type: type of the data
    @param numOfCluster: number of cluster
    @param lengthOfDNA: the length of DNA 
    @return: an initial localSum list  
    '''
    i = 0;
    local = [];
    initSum = [];
    while i < numOfCluster:
        if type == 'point':
            initSum = [Point(0,0), 0]
        elif type == 'DNA':
            initSum = [DNACounter(lengthOfDNA),0]
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

def reCalculateCentroid(localSum, numOfCluster,dataType):
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
            if dataType == "point":
                for j in range(numOfCluster):
                    localSum[0][j][0].add(localSum[i][j][0])
                    localSum[0][j][1] += (localSum[i][j][1])
            elif dataType == "DNA":
                for j in range(numOfCluster):
                    localSum[0][j][0].addCounter(localSum[i][j][0])
    i = 0;
    centroid = [];
    while i < numOfCluster:
        rt = localSum[0][i][0].avg(localSum[0][i][1])
        if dataType == 'point':
            centroid.append(localSum[0][i][0])
        elif dataType == 'DNA':
            centroid.append(rt)
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


#get commandline: python foo.py <number_of_cluster> <input_path> <type_of_data> [threashold] [logpath] 


THRESHOLD = 0.000001
LOG_PATH = 'log_' + formatTime()

args = sys.argv[1:]
NUM_OF_CLUSTER = int(args[0])
INPUT_FILE =  args[1]
TYPE_OF_DATA = args[2]
if len(args) > 3: 
    THRESHOLD = float(args[3])
if len(args) > 4: 
    LOG_PATH = args[4]

log = open(LOG_PATH,"a")
#get MPI attributes
SIZE = MPI.COMM_WORLD.Get_size()
RANK = MPI.COMM_WORLD.Get_rank()
COMM = MPI.COMM_WORLD

#initialize log
writeLog("Command line parsed",log)
writeLog("Program start" ,log)
writeLog("Num_Of_Cluster = " + str(NUM_OF_CLUSTER) ,log)
writeLog("INPUT_FILE = " + INPUT_FILE ,log)
writeLog("TYPE_OF_DATA = " + TYPE_OF_DATA ,log)
writeLog("THRESHOLD = " + str(THRESHOLD) ,log)
writeLog("LOG_PATH = " + LOG_PATH ,log)
####### read in data from file #######
writeLog("Start reading data " ,log)

currentRank = 0
splitLength = 0 
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
    
writeLog("Finish reading data " ,log)
currentRank = None
####### end of read in data from file #######

####### node 0 broadcast the centroid as the first k observations #######
writeLog("Broadcasting centroids " ,log)
#centroid list
centroid = []

if RANK == 0:
    centroid = dataset[:NUM_OF_CLUSTER]
else:
    centroid = None

centroid = COMM.bcast(centroid, root = 0)
writeLog("Processor " + str(RANK) +" Initial Centroid is " + str(centroid) ,log)
writeLog("Finish broadcasting centroids " ,log)
####### initial centroid is ready #######

####### iterate calculation #######
writeLog("Start calculation " ,log)
proceed = True
while proceed:
    #init local sum and number of recluster
    localSum = constructLocalSum(TYPE_OF_DATA, NUM_OF_CLUSTER, len(dataset[0]))
    numOfRecluster = 0.0
    #calculate cluster belonging locally
    for data in dataset:
        belong = toCluster(data, centroid)
        if data.belongTo != belong:
            numOfRecluster += 1
            data.belongTo = belong
        localSum[belong][0].add(data)
        localSum[belong][1] += 1
    
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
            centroid = reCalculateCentroid(localSum, NUM_OF_CLUSTER, TYPE_OF_DATA)
        else:
            centroid = None
        centroid = COMM.bcast(centroid, root = 0)
    else:
        break
writeLog("Finish calculation " ,log)