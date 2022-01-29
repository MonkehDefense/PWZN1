from bokeh.plotting import figure, from_networkx
from bokeh.io import show
from bokeh.layouts import layout, column, row
import numpy as np
import random
import networkx as nx

#print(nodes)

# wizualizacja sieci (narysować)

def make_graph(dir):
	nodes = set()
	edges = []
	with open(dir, 'r') as f:
		for line in f:
			if line[:1] == '#':
				continue
	#		print(line)
			tmp = tuple([int(x) for x in line.split('	')])
			edges.append(tmp)
			nodes.update(tmp)

	graph = nx.Graph()
	graph.add_nodes_from(nodes)
	graph.add_edges_from(edges)

	return graph

def distribution(NXgraph):
	rozkl = dict()

	for node in NXgraph.nodes:
		deg = NXgraph.degree[node]
		if deg in rozkl:
			rozkl[deg] = rozkl[deg] + 1
		else:
			rozkl[deg] = 1

	return rozkl

def bokeh_hist(dist):
	dist = {str(k): v for k, v in sorted(dist.items(), key=lambda item: item[0])}
	#print(dist.keys())
	fig=figure(
		x_range=list(dist.keys()),
		x_axis_label='stopień',y_axis_label='ilość węzłów',
		height=420,
		width=500,
		title='rozkład stopni węzłów',
		sizing_mode='stretch_width',
		toolbar_location='right')
	fig.xgrid.grid_line_color = None
	fig.toolbar.logo = None
	fig.toolbar.autohide = True
	fig.vbar(x = list(dist.keys()),top = list(dist.values()), width = .7)
	fig.x_range.range_padding = .1

	return fig

def bokeh_graph(nxgraph):
	fig = figure(
		title="sieć głosowania na wikipedii",
		x_range=(-1.1,1.1), y_range=(-1.1,1.1))
	fig.xgrid.grid_line_color = None
	fig.toolbar.logo = None
	fig.toolbar.autohide = True
	fig.renderers.append(from_networkx(nxgraph,nx.spring_layout,scale=4,center=(0,0)))

	return fig

def main():
	#https://snap.stanford.edu/data/wiki-Vote.html
	graph = make_graph('Wiki-Vote.txt')
	dist_deg = distribution(graph)
	fig1 = bokeh_hist(dist_deg)
	fig2 = bokeh_graph(graph)
	show(layout(row(fig1,fig2)))

	n = 0
	print('Kolejne składowe spójne w sieci mają następujące ilości węzłów:')
	subs = list(nx.connected_components(graph))
	MAXsub = graph.subgraph(max(subs,key=len))
	for sub in subs:
		n+=1
		print(len(sub))
	print('\nW sumie jest',n,'składowych spójnych.\n\nZaczynam liczyć średnią najmniejszą drogę między węzłami.')

	records = []
	for _ in range(1000):
		w1,w2 = random.choices(list(MAXsub.nodes()),k=2)
		records.append(nx.shortest_path_length(MAXsub,source=w1,target=w2))
	print('Dla największej spójnej składowej średnia najkrótsza trasa wynosi w przybliżeniu:',np.mean(records))



if __name__ == '__main__':
	main()