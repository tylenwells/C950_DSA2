# Tylen Wells twell56


class Package:

    def __init__(self, package_id, destination, deadline, weight, status, note):
        self.id = package_id
        self.destination = destination
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.truck = 0  # If value of truck is 0, package has not yet been assigned to a truck.
        self.note = note


class Destination:

    def __init__(self, address, city, state, zip_code):
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code


class RouteNode:

    def __init__(self, package):
        self.package = package
        self.next = None
        self.previous = None


class RouteList:

    def __init__(self):
        self.truck = 0  # If value of truck is 0, this route has not had a truck assigned yet.
        self.head = None
        self.tail = None


class PackageHashTable:  # This hash table is meant to store the Package items, using the package_id as the key.

    def __init__(self, initial_capacity=64):
        self.table = []
        for i in range(initial_capacity):  # Fill list with (initial_capacity) empty lists as bucket placeholders.
            self.table.append([])

    def _generate_key(self, key):
        self.key_buffer = key * 9001
        return self.key_buffer % 64

    def insert(self, package_id, address, deadline, city, state, zip_code, weight, status, note=""):
        destination = Destination(address, city, state, zip_code)
        package = Package(package_id, destination, deadline, weight, status, note)
        key = self._generate_key(package.id)

        if self.table[key].__len__() is 0:  # If bucket has no items, append new item to empty list.
            self.table[key].append((package.id, package))
        else:
            check = False  # Check for item in bucket with matching key, if one exists replace it.
            for c in self.table[key]:
                if c[0] is package_id:
                    self.table[key].remove(c)
                    self.table[key].append((package.id, package))
                    check = True
            if check is False:
                self.table[key].append((package.id, package))  # If no matching key is found, append new item to list.


class Vertex:

    def __init__(self, destination):
        self.destination = destination


class Graph:

    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex: Vertex, to_vertex: Vertex, weight: float = 1.0):
        if not self.adjacency_list.__contains__(from_vertex):
            self.add_vertex(from_vertex)
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, from_vertex: Vertex, to_vertex: Vertex, weight: float = 1.0):
        self.add_directed_edge(from_vertex, to_vertex, weight)
        self.add_directed_edge(to_vertex, from_vertex, weight)

# TODO Test out graph
