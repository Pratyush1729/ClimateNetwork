from multiprocessing import Pool, Value
import numpy as np
from scipy.stats.stats import pearsonr 
import matplotlib.pyplot as plt
import time
from numba import jit 
thData = np.ndarray(shape=(110, 346, 2), dtype=float) #holds the lth index and rth index for a given location for a given seven day period 
#thData = np.load(open("corTh11AvgYearData"))
linArray = np.ndarray(shape=(357*356/2, 1), dtype=float)
probMat = np.ndarray(shape=(1000, 1), dtype=float)
rainData = np.load(open("rainfallData"))
timeOperation = []
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


def computePearsonVal():
	day = 82
	index = 0	
	for loc1 in range(357) :
			loc2 = loc1 + 1
			while (loc2 < 357): 
				linArray[index], p = pearsonr(rainData[loc1][0][day:day+12], rainData[loc2][0][day:day+12])
				index = index + 1
				loc2 = loc2 + 1

'''
def computePearsonVal(loc1, loc2, index):
		for loc1.value in range(357):
			loc2.value = loc1.value + 1
			while(loc2.value<357):
				print loc1.value, loc2.value, index.value 
				linArray[index.value], p = pearsonr(rainData[loc1.value][0][10:22], rainData[loc2.value][0][10:22])
				index.value = index.value + 1
				loc2.value = loc2.value + 1
'''

for year in np.arange(1):
#	for day in np.arange(82+222, 83+222):	
		print "Loop", year, day
		lth = rth = 500
		thSum = 0
		count =0
		#create the linearArray	or pearson values corresponding to the data set
		computePearsonVal()	

	   	#convert a 'nan' to 0 
		linArray = np.nan_to_num(linArray)		
		#calculate the frequency matrix or the histogram

		histData = np.histogram(linArray, bins=np.arange(-1, 1.002, 0.002))	
		#probablity matrix
		start_time = time.time()
		for indHist in range(1000):
			probMat[indHist] = histData[0][indHist]/(1.0*np.sum(histData[0]))
		end_time = time.time()
		timeOperation.append(end_time-start_time)
		#calculate the threshold
		start_time = time.time() 
		while(1):
			if (thSum < 0.95):
				sign = minima(probMat[lth], probMat[rth])
				if (lth >=0 and rth <1000):
					if (sign == 1) :
						thSum = thSum + probMat[lth]
						lth = lth - 1
					else :
						thSum = thSum + probMat[rth]
						rth = rth + 1
				elif(lth>=0 and rth > 1000):
					thSum = thSum + probMat[lth]							
					lth = lth - 1
				elif(lth<0 and rth<1000):
					thSum = thSum + probMat[rth]
					rth = rth + 1
			else :
					break 
		if (sign ==  1):
			lth = lth + 1
		else :
			rth = rth - 1
		print lth, rth	
		end_time = time.time()
		timeOperation.append(end_time - start_time)
		thData[year][day-10][0], thData[year][day-10][1] = (lth-500)*0.002, (rth - 500)*0.002	
		print thData[year][day-10][0], thData[year][day-10][1]
	

#	np.save(open("corTh11AvgYearData", "w"), thData)

