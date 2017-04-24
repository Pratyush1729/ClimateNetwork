from calClusterSize import *
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

#graphTest = pickle.load(open("graphTester", 'r'))


#Nodes returned are bunch of sets representing the graph
graphNodes = calClusterForYear(year, week)	
clusterNodes = {}
graphAdj = np.load(open("tempGraph"))


def transpose(transList):
	copyList = []
	for i in range(len(transList)):
		tmp = [transList[j][i] for j in range(len(transList))]		
		copyList.append(tmp)
	return copyList		



def createAdjacency(subGraph):
	#Adjacency list of list (0, 1) to represent presence or absence of an edge;  Also, its upper triangular
	global ogAdjList 
	#nodeList contains the graph nodes associated with the particular index in Adjacency; again list-of-list
	global ogNodeList
	ogNodeList = []
	ogAdjList = []
	count=0
	graphList = list(subGraph)
	graphList.sort()
	for i in graphList:
		tmp1 = list(graphAdj[i].intersection(subGraph))
		tmp2 = []
		for j in graphList:
			if (j in tmp1):
				tmp2.append(1)
			else :
				tmp2.append(0)
		ogAdjList.append(tmp2)
	tempTrans = transpose(ogAdjList)
	for i in range(len(tempTrans)):
		for j in range(len(tempTrans)):
			ogAdjList[i][j] = ogAdjList[i][j] + tempTrans[i][j]
	for i in graphList:
		ogNodeList.append([i])


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
		if (r1[0] > r2[0]):
			return r2
		else :
			return r1
	else: 
		setCount = cutSetCount(nodeList)
		return [nodeList[0], nodeList[1], setCount] 			


def run_karger(graphSize):
	#Set an appropriate value for iterCount
	if  (rank >= 2):
		iterCount = math.ceil(math.log(graphSize)*math.log(graphSize))
		iterPerThread = int(math.ceil(iterCount/(size-2.0)))
		minCut = [0, 0, 100]
		global subAdjList ; global nodeList 
		print iterPerThread
		for _ in range(iterPerThread):
			#list to set conversion
			subAdjList = [] ; nodeList = []
			subAdjList = copy.deepcopy(ogAdjList)
			nodeList = copy.deepcopy(ogNodeList)
			#karger returns H, HExc, cutSet 
			nodewa = karger(len(subAdjList))
			if (nodewa[2] < minCut[2]):
				minCut = nodewa
		comm.send(minCut, dest=1, tag=11)	
	elif (rank == 1):
		minCutThreads = []
		for thread in range(size):
			tmp = comm.recv(tag=11)
			minCutThreads.append(tmp)	
		newMin = [0, 0, 100]
		for minThread in minCutThreads:
			if (minThread[2] < newMin[2]):
				newMin = minThread
		comm.send(newMin, dest=0, tag=11)

def HCS(subGraph):
#Create copy of the nodeList 
#	tmp = run_krager(len(subGraph))
	for i in np.arange(2, size):
		comm.send(subGraph, dest=i, tag=11)
	tmp = comm.recv(source=1, tag=11)
	[H, HExc, Clen] = [set(tmp[0]), set(tmp[1]), tmp[2]]
	if (Clen > len(subGraph)/2) :
		print clusterNodes
		clusterNodes.add(subGraph)
	else :
		HCS(H)
		HCS(HExc)


print "start"
#Main 
if (rank == 0):
	for key in graphNodes :
		if (len(graphNodes[key])>2):
			print key
			HCS(graphNodes[key])
if (rank > 1):
	subGraph = comm.recv(tag=11)
	createAdjacency(subGraph)
	run_karger(len(subGraph))

elif (rank==1):
	run_karger(0)
