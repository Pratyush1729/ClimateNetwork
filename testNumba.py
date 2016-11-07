from numba import jit
import time 

#@jit
def testNumba():
	for i in range(10000):
		for j in range(10000):
			k = i * j

start = time.time()
testNumba()
end = time.time()

diff = end - start
