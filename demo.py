from random import choice
from string import digits

import matplotlib.pyplot as plt
import networkx as nx

from graph import Graph
from tests import TestGraph


def randgraph():
	alphabet = "ABCDEFG"

	def choose(seq, size):
		out = [choice(seq)]
		item = None
		for i in range(size - 1):
			while item in out or not item:
				item = choice(seq)
			out.append(item)
		return tuple(out)

	def rand_vert_names():
		return choose(alphabet, 2)

	def rand_edge_str():
		return ''.join([*rand_vert_names(), choice(digits)])

	def rand_graph_str(vertex_count):
		return ','.join(rand_edge_str() for _ in range(vertex_count))

	return Graph(rand_graph_str(10))


t = TestGraph()
t.setUp()
r = randgraph()
g = t.graph

edges = {
		'r': [(edge.start_vertex, edge.end_vertex, edge.magnitude) for edge in r.edges],
		'g': [(edge.start_vertex, edge.end_vertex, edge.magnitude) for edge in g.edges]
		}

R = nx.DiGraph()
G = nx.DiGraph()

R.add_weighted_edges_from(edges['r'])
G.add_weighted_edges_from(edges['g'])

nx.draw_networkx(G)
plt.savefig("graphs/G.png")
plt.show()
plt.cla()
nx.draw_networkx(R)
plt.savefig("graphs/R.png")
plt.show()
