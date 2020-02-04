from copy import copy
from string import digits
from random import choice, shuffle
from unittest import TestCase

from edge import Edge
from graph import Graph
from route import Route


class TestEdge(TestCase):
    def setUp(self):
        self.edge = Edge(i='A', f='B', d=1)

    def test_bad_contructor_args(self):
        with self.assertRaises(KeyError):
            Edge(i='A', f='B', nonsense=1)

    def test_good_constructor_args(self):
        self.setUp()
        self.assertEqual(self.edge.start_vertex, 'A')
        self.assertEqual(self.edge.end_vertex, 'B')
        self.assertEqual(self.edge.magnitude, 1)

    def test_comparisons(self):
        edge0 = Edge(i='A', f='B', d=2)
        edge1 = Edge(i='C', f='D', d=1)

        self.assertGreater(edge0, edge1)
        self.assertGreater(edge0, self.edge)


class TestRoute(TestCase):
    def setUp(self):
        self.route = Route(
            Edge(i='A', f='B', d=1),
            Edge(i='B', f='C', d=1),
            Edge(i='C', f='D', d=2),
            Edge(i='D', f='A', d=3)
        )

    def test_good_constructor_args(self):
        self.setUp()
        self.assertEqual(len(self.route), 7)
        self.assertEqual(self.route.stops, 4)
        self.assertEqual(self.route.start_vertex, 'A')
        self.assertEqual(self.route.end_vertex, 'A')

    def test_good_constructor_args(self):
        route = Route("AB1", Edge(i='B', f='C', d=1), Edge(i='C', f='D', d=2), Edge(i='D', f='A', d=3))
        with self.assertRaises(AttributeError):
            _ = route.magnitude
            _ = route.stops
        self.assertEqual(route.end_vertex, 'A')

    def test_comparisons(self):
        shuffled = Route(
            Edge(i='A', f='B', d=1),
            Edge(i='D', f='A', d=3),
            Edge(i='B', f='C', d=1),
            Edge(i='C', f='D', d=2),
        )
        longer_both = Route(
            Edge(i='A', f='B', d=1),
            Edge(i='B', f='C', d=1),
            Edge(i='C', f='D', d=2),
            Edge(i='D', f='E', d=3),
            Edge(i='E', f='F', d=5),
            Edge(i='F', f='A', d=8)
        )
        longer_mag_fewer_stops = Route(
            Edge(i='A', f='B', d=1),
            Edge(i='B', f='C', d=2),
            Edge(i='C', f='A', d=8)
        )
        peer = Route(
            Edge(i='A', f='B', d=1),
            Edge(i='B', f='C', d=1),
            Edge(i='C', f='D', d=1),
            Edge(i='D', f='A', d=4)
        )
        more_stops_same_mag = Route(
            Edge(i='A', f='B', d=1),
            Edge(i='B', f='C', d=1),
            Edge(i='C', f='D', d=1),
            Edge(i='D', f='E', d=1),
            Edge(i='E', f='A', d=2)
        )
        self.assertGreater(longer_both, self.route)
        self.assertGreater(longer_mag_fewer_stops, self.route)
        self.assertNotEqual(peer, self.route)
        self.assertNotEqual(more_stops_same_mag, self.route)
        self.assertNotEqual(shuffled, self.route)

    def test_methods(self):
        shuffled = Route(
            Edge(i='A', f='B', d=1),
            Edge(i='D', f='A', d=3),
            Edge(i='B', f='C', d=1),
            Edge(i='C', f='D', d=2),
        )
        extension = Edge(i='A', f='A', d=10)
        truncated = Route(
            Edge(i='A', f='B', d=1),
            Edge(i='B', f='C', d=1),
            Edge(i='C', f='D', d=2),
        )
        self.assertFalse(shuffled.is_contiguous())
        self.assertTrue(self.route.is_contiguous())
        self.route.add(extension)
        self.assertEqual(self.route.stops, 5)
        self.assertEqual(extension, self.route.pop())
        self.assertEqual(self.route.stops, 4)


class TestGraph(TestCase):
    def setUp(self):
        self.graph = Graph('AB5,BC4,CD8,DC8,DE6,AD5,CE2,EB3,AE7')

    def test_pathfinding(self):
        routes0 = self.graph.find_paths('C', 'C', 3, None, False)
        routes1 = self.graph.find_paths('A', 'C', 4, None, True)
        # TODO: Figure out why this specific method call is having issues
        routes2 = self.graph.find_path_of_least_magnitude('A', 'C', None)
        routes3 = self.graph.find_path_of_least_magnitude('B', 'B', None)
        routes4 = self.graph.find_paths('C', 'C', None, 29, False)
        self.assertEqual(len(routes0), 2)
        self.assertEqual(len(routes1), 3)
        self.assertEqual(routes2.magnitude, 9)
        self.assertEqual(routes3.magnitude, 9)
        self.assertEqual(len(routes4), 7)
