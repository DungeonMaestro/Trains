class Edge:
    __slots__ = ['start_vertex', 'end_vertex', 'magnitude']

    def __init__(self, **kwargs):
        self.start_vertex = kwargs['i']
        self.end_vertex = kwargs['f']
        self.magnitude = int(kwargs['d']) or 0

    def __len__(self):
        return self.magnitude

    @property
    def vertices(self):
        """Returns a tuple of the vertices of the edge"""
        return self.start_vertex, self.end_vertex

    def __str__(self):
        return f"{self.start_vertex} - {self.magnitude} - {self.end_vertex}"

    def __repr__(self):
        return str(self)

    def __gt__(self, other):
        return self.magnitude > other.magnitude

    def __lt__(self, other):
        return len(self) < len(other)
