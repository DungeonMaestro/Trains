from edge import Edge


class Route():
	__slots__ = ['edges']

	def __init__(self, *edges):
		self.edges = [*edges]

	@property
	def start_vertex(self):
		"""The entry-point vertex of the route"""
		if self.edges:
			return self.edges[0].start_vertex
		return None

	@property
	def end_vertex(self):
		"""The endpoint vertex of the route"""
		if self.edges:
			return self.edges[-1].end_vertex
		return None

	@property
	def stops(self):
		"""How many stops are on the route"""
		return len(self.edges)

	@property
	def magnitude(self):
		"""returns the total magnitude of the route"""
		return sum(edge.magnitude for edge in self.edges)

	# Comparison overloads for sorting
	def __gt__(self, other):
		return self.magnitude > other.magnitude

	def __lt__(self, other):
		return self.magnitude < other.magnitude

	def __eq__(self, other):
		return self.edges == other.edges

	def __ne__(self, other):
		return not self == other

	def add(self, edge):
		"""adds a new edge to the end of a route if the edge is contiguous to the end of the route"""
		if self.edges and self.end_vertex != edge.start_vertex:
			raise ValueError(f"{edge} not contiguous to {self.edges[-1]}")
		self.edges.append(edge)

	def pop(self, index=None):
		"""removes the current endpoint of a route"""
		if self.edges:
			return self.edges.pop(index or -1)
		return None

	def is_contiguous(self):
		"""determines if a route is properly pathed"""
		for i in range(self.stops - 1):
			if self.edges[i].end_vertex != self.edges[i + 1].start_vertex:
				return False
		return True

	def __repr__(self):
		nl = '\n'
		tb = '\t'
		return f"\n---------{self.start_vertex}---------\n" \
		       f"{nl.join(f'{self.edges.index(edge) + 1}){tb}({edge}) -->' for edge in self.edges)}\n" \
		       f"---------{self.end_vertex}---------\n" \
		       f"Stops: {self.stops} | Dist: {self.magnitude}\n"
