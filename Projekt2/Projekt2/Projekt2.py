#import rich.traceback
from rich.progress import track
#from rich.console import Console
from PIL import Image, ImageDraw
import numpy as np
import argparse
import itertools
import os.path
import time
from matplotlib import pyplot as plt

#np.random.seed(14)
#console = Console()
image_folder = 'images'

def main():
    args = parse_args()
    symulacja = simulation(args.n,args.J,args.Beta,args.H,args.q)
    magnetyzacja=symulacja(args.steps,args.file)
    plt.plot(list(range(len(magnetyzacja))),magnetyzacja, 'ro')
    plt.xlabel('krok')
    plt.ylabel('μ')
    plt.savefig(os.path.join('.',image_folder,'magnetyzacja.png'))
    


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
        self.grid = np.ones((n,n))
        tmp = int(q*n)
        self.grid[:,tmp] = -1 * self.grid[:,tmp]
        for i in range(n):
            np.random.shuffle(self.grid[i])

    def __call__(self, steps, file):
        mi=[]
        for i in track(range(steps),description='Postęp symulacji...'):
            self.rysunek(file + '_' + str(i) + '.jpg')
            mi.append(self.magnetyzacja())
            time.sleep(0.1)
            for j in range(self.n**2):
                self.Monte_Carlo()

        self.rysunek(file + '_' + str(steps) + '.png')
        mi.append(self.magnetyzacja())
        return mi

    def hamiltonian(self):
        '''
        Wylicza energię układu jako E = -J * suma1 -H * suma2
        '''
        suma1, suma2 = 0, 0
        for i,j in itertools.product(range(self.n), repeat = 2):
            suma1 += self.grid[i,j] * self.grid[i+1,j] if i < self.n-1 else 0
            suma1 += self.grid[i,j] * self.grid[i,j+1] if j < self.n-1 else 0
            suma2 += self.grid[i,j]
        E = -self.J * suma1 -self.H * suma2
        return E

    def Monte_Carlo(self):
        '''
        Losuje element siatki (i,j), a następnie zamienia jego znak.
        Jeśli nowa energia układu jest mniejsza, kończy działanie.
        W przeciwnym przypadku przyjmuje wartość z prawdopodobieństwem exp(-B*delta_E)
        '''
        E_1 = self.hamiltonian()
        i,j = np.random.randint(self.n), np.random.randint(self.n)
        self.grid[i,j] = -self.grid[i,j]
        E_2 = self.hamiltonian()
        if E_2 > E_1:
            probs=np.exp(-self.beta*(E_2-E_1))
            if probs < np.random.uniform():
                self.grid[i,j] = -self.grid[i,j]

    def rysunek(self, file):
        #(250,250,210)      light goldenrod yellow
        #(135,206,250)      light sky blue
        #(240,128,128)      light coral
        #(189,183,107)      dark khaki
        size = 850
        image = Image.new('RGB',(size,size),(250,250,210))
        draw = ImageDraw.Draw(image)
        
        for i,j in itertools.product(range(self.n), repeat=2):
            if self.grid[i,j] > 0:
                xy1 = (int((j+0.5)*size/self.n),int((i+0.25)*size/self.n))
                xy2 = (int((j+0.25)*size/self.n),int((i+0.75)*size/self.n))
                xy3 = (int((j+0.75)*size/self.n),int((i+0.75)*size/self.n))
                draw.polygon((xy1,xy2,xy3),(135,206,250))
            else:
                xy1 = (int((j+0.5)*size/self.n),int((i+0.75)*size/self.n))
                xy2 = (int((j+0.25)*size/self.n),int((i+0.25)*size/self.n))
                xy3 = (int((j+0.75)*size/self.n),int((i+0.25)*size/self.n))
                draw.polygon((xy1,xy2,xy3),(240,128,128))
        image.save(os.path.join('.',image_folder,file))

    def magnetyzacja(self):
        mi=0
        for i,j in itertools.product(range(self.n), repeat = 2):
            mi += self.grid[i,j]
        return mi/(self.n**2)


if __name__ == "__main__":
    main()
