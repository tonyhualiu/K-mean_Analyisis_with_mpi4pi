'''
Created on Jul 28, 2014

@author: AndyDu
'''
import random
import time

#########################
# Deal with loading data from files
#########################

def loadCSV (filename):
    '''
    given a filename, load in a CSV file
    '''
    fileReader = open(filename, "r+")
    lines = fileReader.readlines()
    fileReader.close()

    dataArray = []
    for line in lines:
        data = convertToTuple(line)
        dataArray.append(data)
    return dataArray


def convertToTuple(line):
    '''
    convert line to tuple 
    '''
    # get rid of leading and trailing space
    line = line.strip()
    dataArray = line.split(",")
    # convert string to number
    for i in range(len(dataArray)):
        dataArray[i] = float(dataArray[i])


##########################
# This section implements the k-means algorithm using sequential approach
##########################


def kmeans(k, sampleData, startingCentroids=None):
    '''
    given the number of k, the sample group of data and initial centroids
    the method will calculate the k means
    '''
    result = {}
    # initialize centroids for the first phase
    if (startingCentroids == None or len(startingCentroids) < k):
        random.seed()
        centroids = random.sample(sampleData, k)
    # if this is not the first round of calculation, use the passed in centriods
    else:
        centroids = startingCentroids
    # 
    clusters = []
    for i in range(k):
        clusters.append([])
    
    # 
    clusters[0] = sampleData
    
    # start iteration
    iterationCounter = 0
    previousRoundOfCentroids = []
    while (centroids != previousRoundOfCentroids):
        clusters = reformCluster(sampleData, centroids)
        iterationCounter = iterationCounter + 1 
        
        # 
        previousRoundOfCentroids = centroids
        centroids = getCentroids(clusters)
        #
        threshold = 0
        for i in range(len(centroids)):
            centroid = centroids[i]
            cluster = clusters[i]
            for item in cluster:
                threshold += computeDistance(centroid, item)
        
    result["clusters"] = clusters
    result["centroids"] = centroids
    result["threshold"] = threshold
    return result

def reformCluster(sampleData, centroids):
    # reformCluster the list of lists to store all the data
    clusters = []
    for i in range(len(centroids)):
        clusters.append([])
    # calculate and determine which centroid is the right one
    for data in sampleData:
        # find which cluster the data belongs to 
        clusterIndex = findMinDistanceIndex(data, centroids)
        clusters[clusterIndex].append(data)     
    return clusters
              
       
def findMinDistanceIndex(point, centroids):
    # initialize minimum
    minDistance = computeDistance(point, centroids[0])
    index = 0
    for i in range(1, len(centroids)):
        tmp = computeDistance(point, centroids[i])
        if (tmp < min):
            minDistance = tmp
            index = i
    return index

def getCentroids (clusters):
    centroids = []
    for i in range(len(clusters)):
        centroid = getMeanForOneCluster(clusters[i])
        centroids.append(centroid)
    return centroids
    
def getMeanForOneCluster (list):
    # corner case
    if (len(list) == 0):
        return
    # 
    numOfAttributes = len(list[0])
    means = [0] * (numOfAttributes - 1)
    #
    for item in list:
        for i in range(1, numOfAttributes):
            means[i] = means[i] + item[i]
    #         
    for j in range(1, numOfAttributes):
        means[j] = means[j] / float(len(list))
    return tuple(means)

def computeDistance (pointOne, pointTwo):
    # corner case
    if pointOne == None or pointTwo == None:
        return float("inf")
    # normal form
    result = 0
    for i in range(1, len(pointOne)):
        result = result + (pointOne[i] - pointTwo[i]) ** 2
    return result


    
### Testing code ###
dataset = loadCSV("./test_2D_points.txt")
clusters = kmeans(3, dataset)
print clusters["clusters"]
print clusters["centroids"]
print clusters["threshold"]
