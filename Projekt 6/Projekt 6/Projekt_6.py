import functools
import numpy as np
import time
#from datetime import datetime

def time_it(_func=None,n=1):
	def sub(func, *args, **kwargs):
		@functools.wraps(func)
		def wrapper(*args,**kwargs):
			result = None
			start=time.time()
			for i in range(n):
				result = func(*args,**kwargs)
			stop = time.time()
			print(f'średni czas wykonania funkcji {func.__name__}: {(stop-start)/n}s')
			return result
		return wrapper

	if _func is None:
		return sub
	return sub(_func)



@time_it
def time_waster(array, k):
	for i in range(k):
		np.zeros((3,len(array))) if np.random.random() < .5 else array[:]*.1*(5 - np.linalg.norm(array[:]))/np.linalg.norm(array[:])
#		print('ok')
		for j in range(len(array)):
			np.linalg.norm(array[j]/.2)
	return array

tablica=np.array([np.sin(x) for x in np.linspace(0,np.pi,300)])

#a=time.time()
#time.sleep(2)
#b=time.time()
#print(f'{b-a}s\n')

time_waster(tablica, 20)
