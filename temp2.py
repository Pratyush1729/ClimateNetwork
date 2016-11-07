import numpy as np
from scipy.stats.stats import pearsonr


thData = np.ndarray(shape=(224, 2), dtype=float) #holds the lth index and rth index
linArray = np.ndarray(shape=(357*356/2, 1), dtype=float)
probMat = np.ndarray(shape=(1000, 1), dtype=float)
avgData = np.load(open("rainAvg10Data"))


binary = 0
def minima(pl, pr):
#zero if left is smaller; one otherwise
	global binary 
        if (binary == 0):
		binary = 1
                return 0
        else :
		binary = 0
                return 1

for i in range(357):

	print "Loop", i	
	lth = rth = 500
	thSum = 0 
	count = 0
	#create the linearArray you would like to find the threshold for 
	for j in range(110):
		for k in range(21):
			if (k!=j):
				linArray[count], p = pearsonr(avgData[i][j][k*11:((k+1)*11-1)], avgData[i][j][k*11:((k+1)*11-1)]1)
				count = count + 1

	#create the frequency matrix or the histogram
		histData = np.histogram(linArray, bins=np.arange(-1, 1.002, 0.002))	

	#probablity matrix
	for k in range(1000):
		probMat[k] = histData[0][k]/(1.0*np.sum(histData[0]))
	
	#calculate the threshold 		
	while(1):
		if (thSum < 0.95):
			if (lth >= 0 and rth < 1000):
				sign = minima(probMat[lth], probMat[rth])
				if (sign == 1):
					thSum = thSum + probMat[lth]
					lth = lth - 1
				else :
					thSum = thSum + probMat[rth]
					rth = rth + 1
			elif(lth>=0 and rth > 1000):
				thSum	= thSum + probMat[lth]
				lth = lth - 1
			elif(lth<0 and rth <= 1000):
				thSum = thSum + probMat[rth]
				rth = rth + 1
			else :
				break 
		
		else :
			print thSum
		        break
	if(sign == 1):
		lth = lth + 1
	else :
       		rth = rth - 1
	thData[i][0], thData[i][1] = (lth-500)*0.002, (rth-500)*0.002 		

np.save(open("corTh10AvgData", "w"), thData)	 			
