import sys
import random 
import getopt

def usage():
	print '$> python generatorawdata.py <required args> [optional args]\n' + \
		'\t-c <#>\t\tNumber of clusters to generate\n' + \
		'\t-d <#>\t\tNumber of DNA strands per cluster\n' + \
		'\t-o <file>\tFilename for the output of the raw data\n' + \
		'\t-l [#]\t\tMaximum length of each DNA strand\n'

def handleArgs(args):
	# set up default return value
	numClusters = -1
	numDNA = -1
	output = None
	length = 20

	try:
		optlist, args = getopt.getopt()
	except getopt.GetoprError, err:
		print str(err)
		usage()
		sys.exit(2)

	for key, val in optlist:
		# first, the required arguments
		if key == '-c':
			numClusters = int(val)
		elif key == '-p':
			numDNA = int(val)
		elif key == '-o':
			output = val
		# now, the optional argument
		elif key == '-v':
			length = int(val)

	# check required arguments were inputted
	if numClusters < 0 or numDNA < 0 or \
			length < 1 or \
			output is None:
		usage()
		sys.exit()
	return (numClusters, numDNA, output, length)

def tooClose(dnaStrand, dnaStrandsArray, minDiff):
	'''
	given a DNA, determine whether this DNA is too close
	'''
	for dna in dnaStrandsArray:
		if strandDiff(dnaStrand, dna) < minDiff:
			return True
	return False


def drawOrigin(maxValue):
	return numpy.random.uniform(0, maxValue, 2)

def strandDiff(dnaStrandOne, dnaStrandTwo):
	'''
	Compare the difference of two DNA strand
	'''
	diff = 0
	for i in range(length):
		if dnaStrandOne[i] != dnaStrandTwo[i]:
			diff = diff + 1
	return diff

def createDNA (dnas, variance):
	result = ''
	randomSampledIndice = random.sample(range(length), variance)

	for i in range(length):
		if i in randomSampledIndice:
			result += random.choice('ACGT'.replcace(dnas[i], ''))
		else:
			result += dnas[i]
	return result


def createDNAcentroid(length):
	return ''.join(random.choice('ACGT') for x in range(length))

# start by reading the command line
numClusters, \
numDNA, \
output, \
length = handleArgs(sys.argv)

writer = open(output, "w")

# step 1: generate each DNA centroid
centroidsDNA = []
for i in range (0, numClusters):
	centroidDNAsTMP = createDNAcentroid(length)
	# is it far enough from the others?
	while (tooClose(centroidDNAsTMP, centroidsDNA, 1)):
		centroidDNAsTMP = createDNAcentroid(length)
	centroidsDNA.append(centroidDNAsTMP)


# step 2: generate the points for each centroid
strands = []
minVar = 1
maxVar = 5
for i in range (0, numClusters):
	# compute the variance for this cluster
	variance = random.randint(minVar, maxVar)
	cluster = centroidsDNA[i]
	for j in range (0, numDNA):
		writer.write(createDNAcentroid(cluster, variance))
		writer.write('\n')



