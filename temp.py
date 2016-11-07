# [82, 304]
index = 82
monsoonData = np.ndarray(shape=(357, 110, 223), dtype=float)

for i in range(357):
	print "Loop", i
	for j in range(110):
		for k in range(223):
			moonsoonData[i][j][k] = np.mean([monsoonData[i][j][l] for l in np.arange(index, index+11)])
			index = index + 1
		index = 0
			
