from rich.console import Console
import rich.traceback
import functools

#po prostu zrobić dekorator

console = Console()
console.clear()
rich.traceback.install()

def called_decorator(_func = None, color='blue'):
	def sub_decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kwargs):
			console.print(f'[{color}]Called {func.__name__}[/{color}]')
			return func(*args,**kwargs)
		return wrapper
	if _func is not None:
		return sub_decorator(_func)
	return sub_decorator





#@called_decorator
@functools.cache
def fibon(n = 10):
	if n < 2:
		return n
	return fibon(n-1) + fibon(n-2)
#fibon = called_decorator(fibon)

#for n in range(50):
#	console.print(f'{n = }	{fibon(n) = }')


class MonteCarloSimulation:
	def __init__(self, hamiltonian = None):
		self._hamiltonian = hamiltonian

	def next_step(self):
		console.print(self._hamiltonian())

	def hamiltonian(self, func):
		self._hamiltonian = func
		return func
	
mcs = MonteCarloSimulation()

@mcs.hamiltonian
def my_super_hamiltonian():
	return 5

#mcs.next_step()



#class przyklad:
#	def __init__(self, b=0):
#		self.b = b
#
#	def get_b(self):
#		return self._b
#
#	def set_b(self, value):
#		self._b = value if value >= 0 else 0
#
#	b = property(get_b,set_b)


class przyklad:
	def __init__(self, b=0):
		self.b = b

	@property
	def b(self):
		return self._b
	@b.setter
	def b(self, value):
		self._b = value if value >= 0 else 0


p = przyklad()
p.b=15
console.print(p.b)

p.b=-15
#p._b=-15
console.print(p.b)

