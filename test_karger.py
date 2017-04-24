#from calClusterSize import *
import numpy as np
import random
import pickle
import copy 
from mpi4py import MPI 

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
'''

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
		ogAdjList.append(list(graphTest[i][j]))
	#create a workable copy for the adjacency matrix
	for i in subGraph:
		nodeList.append([i])
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

def krager():
	while (len(subAdjList) > 2):
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
	setCount = cutSetCount(nodeList)
	return [nodeList, setCount] 			


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

complexityList = []

cutSet = np.load(open("cutSet"))
indexi = 8
#for iindexi in range(10):
if  (rank <= size-2):
	for count in range(20):
		c1 = 0
		while (1):
			#list to set conversion
			subAdjList = []
			ogAdjList = []
			graphSize = len(graphTest[indexi])
			graphNodes = range(graphSize)	
			createAdjacency(graphNodes, indexi)
			permute(subAdjList, 0, graphSize-1)
			permute(subAdjList, 1, graphSize-2)
			permute(ogAdjList, 0, graphSize-1)
			permute(ogAdjList, 1, graphSize-2)
			nodewa = krager()
#			print nodewa[0], nodewa[1]
			if (nodewa[1] == cutSet[indexi]):	
				comm.send(c1, dest=size-1, tag=11)
				break
			c1 = c1 + 1
			for i in ogAdjList:
				print i
else :
	while(len(complexityList) <= 99):
		print len(complexityList)
		complexityList.append(comm.recv(tag=11))
#	iterations = {}
	iterations = np.load(open("IterationCount2"))
	iterations[2] = complexityList
	pickle.dump(iterations, open("IterationCount2", 'w'), pickle.HIGHEST_PROTOCOL)	
