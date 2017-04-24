#from calClusterSize import *
import numpy as np
import random
import pickle
import copy 
from mpi4py import MPI 
from timeit import Timer 
import time 
import math
comm = MPI.COMM_WORLD

#Number of threads
size = comm.Get_size()

#Thread number
rank = comm.Get_rank()
 
#count for the set 
count = 0
#assign year here 
year = 0
#assign week here 
week = 1

graphTest = pickle.load(open("graphTester", 'r'))


#Nodes returned are bunch of sets representing the graph
	
clusterNodes = {}


'''
def transpose(transList):
	copyList = []
	for i in range(len(transList)):
		tmp = [transList[j][i] for j in range(len(transList))]		
		copyList.append(tmp)
	return copyList		

def createAdjacency(subGraph, i):
	#Adjacency list of list (0, 1) to represent presence or absence of an edge;  Also, its upper triangular
	global subAdjList 
	#copy
	global ogAdjList
 
	subAdjList = []
	ogAdjList = []
	#nodeList contains the graph nodes associated with the particular index in Adjacency; again list-of-list
	global nodeList
	#copy 
	global ogNodeList
	nodeList = []
	ogNodeList = []
	for j in range(len(graphTest[i])):
		subAdjList.append(list(graphTest[i][j]))
#		ogAdjList.append(list(graphTest[i][j]))
	#create a workable copy for the adjacency matrix
	for i in subGraph:
		nodeList.append([i])
		ogNodeList.append([i])
'''
def permute(graphAdjList, index1, index2):
	tmp = graphAdjList[index1]
	graphAdjList[index1] = graphAdjList[index2]
	graphAdjList[index2] = tmp
	tmp = [graphAdjList[i][index1] for i in range(len(graphAdjList))]
	for i in range(len(graphAdjList)):
		graphAdjList[i][index1] = graphAdjList[i][index2]
		graphAdjList[i][index2] = tmp[i]


def convert(i):
	for key in range(len(ogNodeList)):
		if (i in ogNodeList[key]):
			return key

def cutSetCount(nodeList):
	global ogAdjList
	count = 0
	for i in nodeList[0]:
		for j in nodeList[1]:
			index1 = convert(i); index2 = convert(j)
			if (ogAdjList[index1][index2] == 1):
				count = count + 1
	return count 

		
def karger(n):
	global subAdjList
	global nodeList
	if (n>6):
		ki = math.ceil(n/np.sqrt(2)) + 1
	else :	
		ki = 2

	while (len(subAdjList) > ki):
#	if (1):
		#Selecting two nodes to collapse
		global i, j
		sumTotal = sum([sum(subAdjList[i]) for i in range(len(subAdjList))])/2
#		print sumTotal
		randInt = random.randint(1, sumTotal)
#		print randInt
		sumOfEle = 0
		flag = 0
		for i in range(len(subAdjList)):
			j = i+1 
			while (j < len(subAdjList)):
				if (subAdjList[i][j] >= 1):
					sumOfEle = sumOfEle + subAdjList[i][j]
					if (sumOfEle >= randInt):
						flag = 1
						break 
				j = j +1
			if (flag == 1):
				break	
#		print ogAdjList 
#		print i, j

		# (i, j) are the two nodes to be collapsed

		# jth node is shifted below ith node to make the whole operation easier
#		print subAdjList 
		if (j!=i+1):
			permute(subAdjList, i+1, j)
		for k in range(len(subAdjList[0])):
			subAdjList[i][k] = subAdjList[i][k] + subAdjList[i+1][k]
		subAdjList.pop(i+1)
		for k in range(len(subAdjList)):
			subAdjList[k][i] = subAdjList[k][i] + subAdjList[k][i+1]
			subAdjList[k].pop(i+1)
#			print subAdjList[k]
		subAdjList[i][i] = 0
#		print subAdjList 	
#		update graphNodes
		for nodes in nodeList[j]:
			nodeList[i].append(nodes)
		nodeList.remove(nodeList[j])
	if (n>6):
		levelCopyAdj = copy.deepcopy(subAdjList)
		levelCopyNodes = copy.deepcopy(nodeList)
		r1 = karger(ki) 
		subAdjList = copy.deepcopy(levelCopyAdj)
		nodeList = copy.deepcopy(levelCopyNodes)
		r2 = karger(ki)
		return min(r1, r2)
	else: 
		setCount = cutSetCount(nodeList)
		return setCount 			


'''
def HCS(subGraph):
#Create copy of the nodeList 
	H, HExc, Clen = krager(subGraph)
	if (Clen > len(subGraph)/2) :
		clusterNodes.add(subGraph)
	else :
		createAdjacency(subGraph, year, week)
		HCS(H)
		createAdjacency(subGraph, year, week)
		HCS(HExc)

for key in graphNodes :
	if (len(graphNodes[key])>2):
		createAdjacency(graphNodes)
		HCS(graphNodes)
		H, HExc, cutSet = krager(graphNodes[key])
	else :
		clusterNodes[count] = graphNodes[key]
		count = count + 1

'''

iterations = {}
timeAvg = {}

for indexi in range(10):
	t1 = t2 =0
	complexityList = []
	timeList = []
	ogAdjList = []
	ogNodeList = []
	graphSize = len(graphTest[indexi])
	graphNodes = range(graphSize)	
	cutSet = np.load(open("cutSet"))
	ogAdjList = copy.deepcopy(graphTest[indexi])
	permute(ogAdjList, 0, graphSize-1)
	permute(ogAdjList, 1, graphSize-2)
	#permute(ogAdjList, 2, graphSize-3)
	for i in range(graphSize):
		ogNodeList.append([i])  
	if  (rank <= size-2):
		for count in range(20):
			c1 = 0
			while (1):
	#		if (1):
				#list to set conversion
				subAdjList = [] ; nodeList = []
				subAdjList = copy.deepcopy(ogAdjList)
				nodeList = copy.deepcopy(ogNodeList)
				nodewa = karger(len(subAdjList))
				if (nodewa == cutSet[indexi]):	
					print c1
					comm.send(c1, dest=size-1, tag=11)
					break
				c1 = c1 + 1
#			print count 
		req = comm.irecv(tag=11)
		req.wait()
#		print "recv", indexi
	elif (rank == size-1) :
		while(len(complexityList) <= 99):
#			tmp = comm.recv(tag=11)	
#			print len(complexityList)
			complexityList.append(comm.recv(tag=11))
#			timeList.append(tmp[1])
#		iterations = np.load(open("IterationCount"))
		print "completed"
#		timeAvg[graphSize] = np.average(timeList)		
		iterations[indexi] = complexityList
		#synchronize the 5 threads
		req = comm.isend(1, dest=0, tag=11)
		req = comm.isend(1, dest=1, tag=11)
		req = comm.isend(1, dest=2, tag=11)
		req = comm.isend(1, dest=3, tag=11)
		req = comm.isend(1, dest=4, tag=11)



#pickle.dump(timeAvg, open("timePerIteration", 'w'), pickle.HIGHEST_PROTOCOL)
#pickle.dump(iterations, open("TempIterations", 'w'), pickle.HIGHEST_PROTOCOL) 
pickle.dump(iterations, open("IterationCountStein", 'w'), pickle.HIGHEST_PROTOCOL)	
