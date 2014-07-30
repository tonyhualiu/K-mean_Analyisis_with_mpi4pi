'''
Created on Jul 28, 2014

@author: AndyDu
'''
import random
import time

#########################
# Deal with loading data from files
#########################

def loadDNA (filename):
    '''
    given a filename, load in a DNA file
    '''
    fileReader = open(filename, "r+")
    lines = fileReader.readlines()
    fileReader.close()
    
    dataArray = []
    for line in lines:
        line = line.strip()
        dataArray.append(line)
    return dataArray

# def convertToTuple(line):
#     '''
#     convert line to tuple 
#     '''
#     # get rid of leading and trailing space
#     line = line.strip()
#     dataArray = line.split(",")
#     # convert string to number
#     for i in range(len(dataArray)):
#         dataArray[i] = float(dataArray[i])
    # return dataArray


##########################
# This section implements the k-means algorithm using sequential approach
##########################

def kmeans (k, sampleDNAs, startingCentroids = None):
    '''
    given the number of k, the sample group of data and initial centroids
    the method will caculate the k means
    '''

    result = {}
    # initialize centroids for the first phase
    if (startingCentroids == None or len(startingCentroids) < k):
        random.seed()
        centroids = random.sample(sampleDNAs, k)
    # if this is not the first phase of the calculation, used the previous centroids
    else:
        centroids = startingCentroids

    # allocating a new list of lists to store the DNA
    clusters = []
    for i in range(k):
        clusters.append([])
    # intialize by putting all the DNAs in the first cluster
    clusters[0] = sampleDNAs

    # start the iteration
    iterationCounter = 0
    previousRoundOfCentroids = []


    ###########
    print 'centroids, ', centroids
    type(centroids)
    print 'previousRoundOfCentroids, ', previousRoundOfCentroids
    type(previousRoundOfCentroids)
    ###########
    
    while (centroids != previousRoundOfCentroids):
        clusters = reformCluster(sampleDNAs, centroids)
        iterationCounter += 1
        #
        previousRoundOfCentroids = centroids
        centroids = getCentroids(clusters)
        #
        threshold = 0
        for i in range(len(centroids)):
            centroid = centroids[i]
            cluster = clusters[i]

            for item in cluster:
                threshold += computeDiff(centroid, item)

    result["clusters"] = clusters
    result["centroids"] = centroids
    result["threshold"] = threshold
    return result 

def reformCluster(sampleDNAs, centroids):
    clusters = []
    # initialize the clusters storage
    for i in range(len(centroids)):
        clusters.append([])
    # calculate which centroid is the right one
    for DNA in sampleDNAs:
        clusterIndex = findMinDiffIndex(DNA, centroids)
        clusters[clusterIndex].append(DNA)
    return clusters

def findMinDiffIndex(DNA, centroids):
    # initialize the minimum
    
    minDiff = computeDiff(DNA, centroids[0])
    index = 0
    for i in range(1, len(centroids)):
        tmp = computeDiff(DNA, centroids[i])
        if tmp < minDiff:
            minDiff = tmp
            index = i
    return index

def computeDiff(DNAone, DNAtwo):
    # corner case
    if DNAone == None or DNAtwo == None:
        return float("inf")
    # compute the difference by compare each position of the DNA
    # DNAone and DNAtwo should be string, such as 'ACGTTCGA'
    listOne = list(DNAone)
    listTwo = list(DNAtwo)
    # DNA strands is in same length, according to requirement of this assignment
    diffCounter = 0
    for i in range(len(listOne)):
        # print i
        if listOne[i] != listTwo[i]:
            diffCounter += 1
    return diffCounter



def getCentroids(clusters):
    centroids = []
    for i in range(len(clusters)):
        centroid = getMeanForOneCluster(clusters[i])
        centroids.append(centroid)
    return centroids


def getMeanForOneCluster(lists):
    # corner case
    if (len(lists)) == 0:
        return
    #
    means = []
    #
    arrayOfDNA = ['A', 'C', 'G', 'T']
    arrayOfCounter = [0] * 4

    for i in range(len(lists[0])):
        
        print i
        
        for item in lists:

            print 'item: ', item
            print 'item[i]', item[i]

            if item[i] in ('A'):
                arrayOfCounter[0] += 1
            elif item[i] in ('C'):
                arrayOfCounter[1] += 1
            elif item[i] in ('G'):
                arrayOfCounter[2] += 1
            elif item[i] in ('T'):
                arrayOfCounter[3] += 1
            
        print 'arrayofCounter: ', arrayOfCounter
        print 'max(arrayOfCounter): ', max(arrayOfCounter)
        mostOccured = arrayOfCounter.index(max(arrayOfCounter))
        print 'mostOccured: ', mostOccured
        
        print arrayOfDNA[mostOccured]
        means.append(arrayOfDNA[mostOccured])
        print 'means after append, ', means

    print 'means, ',    means
    return means
    
# ### Testing code ###
dataset = loadDNA("./output.txt")
clusters = kmeans(3, dataset)
print clusters
