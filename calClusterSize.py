import numpy as np

spTup = np.load(open("corSparseMatrix"))
tmp = []
covered = np.zeros(357, dtype=int)
clusterSize = []

'''#Each matrix element would be updated to 1 when the grah element is covered in a given cluster 
for i in range(5):
	for j in range(357):
		tmp.append(np.zeros(len(spTup[i][j])))		
	countCheck.append(tmp)
'''

count = 0		
def calClusterSize(rowNo, week, year):
	global spTup; global count; global covered
	if (len(spTup[year][week][rowNo])!=0):
		for edge in spTup[year][week][rowNo]:
			if (covered[edge] == 0):
				covered[edge] = 1
				count = count + 1
				calClusterSize(edge, week, year) 
			else :
				count = count + 1	
	return count
temp = set()


def calClusterForYear(year):
	for week in range(345):
		for loc1 in range(357): 
			if (covered[loc1] == 0):
				covered[loc1] = 1
				temp.append(calClusterSize(loc1, week, year))
				count = 0 		
		clusterSize.append(temp)
		temp = []	
		covered = np.zeros(357, dtype=int)			
