from math import factorial

from edge import Edge
from route import Route


class Graph:
	"""A graph stores a collection of edges and stores some methods to operate upon them"""
	__slots__ = ['edges', 'vertices']

	def __init__(self, map_str):
		def parse_edges():
			"""breaks a string into a dictionary of attributes for creating Edge objects"""
			return [{'i': edge[0], 'f': edge[1], 'd': edge[2:]} for edge in map_str.split(',')]

		edge_dict = parse_edges()
		self.edges = {Edge(**e_dict) for e_dict in edge_dict}
		self.vertices = {['starts', 'ends'][i]: list(zip(*map(lambda e: e.vertices, self.edges)))[i] for i in range(2)}

	def find_edges(self, **kwargs):
		"""finds the subset of the links whose attributes satisfy the passed kwargs"""
		return [edge for edge in self.edges if all(getattr(edge, key) == value for key, value in kwargs.items())]

	@property
	def M(self):
		"""
		M is a common notation for an arbitrary large number to be used as an upper bound for optimization problems
		I defined it as the product of the magnitude of the longest edge and the number of non-replacing permutations of
		the edges of the graph. A graph's big-M must at most be equal to this value if the lowest upper bound is finite*

		*proof left as an exercise to the reader
		"""
		def longest_edge():
			"""returns the magnitude of the longest edge"""
			return max(self.edges).magnitude

		return longest_edge() * factorial(len(self.edges))

	def __repr__(self):
		nl = '\n'
		return f"{nl.join(str(edge) for edge in self.edges)}"

	def find_paths(self, from_v, to_v, max_stops=None, max_dist=None, exact=True):
		"""
		Finds every path from a starting point to an ending point, given restrictions. If no restrictions are
		given then an exception is thrown

		The path is found by using a depth-first traversal: iterating through a list of connected edges, and for each
		edge iterating through a sublist of connected edges, etc recursively, using the state subobject to persist
		the progress of the algorithm
		"""

		class State:
			"""The live state of the algorithm's progress"""

			# we use state instead of self here because the super's self is needed for definitions
			def __init__(state):
				state.graph = self
				state.max_dist = max_dist or self.M
				state.max_stops = max_stops or self.M
				state.dist_escape = (lambda: state.curr_dist > state.max_dist)
				state.valid_dist = (
						lambda: state.curr_dist == state.max_dist) if max_dist and exact else lambda: not state.dist_escape()
				state.stops_escape = (lambda: state.curr_stops > state.max_stops)
				state.valid_stops = (
						lambda: state.curr_stops == state.max_stops) if max_stops and exact else lambda: not state.stops_escape()
				state.curr_path = []
				state.solutions = []

			@property
			def curr_vertex(self):
				"""the current end of the path"""
				if self.curr_path:
					return self.curr_path[-1].end_vertex
				return from_v

			@property
			def curr_stops(self):
				"""The running total of stops made"""
				return sum(1 if isinstance(vertex, Edge) else vertex.stops for vertex in self.curr_path)

			@property
			def curr_dist(self):
				"""The running total distance travelled"""
				return sum(edge.magnitude for edge in self.curr_path)

			def traverse_through(self, edge):
				"""steps the path into the given edge"""
				self.curr_path.append(edge)

			def traverse_back(self):
				"""steps the path back to the previous edge"""
				if self.curr_path:
					self.curr_path.pop()

			def contiguous_edges(self):
				"""gets the valid links that branch from the current node"""
				return {edge for edge in self.graph.edges if edge.start_vertex == self.curr_vertex}

		def traverse_graph(state):
			"""The recursive method that traverses the tree, recording and solutions"""

			# if either escape clause is true...
			if state.dist_escape() or state.stops_escape():
				return state

			# if the endpoint is reached and everything is valid, a solution is found
			if \
					state.curr_path and \
							state.curr_path[-1].end_vertex == to_v and \
							state.valid_stops() and \
							state.valid_dist():
				state.solutions.append(Route(*state.curr_path))

			# get a set of potential edges to follow and iterate over that set
			potential_edges = state.contiguous_edges()
			for edge in potential_edges:
				state.traverse_through(edge)
				traverse_graph(state)
				state.traverse_back()
			return state

		if to_v not in self.vertices['ends']:
			raise ValueError(f" This method will never find a solution because {to_v} is not an endpoint of any edge")
		if not max_dist and not max_stops:
			raise ValueError("This method requires at least either max_dist= or max_stops= to be defined.")

		# Instantiate the state so here I can watch it more easily
		state = State()
		traverse_graph(state)
		solutions = state.solutions

		return solutions

	def find_path_of_least_magnitude(self, from_v, to_v, max_dist=None):
		"""
		Recursively searches the tree by growing resolution until a solution is found, then return it.

		This method works by assuming the shortest possible distance is 0, then assuming the shortest possible distance
		is 1, etc, until it finds a valid path from A to B that is no larger than the assumption.

		The path is found by using a depth-first traversal: iterating through a list of connected edges, and for each
		edge iterating through a sublist of connected edges, etc recursively, using the state subobject to persist
		the progress of the algorithm"""

		class State:
			"""The live state of the algorithm's progress"""

			# we use state instead of self here because the super's self is needed for definitions
			def __init__(state):
				state.graph = self
				state.depth = lambda: sum(edge.magnitude for edge in state.curr_path)
				state.escape = max_dist or self.M
				state.max_dist = max_dist or self.M
				state.curr_path = []
				state.solution = None
				state.resolution = 0

			@property
			def curr_vertex(self):
				"""the current end of the path"""
				if self.curr_path:
					return self.curr_path[-1].end_vertex
				return from_v

			def traverse_through(self, edge):
				"""steps the path into the given edge"""
				self.curr_path.append(edge)

			def traverse_back(self):
				"""steps the path back to the previous edge"""
				if self.curr_path:
					self.curr_path.pop()

			def contiguous_edges(self):
				"""gets the valid links that branch from the current node"""
				return {edge for edge in self.graph.edges if edge.start_vertex == self.curr_vertex}

			@property
			def is_path(self):
				"""returns whether or not a correct path is found"""
				return self.curr_path and self.curr_path[-1].end_vertex == to_v

		def traverse_graph(state):
			"""The recursive method that traverses the tree, returning when a solution is found"""

			# increments the method resolution
			for state.resolution in range(state.resolution, state.escape):

				# if a solution is recorded
				if state.is_path:
					state.solution = Route(*state.curr_path)
					break
				else:

					# get a set of potential edges to follow and iterate over that set
					potential_edges = state.contiguous_edges()
					for edge in potential_edges:
						# if stepping forward from here would exceed the resolution, or if the resolution has already
						# been exceeded, move to the next potential edge instead of going deeper
						if state.depth() >= state.resolution:
							continue

						elif state.depth() + edge.magnitude < state.resolution:
							state.traverse_through(edge)
							traverse_graph(state)
							# if a solution is found, bubble the recursion up instead of proceeding
							if state.solution:
								return state
							state.traverse_back()
			return state

		if to_v not in self.vertices['ends']:
			raise ValueError(f" This method will never find a solution because {to_v} is not an endpoint of any edge")

		state = State()
		try:
			traverse_graph(state)
		except RecursionError:
			print("No solution was found")
			return None
		return state.solution
