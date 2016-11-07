import numpy as np 


corMat = np.load(open("corSparseMatrix"))

def gmlfilecreator(i):	
	
	file1 = open("graphFile%d.gml"%i, "a") 
	#you have to start with this
	file1.write("graph\n[")
	#now based on the number of nodes you create the nodes in the graph

	for size in range(357):
		file1.write("\n  node  \n  [\n   id %d\n  ]"%size)
	for source in range(357):
		for target in corMat[i][source]:
			file1.write("\n  edge  \n  [\n   source %d\n   target %d\n  ]"%(source, target)) 	
	file1.write("\n]")
