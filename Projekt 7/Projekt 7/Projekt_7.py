#import rich.traceback
#from rich.console import Console
import time
import numpy as np
import argparse
import itertools
import time
from os.path import join
from rich.progress import track
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from numba import njit


#przykładowe argumenty:
#	10 0.3 4.142e-21 15 30
#	10 0.3 4.142e-21 15 30 q= file=

#np.random.seed(14)
#console = Console()
image_folder = 'images'

def main():
	start=time.time()
	
	args = parse_args()

	symulacja = simulation(args.n,args.J,args.Beta,args.H,args.q)
	magnetyzacja=symulacja(args.steps,args.file)
	plt.plot(list(range(len(magnetyzacja))),magnetyzacja, 'ro')
	plt.xlabel('krok')
	plt.ylabel('μ')
	plt.savefig(join('.',image_folder,'magnetyzacja.png'))

	stop = time.time()
	print(f'Czas wykonania symulacji: {stop-start}s')


def parse_args():
	"""
	Ustala wymagane i opcjonalne argumenty, a następnie
	zwraca strukturę, dla której są to atrybuty.
	"""
	parser = argparse.ArgumentParser(description='to jest opis')
	parser.add_argument('n', help='used to generate a n x n grid', type=int)
	parser.add_argument('J', help='całka wymiany', type=float)
	parser.add_argument('Beta', help='1/kT', type=float)
	parser.add_argument('H', help='external magnetic field', type=float)
	parser.add_argument('steps', help='number of steps in the simulation', type=int)
	parser.add_argument('-q', help='upward spin density in time = 0', type=float, default=0.5)
	parser.add_argument('-file', help='output file name', default='step')
	return parser.parse_args()

class simulation():
	def __init__(self, n, J, beta, H, q):
		self.n = n
		self.J = J
		self.beta = beta
		self.H = H

		arr = np.ones(n**2)
		tmp = int(q*n*n)
		arr[:tmp] = -1 * arr[:tmp]
		np.random.shuffle(arr)
		self.grid = np.reshape(arr,(n,n))

	def __call__(self, steps, file):
		mi=[]
		for i in range(steps):
			rysunek(file + '_' + str(i) + '.png',self.grid,self.n)
			mi.append(np.sum(self.grid)/(self.n**2))
			for _ in range(self.n**2):
				self.grid = Monte_Carlo(self.grid,self.n,self.beta,self.J,self.H)

		rysunek(file + '_' + str(steps) + '.png',self.grid,self.n)
		mi.append(np.sum(self.grid)/(self.n**2))
		return mi



#w
#@njit
def xy_points(n,size,i,j,spin=1):
	if spin == 0:
		xy1 = (int((j+0.5 )*size/n),int((i+0.75)*size/n))
		xy2 = (int((j+0.25)*size/n),int((i+0.25)*size/n))
		xy3 = (int((j+0.75)*size/n),int((i+0.25)*size/n))
	else:
		xy1 = (int((j+0.5 )*size/n),int((i+0.25)*size/n))
		xy2 = (int((j+0.25)*size/n),int((i+0.75)*size/n))
		xy3 = (int((j+0.75)*size/n),int((i+0.75)*size/n))
		
	return (xy1,xy2,xy3)


#s
@njit
def hamiltonian(grid,n,J,H):
	'''
	Wylicza energię układu jako E = -J * suma1 -H * suma2
	'''
	suma1 = 0
	suma2 = 0
	for i in range(n):
		for j in range(n):
			if i < n-1:
				suma1 += grid[i,j] * grid[i+1,j]
			if j < n-1:
				suma1 += grid[i,j] * grid[i,j+1]
			suma2 += grid[i,j]
	E = -J * suma1 - H * suma2
	return E

#w
#@njit
def Monte_Carlo(grid,n,beta,J,H):
	'''
	Losuje element siatki (i,j), a następnie zamienia jego znak.
	Jeśli nowa energia układu jest mniejsza, kończy działanie.
	W przeciwnym przypadku przyjmuje wartość z prawdopodobieństwem exp(-B*delta_E)
	'''
	i = np.random.randint(n)
	j = np.random.randint(n)
	E_1 = hamiltonian(grid,n,J,H)
	grid[i,j] = -grid[i,j]
	E_2 = hamiltonian(grid,n,J,H)
	if E_2 > E_1:
		probs=np.exp(-beta*(E_2-E_1))
		if probs < np.random.random():
			grid[i,j] = -grid[i,j]

	return grid


def rysunek(file,grid,n):
	size = 850
	image = Image.new('RGB',(size,size),(250,250,210))
	draw = ImageDraw.Draw(image)
	
	for i,j in itertools.product(range(n), repeat=2):
		if grid[i,j] > 0:
			draw.polygon(xy_points(n,size,i,j),(135,206,250))
		else:
			draw.polygon(xy_points(n,size,i,j,0),(240,128,128))
	image.save(join('.',image_folder,file))


if __name__ == "__main__":
	main()
