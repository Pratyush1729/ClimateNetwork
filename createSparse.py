#create sparse matrix given threshold values 
from scipy.stats.stats import pearsonr
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
newTup = []
rainData = np.load(open("rainfallData"))
arr = []
#sparse matrices for 5 months (not exactly sparse, but you get the point)
spSet = set() #the nodes that need to be attached : edge_nodes 
spTup = [] #stores the whole thing for each month
#spTup = np.load(open("corSparseMatrix"))
#spTup = list(spTup)
spDict = {} #dictionary of (node, set(edge_nodes))
thData = np.load(open("corTh11AvgYearData"))
#correlation matrix for holding all (357, 357)
rank = comm.Get_rank()

year = 90+rank #0 to 109
val = np.ndarray(shape=(357, 1), dtype=float)
if (rank!=3):
	for day in np.arange(10, 355):
		print "Loop", day
		for loc1 in range(357):
			loc2 = loc1+1
			while (loc2 < 357):
				val[loc2], p = np.nan_to_num(pearsonr(rainData[loc1][year][day:(day+12)], rainData[loc2][year][day:(day+12)]))
				if (thData[90+rank][day-10][0]>val[loc2] or thData[90+rank][day-10][1]<val[loc2]):
					spSet.add(loc2)
				loc2 = loc2 + 1
			spDict[loc1] = spSet 
			spSet = set()
		spTup.append(spDict)
		spDict = {}
	comm.send(np.array(spTup), dest=3)
else :
	arr = comm.recv(source=0, tag=MPI.ANY_TAG)
	newTup.append(arr)				
	arr = comm.recv(source=1, tag=MPI.ANY_TAG)					
	newTup.append(arr)
	arr = comm.recv(source=2, tag=MPI.ANY_TAG)					
	newTup.append(arr)
	np.save(open("corSparseMatrix", "w"), newTup)
