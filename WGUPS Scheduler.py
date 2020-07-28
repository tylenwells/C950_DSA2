# Tylen Wells twell56

import csv


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

    def __init__(self, address: str, city: str, state: str, zip_code: str) -> None:
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
        int_key = int(key)
        self.key_buffer = int_key * 9001
        return self.key_buffer % 64

    def insert(self, package_id, address, deadline, city, state, zip_code, weight, status, note=""):
        destination = Destination(address, city, state, zip_code)
        package = Package(package_id, destination, deadline, weight, status, note)
        key = self._generate_key(package.id)
        self._add_to_list(key, package)

    def insert(self, package: Package):
        package = package
        key = self._generate_key(package.id)
        self._add_to_list(key, package)

    def _add_to_list(self, key, package: Package):

        if self.table[key].__len__() is 0:  # If bucket has no items, append new item to empty list.
            self.table[key].append((package.id, package))
        else:
            check = False  # Check for item in bucket with matching key, if one exists replace it.
            for c in self.table[key]:
                if c[0] is package.id:
                    self.table[key].remove(c)
                    self.table[key].append((package.id, package))
                    check = True
            if check is False:
                self.table[key].append((package.id, package))  # If no matching key is found, append new item to list.

    def lookup(self, package_id):  # This returns the package class item containing the entity-specific data elements.
        key = self._generate_key(package_id)
        if self.table[key].__len__() is 0:
            return None  # Return None if no package in the bucket.
        else:
            for c in self.table[key]:
                if c[0] is package_id:
                    return c[1]
        return None  # Return None if none of the existing packages in the bucket match the key provided.


# Vertex and Graph classes are used to represent addresses and the distances between. Each vertex will contain a
# Destination class that stores the address specific information. Each edge will contain the distance,
# which will be the weight for each edge.


class Vertex:

    def __init__(self, destination):
        self.destination = destination


class Graph:

    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex: Vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex: Vertex, to_vertex: Vertex, weight: float = 1.0):
        if not self.adjacency_list.__contains__(from_vertex):
            self.add_vertex(from_vertex)
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, from_vertex: Vertex, to_vertex: Vertex, weight: float = 1.0):
        self.add_directed_edge(from_vertex, to_vertex, weight)
        self.add_directed_edge(to_vertex, from_vertex, weight)


################################################
#   Begin main function
################################################


# Read the CSV File for distance and load data.

with open('WGUPS Distance Table.csv', newline='') as distance_csv_file:
    distance_reader = csv.reader(distance_csv_file, dialect='excel')
    distance_import_rows = []
    for row in distance_reader:
        distance_import_rows.append(row)

# Read the CSV file for packages and load data.

with open('WGUPS Package File.csv', newline='') as package_csv_file:
    package_reader = csv.reader(package_csv_file, dialect='excel')
    package_import_rows = []
    for row in package_reader:
        package_import_rows.append(row)

# Load distance data and destinations into graph data structure.

destination_list = []
vertex_list = []
for i in range(distance_import_rows.__len__() - 1):  # Populate "destination_list" with info.

    leading_char = distance_import_rows[i + 1][1][0]  # Removing the leading whitespace from addresses.
    while leading_char.__contains__(" "):
        distance_import_rows[i + 1][1] = distance_import_rows[i + 1][1][1:]
        leading_char = distance_import_rows[i + 1][1][0]

    return_index = distance_import_rows[i + 1][1].index('\n')  # Finding the '\n' offset for Zip-Code retrieval.

    # Creates Destination objects and appends them to the "destination_list" list for future use.
    d1 = Destination(distance_import_rows[i + 1][1][:return_index], "Salt Lake City", "UT",
                     distance_import_rows[i + 1][1][return_index + 2:return_index + 7])
    destination_list.append(d1)

for d in destination_list:  # Populate "vertex_list" with a unique vertex for each destination.
    v1 = Vertex(d)
    vertex_list.append(v1)

graph = Graph()  # "graph" will be our data structure to store distances. This is an undirected, weighted graph.

for v in vertex_list:  # Add vertexes to "graph"
    graph.add_vertex(v)

for i in range(distance_import_rows.__len__() - 1):  # This creates the undirected edges to hold the distance weights.
    values_to_process = i + 1
    for c in range(values_to_process):
        distance_value = float(distance_import_rows[values_to_process][c + 2])  # The distance will be the weight.
        graph.add_undirected_edge(vertex_list[i], vertex_list[c], distance_value)

# Load package data into hash table.

package_hash_table = PackageHashTable()

for i in range(package_import_rows.__len__() - 2):
    package_row = i + 2  # Skips the first two rows of "package_import_rows"
    package_number = package_import_rows[package_row][0]
    package_address = package_import_rows[package_row][1]
    package_city = package_import_rows[package_row][2]
    package_state = package_import_rows[package_row][3]
    package_zip_code = package_import_rows[package_row][4]
    package_deadline_time = package_import_rows[package_row][5]
    package_weight = package_import_rows[package_row][6]
    package_note = package_import_rows[package_row][7]
    package_destination = None

    for v in vertex_list:  # Find package destination in vertex list, use for creation of Package object.
        if v.destination.address == package_address:
            package_destination = v.destination
            v.destination.city = package_city   # Assign correct city data to vertex destination.
            break

    if package_deadline_time[0] is 'E':  # Convert deadline time to four-digit 24-hour time. (e.g. 4:00 PM to 1600)
        package_deadline_time = "1700"
    else:
        if package_deadline_time[1] is ':':  # Ensure a leading 0 to provide a 4-digit time. (e.g. 8:00 to 08:00)
            package_deadline_time = "0" + package_deadline_time
        if package_deadline_time[6] is "P":  # Convert 12-hour time to 24-hour time. (e.g. 08:00 to 20:00)
            to_convert = int(package_deadline_time[0:2]) + 12
            package_deadline_time = str(to_convert) + package_deadline_time[2:]

        package_deadline_time = package_deadline_time[0:2] + package_deadline_time[3:5]  # Convert to 4-digit time.

    p1 = Package(package_number, package_destination, package_deadline_time, package_weight, "Awaiting assignment",
                 package_note)

    package_hash_table.insert(p1)

