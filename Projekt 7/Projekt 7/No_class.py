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
#	10 0.3 4.142e-21 15 30 q= file=

#np.random.seed(14)
#console = Console()
image_folder = 'images'

def main():
	start=time.time()
	
	#argumenty
	args = parse_args()
	n = args.n
	

	#sieć spinów
	grid = np.ones(n**2)
	tmp = int(args.q*n*n)
	grid[:tmp] = -1 * grid[:tmp]
	np.random.shuffle(grid)
	grid = np.reshape(grid,(n,n))

	#symulacja
	magnetyzacja=np.zeros(args.steps +1)
	for i in range(args.steps):
		rysunek(args.file + f'_{i}.png',grid,n)
		magnetyzacja[i]=(np.sum(grid)/(n**2))
		for j in range(n**2):
			x = np.random.randint(n)
			y = np.random.randint(n)
			grid[y,x] = Monte_Carlo(grid,n,args.Beta,args.J,args.H,x,y)

	rysunek(args.file + f'_{i}.png',grid,n)
	magnetyzacja[args.steps]=(np.sum(grid)/(n**2))


	#wykres magnetyzacji
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
def Monte_Carlo(grid,n,beta,J,H,x,y):
	'''
	Losuje element siatki (i,j), a następnie zamienia jego znak.
	Jeśli nowa energia układu jest mniejsza, kończy działanie.
	W przeciwnym przypadku przyjmuje wartość z prawdopodobieństwem exp(-B*delta_E)
	'''
	E_1 = hamiltonian(grid,n,J,H)
	grid[y,x] = -grid[y,x]
	E_2 = hamiltonian(grid,n,J,H)
	if E_2 > E_1:
		probs=np.exp(-beta*(E_2-E_1))
		if probs < np.random.random():
			grid[y,x] = -grid[y,x]

	return grid[y,x]


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

