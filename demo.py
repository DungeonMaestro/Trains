import matplotlib
import scipy
import networkx as nx

from tests import TestGraph

t = TestGraph()
t.setUp()
r = t.rand_graph
g = t.graph

edges = {
    'r': [(edge.start_vertex, edge.end_vertex, edge.magnitude) for edge in r.edges],
    'g': [(edge.start_vertex, edge.end_vertex, edge.magnitude) for edge in g.edges]
}

R = nx.Graph()
G = nx.Graph()

R.add_weighted_edges_from(edges['r'])
G.add_weighted_edges_from(edges['g'])

nx.draw_networkx(G)
# nx.draw_networkx(R)
