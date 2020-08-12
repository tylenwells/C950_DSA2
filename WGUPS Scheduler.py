# Tylen Wells twell56

import csv
from os import system, name
import time
import sys


class Package:
    # This is the main object that will contain the package data, and that will be inserted into the hash table.
    # distance between two destinations can be gotten by finding the vertex associated with the destination and taking
    # advantage of graph.edge_weights.get((vertex 1, vertex 2)) function which will return a float distance value.

    # Complexity: O(C)
    def __init__(self, package_id, destination, deadline, weight, status, note):
        self.id = package_id
        self.destination = destination
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.route = 0  # If value of route is 0, package has not yet been assigned to a route.
        self.note = note
        self.assigned = False
        self.bypass_flag = False


class Destination:
    # Contains an address that is assigned to both packages and our distance graph vertexes.
    # This class is used to cross reference package addresses for distance retrieval.

    # Complexity: O(C)
    def __init__(self, address: str, city: str, state: str, zip_code: str) -> None:
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

#
class RouteNode:
    # Nodes of the RouteList linked list class. contains package and vertex elements for data, as well as pointing to
    # the .next node in the linked list.

    # Complexity: O(N)
    def __init__(self, package):
        self.package = package
        self.vertex = None
        for i in vertex_list:
            if i.destination.address == self.package.destination.address:
                self.vertex = i
                break
        self.next = None


class RouteList:

    # Complexity: O(C)
    def __init__(self, truck: int, max_nodes=16):
        self.truck = truck  # If value of truck is 0, this route has not had a truck assigned yet.
        self.head = None
        self.tail = None
        self.size = 0
        self.max_nodes = max_nodes  # This is the maximum number of packages allowed per route. Default is 16.
        self.active = False
        self.start_time = "0800"

    # Complexity: O(C)
    def set_start_time(self, start_time: int):  # Ensures start time is set as an 4 digit number between 0800 and 1200.
        if start_time > 1700 or start_time < 800:  # If start time is before 8:00AM or after EOD, disregard.
            return None
        else:
            buffered_time = str(start_time)  # Convert int input to str. E.g. 800 for 8AM converted to "800".
            if buffered_time.__len__() == 3:  # e.g. "800", this is not 24 hour, 4 digit time. It's missing the lead 0.
                buffered_time = "0" + buffered_time  # e.g. "800" becomes "0800"
            self.start_time = buffered_time  # Set start time to the formatted string time.

    # Complexity: O(logN), This is because add_node() calls self.sort_route() which has a complexity of O(logN).
    def add_node(self, new_node: RouteNode = None, new_node_list=None, *args):  # Adds node(s) to the linked list.
        if new_node is not None and new_node_list is None:  # If a node (singular) is passed but not a list of nodes.
            if self.size == 0:  # If list doesn't currently contain any nodes, new node is also the head and tail.
                self.head = new_node
                self.tail = new_node
                self.size = 1
                self.active = True
            else:  # If the list has nodes already, append the new node to tail.next and make it the new tail. Sort.
                self.tail.next = new_node
                self.tail = self.tail.next
                self.size = self.size + 1
                self.sort_route(graph)
        if new_node_list is not None and new_node is None:  # If list is passed in instead of a singular node.
            if self.size == 0:  # If the linked list doesn't contain any nodes.
                self.head = new_node_list[0]  # Set the first new node as the head.
                self.tail = new_node_list[0]  # Set the first new node as the tail.
                self.size = 1
                self.active = True
                new_node_list.remove(new_node_list[0])  # Remove the first new node to prevent a duplicate node.
            for node in new_node_list:  # Add each remaining new node to the linked list per normal.
                self.tail.next = node
                self.tail = self.tail.next
                self.size = self.size + 1
            self.sort_route(graph)  # Sort.

    # Complexity: O(logN)
    def sort_route(self, graph):  # The primary sorting algorithm for ordering deliveries is done here.
        list_to_sort = []  # List to aggregate nodes that have been added to this route.

        list_near_to = []  # List to store nodes with deadlines on the same side of the hub as the furthest node.
        list_near_from = []  # List to store nodes without deadlines on the same side of the hub as the furthest node.
        list_far_to = []  # List to store nodes with deadlines on the far side of the hub from the furthest node.
        list_far_from = []  # List to store nodes without deadlines on the far side of the hub from the furthest node.

        # Add all nodes in route to list_to_sort.
        for r in range(self.size):
            buffer = r
            node_to_add = self.head
            while buffer > 0:
                node_to_add = node_to_add.next
                buffer = buffer - 1
            list_to_sort.append(node_to_add)

        # Find the node furthest from the hub. We use this to structure our algorithm.
        furthest_node = (0.0, None)  # Buffer to hold highest distance node from Hub.
        for node in list_to_sort:  # Get Distance from Hub to Node, store it if it's higher than furthest_node.
            distance = graph.edge_weights.get((vertex_list[0], node.vertex))
            if distance > furthest_node[0]:
                furthest_node = (distance, node)
        list_to_sort.remove(furthest_node[1])  # Remove furthest node from the list_to_sort.
        list_near_from.append(furthest_node[1])  # Add furthest node to the list_near_from.
        list_near_from[0].next = None  # Clear the next pointer from the node, we don't know what will be after it yet.

        # Here we sort the rest of the nodes into the proper list based upon two pieces of data.
        #
        # 1. Is the node on the same side of the hub as the furthest node?
        #   a) This is found by comparing the distance between the furthest node and the hub with the distance between
        #      the furthest node and the node in question. If the distance between the furthest node and the node in
        #      question is greater, it's assumed to be on the "far side" of the hub from the furthest node.
        #   b) Separating the nodes into the "far side" and the "near side" allows us to target nodes more efficiently.
        #
        # 2. Does the node have a deadline before 1200?
        #   a) If so, this node needs to be prioritized, we should deliver it before the nodes the do not.
        #   b) We do this by further breaking apart the "near" and "far" groups into "to" and "from".
        #   c) The "to" group for each of the sides will have the prioritized nodes that have deadlines.
        #
        # These groups give us the lists we initiated above, containing near_to, near_from, far_to, and far_from.

        for n in list_to_sort:
            n.next = None  # Since we don't know what the node after each node is yet, clear the node.next pointer.
            distance = graph.edge_weights.get((furthest_node[1].vertex, n.vertex))  # Distance from node to furthest.
            if distance > furthest_node[0]:  # If node is on "far side"
                if int(n.package.deadline) < 1200:  # If node has deadline before 1200.
                    list_far_to.append(n)
                else:
                    list_far_from.append(n)
            else:  # Else node is on "near side"
                if int(n.package.deadline) < 1200:  # If node has deadline before 1200.
                    list_near_to.append(n)
                else:
                    list_near_from.append(n)

        self.head = None  # Set head pointer to none.
        self.tail = None  # Set tail pointer to none.

        #
        # This sorting algorithm prioritizes each different list in the following order:
        # 1. list_far_to - contains far side nodes with deadlines before 1200
        # 2. list_far_from - contains the rest of the far side nodes. This is delivered before list_near_to because of
        #                    the physical proximity to the nodes of list_far_to.
        # 3. list_near_to - contains the near side nodes with deadlines before 1200
        # 4. list_near_from - contains the rest of the near side nodes, including the furthest node from the hub.
        #
        # Logic for each of the lists is identical and uses a simple greedy algorithm from this point on.
        #

        # 1. list_far_to
        while list_far_to.__len__() > 0:

            # Find the closest node to the start location (either self.tail or hub).
            closest_node = (9999.9, None)  # Set closest_node to unrealistically high distance (10000KM distance).
            for node in list_far_to:
                if self.tail is not None:  # If a node has already been assigned to the linked list.
                    distance = graph.edge_weights.get((self.tail.vertex, node.vertex))  # Get distance from tail.
                else:
                    distance = graph.edge_weights.get((vertex_list[0], node.vertex))  # Get distance from hub.
                if distance < closest_node[0]:  # If the distance is closer than the distance of closest_node.
                    closest_node = (distance, node)  # Assign current node as the new closest node.
            if self.head is None:  # If list has no head (presumably it's empty or hasn't had one assigned yet).
                self.head = closest_node[1]  # Assign closest node to head. If a head exists, just set it as tail only.
            if self.tail is not None:  # If a tail already exists as well, set the new node the the current tail.next.
                self.tail.next = closest_node[1]
            self.tail = closest_node[1]  # Set the tail to the closest node.
            list_far_to.remove(closest_node[1])  # Remove the node from the list as it's been processed.

        # 2. list_far_from - logic is the same.
        while list_far_from.__len__() > 0:
            closest_node = (9999.9, None)
            for node in list_far_from:
                if self.tail is not None:
                    distance = graph.edge_weights.get((self.tail.vertex, node.vertex))
                else:
                    distance = graph.edge_weights.get((vertex_list[0], node.vertex))
                if distance < closest_node[0]:
                    closest_node = (distance, node)
            if self.head is None:
                self.head = closest_node[1]
            if self.tail is not None:
                self.tail.next = closest_node[1]
            self.tail = closest_node[1]
            list_far_from.remove(closest_node[1])

        # 3. list_near_to - logic is the same.
        while list_near_to.__len__() > 0:
            closest_node = (9999.9, None)
            for node in list_near_to:
                if self.tail is not None:
                    distance = graph.edge_weights.get((self.tail.vertex, node.vertex))
                else:
                    distance = graph.edge_weights.get((vertex_list[0], node.vertex))
                if distance < closest_node[0]:
                    closest_node = (distance, node)
            if self.head is None:
                self.head = closest_node[1]
            if self.tail is not None:
                self.tail.next = closest_node[1]
            self.tail = closest_node[1]
            list_near_to.remove(closest_node[1])

        # 4. list_near_from - logic is the same.
        while list_near_from.__len__() > 0:
            closest_node = (9999.9, None)
            for node in list_near_from:
                if self.tail is not None:
                    distance = graph.edge_weights.get((self.tail.vertex, node.vertex))
                else:
                    distance = graph.edge_weights.get((vertex_list[0], node.vertex))
                if distance < closest_node[0]:
                    closest_node = (distance, node)
            if self.head is None:
                self.head = closest_node[1]
            if self.tail is not None:
                self.tail.next = closest_node[1]
            self.tail = closest_node[1]
            list_near_from.remove(closest_node[1])

        #
        # Update Start Times of Route 2 for each Truck.
        # This sets the second route start time to the trucks arrival back to the hub after delivering the last package.
        #
        if r1_0.size != 0:  # If Truck 1 Route 1 is not empty, set Truck 1 Route 2's start time to the return time of
            # Truck 1 Route 1

            # Get the time of delivery of the last package for route 1.
            r1_0_last_package_time = r1_0.get_package_delivery_time(graph, r1_0.tail)

            # Find the amount in minutes of time to add to the last_package_time in order to find the return time.
            r1_0_minutes_to_add = (graph.edge_weights.get((vertex_list[0], r1_0.tail.vertex)) * 60) / 18

            # Break minutes into hours and minutes.
            r1_0_hours_to_add = int(r1_0_minutes_to_add / 60)
            r1_0_minutes_to_add = round((r1_0_minutes_to_add % 60) + int(r1_0_last_package_time[2]
                                                                         + r1_0_last_package_time[3]))
            if r1_0_minutes_to_add > 59:
                r1_0_hours_to_add = r1_0_hours_to_add + 1
                r1_0_minutes_to_add = r1_0_minutes_to_add - 60

            # Convert the time hours and minutes into strings.
            r1_0_start_hours = str(int(r1_0_last_package_time[0:2]) + r1_0_hours_to_add)
            r1_0_start_minutes = str(r1_0_minutes_to_add)

            # Ensure that the length of each string is 2, providing leading zeroes if needed.
            if r1_0_start_hours.__len__() != 2:
                r1_0_start_hours = "0" + r1_0_start_hours
            if r1_0_start_minutes.__len__() != 2:
                r1_0_start_minutes = "0" + r1_0_start_minutes

            # Set the start time of the second route to the return time of the first route using 24-hour 4 digit time.
            r1_1.set_start_time(int(r1_0_start_hours + r1_0_start_minutes))  # e.g. "1345" for 1:45 PM

        # Logic is the same as above.
        if r2_0.size != 0:  # If Truck 2 Route 1 is not empty, set Truck 2 Route 2's start time to the return time of
            # Truck 2 Route 1
            r2_0_last_package_time = r2_0.get_package_delivery_time(graph, r2_0.tail)
            r2_0_minutes_to_add = (graph.edge_weights.get((vertex_list[0], r2_0.tail.vertex)) * 60) / 18

            r2_0_hours_to_add = int(r2_0_minutes_to_add / 60)
            r2_0_minutes_to_add = round((r2_0_minutes_to_add % 60) + int(r2_0_last_package_time[2]
                                                                         + r2_0_last_package_time[3]))
            if r2_0_minutes_to_add > 59:
                r2_0_hours_to_add = r2_0_hours_to_add + 1
                r2_0_minutes_to_add = r2_0_minutes_to_add - 60
            r2_0_start_hours = str(int(r2_0_last_package_time[0:2]) + r2_0_hours_to_add)
            r2_0_start_minutes = str(r2_0_minutes_to_add)
            if r2_0_start_hours.__len__() != 2:
                r2_0_start_hours = "0" + r2_0_start_hours
            if r2_0_start_minutes.__len__() != 2:
                r2_0_start_minutes = "0" + r2_0_start_minutes
            r2_1.set_start_time(int(r2_0_start_hours + r2_0_start_minutes))

    # Complexity: O(N)
    def get_package_delivery_time(self, graph, node) -> str:  # This returns a string that represents the estimated time
        # of delivery for a node.

        # Set the current node to the head of the list, adding the distance from hub to head to total_distance.
        current = self.head
        next = current.next
        total_distance = graph.edge_weights.get((vertex_list[0], current.vertex))

        # Loop through each node in the route adding the distance to total_distance until finding the specified node.
        for i in range(self.size):

            # If the current node is the specified node, calculate and return delivery time.
            if current == node:
                start_time = self.start_time
                time_to_add = (total_distance * 60) / 18
                hours_to_add = int(time_to_add / 60)
                minutes_to_add = round((time_to_add % 60) + int(start_time[2] + start_time[3]))
                if minutes_to_add > 59:
                    hours_to_add = hours_to_add + 1
                    minutes_to_add = minutes_to_add - 60
                start_hours = str(int(start_time[0:2]) + hours_to_add)
                start_minutes = str(minutes_to_add)
                if start_hours.__len__() != 2:
                    start_hours = "0" + start_hours
                if start_minutes.__len__() != 2:
                    start_minutes = "0" + start_minutes
                return start_hours + start_minutes

            # If the current node is not the specified node, add distance to total_distance and keep going.
            if current.next is not None:
                total_distance = total_distance + graph.edge_weights.get((current.vertex, next.vertex))
                current = current.next
                next = current.next

    # TODO Finish writing up time complexity for the rest of the program. Start on the paperwork.
    def auto_assign_routes(self, graph, route_number: int):   # Automatically adds more nodes to the specified route.
        # This will add nodes until it runs out of unassigned nodes, or the truck is full.
        #
        # This assignment prioritizes those packages with deadlines before those without.

        graph = graph
        unassigned_packages = []
        for value in range(package_hash_table.table.__len__()):  # Get list of all packages that are unassigned.
            if package_hash_table.table[value].__len__() != 0:
                for a in package_hash_table.table[value]:
                    if a[1].route == 0:
                        unassigned_packages.append(a[1])

        # If there is room on the truck, proceed. Else, stop.
        remaining_capacity = self.max_nodes - self.size
        # Added a check for unassigned packages to keep function from running when there are no more packages to assign.
        if remaining_capacity == 0 or unassigned_packages.__len__() == 0:
            return
        else:
            nodes_to_add = []
            packages_with_deadlines = []

            # Find packages with deadlines and seperate them from unassigned_packages
            for package in unassigned_packages:
                if package.deadline != "1700":
                    packages_with_deadlines.append(package)
                    unassigned_packages.remove(package)

            # If there is more capacity available than there are packages with deadlines, just add them all.
            if packages_with_deadlines.__len__() <= remaining_capacity:
                for p in packages_with_deadlines:
                    p = RouteNode(p)
                    nodes_to_add.append(p)
                remaining_capacity = remaining_capacity - nodes_to_add.__len__()   # Update remaining_capacity.
            else:   # Otherwise, add packages individually until you run out of space.
                while remaining_capacity > 0 and packages_with_deadlines.__len__() > 0:
                    node_buffer = RouteNode(packages_with_deadlines.pop(0))
                    nodes_to_add.append(node_buffer)
                    remaining_capacity = (self.max_nodes - self.size) - nodes_to_add.__len__()   # Update capacity.

            # If you still have space after adding packages with deadlines, add the rest using a simple greedy algorithm
            # weighted based upon distance.
            if remaining_capacity > 0:
                tuple_list = []
                for package in unassigned_packages:
                    package = RouteNode(package)
                    distance = graph.edge_weights.get((package.vertex, vertex_list[0]))
                    tuple_list.append((distance, package))
                tuple_list.sort(key=lambda tup: tup[0])
                while remaining_capacity > 0 and tuple_list.__len__() > 0:
                    for t in tuple_list:
                        if tuple_list.__len__() == 0 or remaining_capacity == 0:
                            break
                        nodes_to_add.append(tuple_list.pop(0)[1])
                        remaining_capacity = remaining_capacity - 1

            # Ensure each node in nodes_to_add has had the route number appended and marked as assigned.
            for node in nodes_to_add:
                node.package.route = route_number
                node.package.assigned = True

            # Add list of nodes to the route, which will sort them properly.
            self.add_node(new_node_list=nodes_to_add)


# noinspection PyRedeclaration
class PackageHashTable:  # This hash table is meant to store the Package items, using the package_id as the key.

    def __init__(self, initial_capacity=64):  # Set the initial capacity of the hash table to 64.
        self.table = []
        for i in range(initial_capacity):  # Fill list with (initial_capacity) empty lists as bucket placeholders.
            self.table.append([])

    def _generate_key(self, key):  # This takes the int conversion of str package id * 9001 and takes % 64 as the key.
        int_key = int(key)
        self.key_buffer = int_key * 9001
        return self.key_buffer % 64

    # Requirement E is satisfied with this insert function.
    def insert(self, package_id, address, deadline, city, state, zip_code, weight, status, note=""):
        destination = Destination(address, city, state, zip_code)
        package = Package(package_id, destination, deadline, weight, status, note)
        key = self._generate_key(package.id)
        self._add_to_list(key, package)

    def insert(self, package: Package) -> None:  # This is a convenience function that takes a "Package" obj instead.
        package = package
        key = self._generate_key(package.id)
        self._add_to_list(key, package)

    def __count__(self, reference_string="") -> int:  # Function to return the count of packages of certain types.
        count = 0
        if reference_string is "":  # All packages.
            for value in range(self.table.__len__()):
                count = count + self.table[value].__len__()
        if reference_string is "note":  # Packages with notes.
            for value in range(self.table.__len__()):
                if self.table[value].__len__() != 0 and len(self.table[value][0][1].note) != 0:
                    count = count + 1
        if reference_string is "unresolved":  # Unassigned packages with notes.
            for value in range(self.table.__len__()):
                if self.table[value].__len__() != 0 and len(self.table[value][0][1].note) != 0 and \
                        self.table[value][0][1].route == 0:
                    count = count + 1
        if reference_string is "unassigned":  # All unassigned packages.
            for value in range(self.table.__len__()):
                if self.table[value].__len__() != 0 and self.table[value][0][1].route == 0:
                    count = count + 1
        return count

    def _add_to_list(self, key, package: Package):  # Internal function to add a package to the list via the key.

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
                if c[0] == package_id:
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

package_hash_table = PackageHashTable()  # This is the instantiated hash table used to store package data.

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
            v.destination.city = package_city  # Assign correct city data to vertex destination.
            v.destination.state = package_state  # Assign correct state data to vertex destination.
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
                 package_note)  # Assigns values found to a Package object

    package_hash_table.insert(p1)  # Insert package object into hash table.

# Declare two routes for each truck. rX_0 runs first, rX_1 runs second(if needed).

r1_0 = RouteList(1)
r1_1 = RouteList(1)
r2_0 = RouteList(2)
r2_1 = RouteList(2)


##
# GUI implementation starts here.
##

class GUI:
    def __init__(self):
        # GUI Class init method is blank and the class has no data members as it is a functional class
        # and not a data-storage class. This is only used to display a GUI for user interaction.
        pass

    @staticmethod
    def clear():  # Clear screen, works for both unix based and windows operating systems.
        if name == 'nt':
            _ = system('cls')
        if name == 'posix':
            _ = system('clear')

    def draw_main(self):  # Prints a main menu for users to interact with by choosing an option or inputting data.

        self.clear()
        time.sleep(0.1)
        print("########################################################################\n")
        print("Welcome to the WGUPS Scheduling Application!\n\n\nCurrent configuration is as follows:")
        print("Number of Trucks: 2")
        print("Number of Packages: " + str(package_hash_table.__count__()))
        print("Number of Packages with notes: " + str(package_hash_table.__count__("note")))
        print("Number of Packages with notes awaiting resolution: " + str(package_hash_table.__count__("unresolved")))
        print("Number of packages that are unassigned: " + str(package_hash_table.__count__("unassigned")))

        print("\nPlease choose an option:")
        print("1. Review packages with notes. (Noted packages must be assigned before auto-assignment can occur.)")
        print("2. Review all packages.")
        print("3. View status of specific package.")
        print("4. View estimated status of all packages at a specified time.")
        print("5. Manual Package Assignment")
        print("6. Automatically assign unassigned packages. (Requires pre-assignment of all packages with notes!)")
        print("7. View specific route information.")
        print("0. Exit this program.")

        user_choice = input("\n\nEnter a number and press \"Enter\" >")

        check = False
        if user_choice == "1":  # Sends the user to a screen where they can review packages that contain notes.
            check = True
            self.review_packages_with_notes()
        if user_choice == "2":  # Send users to a page to view all packages as well as their data and assigment status.
            check = True
            self.review_all_packages()
        if user_choice == "3":  # Allows users to specify an individual package by package_id to view.
            check = True
            self.review_specific_package()
        if user_choice == "4":  # Allows users to specify a time to view status of all packages at that point in time.
            check = True
            self.review_packages_temporal()
        if user_choice == "5":  # Allows users to choose a package by package ID and assign to a route manually.
            check = True
            self.manual_package_assignment()
        if user_choice == "6":  # Allows users to algorithmically assign the rest of packages to a route.
            # Requires all packages with notes to have been manually assigned.
            check = True
            self.automatic_package_assignment()
        if user_choice == "7":  # Allows users to view the status of a specific route including delivery times.
            # Also allows users to change the start-time of the first route of the day for each truck.
            check = True
            self.print_route_info()
        if user_choice == "0":  # Exits the program.
            sys.exit()
        if check is False:  # Re-draws the screen if the input given was invalid.
            print("Invalid input! Please try again.")
            print("\n")
            input("Press ENTER to continue...")
            self.draw_main()

    def review_packages_with_notes(self):
        self.clear()  # Clear screen.
        package_list = []
        for value in range(package_hash_table.table.__len__()):  # Find and append all packages with notes to list.
            if package_hash_table.table[value].__len__() != 0:
                for a in package_hash_table.table[value]:
                    if len(a[1].note) != 0:
                        package_list.append((int(a[1].id), a[1]))
        package_list.sort(key=lambda tup: tup[0])  # Sort by package ID.

        # Print header for list.
        print("\n All Packages with Notes:\n\nPackage ID\t\tDeliver To\t\t\t\t\t\t\t\t\tDeadline\tAssigned\tNote")

        # Print data for each package.
        for package in package_list:
            buffered_address = package[1].destination.address
            address_offset = 40 - len(package[1].destination.address)
            buffered_assignment = str(package[1].assigned)
            if package[1].assigned is True and package[1].route != 0:
                buffered_assignment = "Route " + str(package[1].route)[0] + "_" + str(package[1].route)[1]

            for p in range(address_offset):
                buffered_address = buffered_address + " "
            print(package[1].id + "\t\t\t\t" + buffered_address + "\t" + package[1].deadline + "\t\t" +
                  buffered_assignment + "\t\t" + package[1].note)

        # Present the user with the option of assigning one of the packages to a route manually.
        print("\nPlease choose an option:")
        print("1. View details about or assign a specific package to a route.")
        print("0. Return to main menu.")
        user_choice = input("\n\nEnter a number and press \"Enter\" >")
        check = False
        if user_choice == "1":
            check = True
            self.review_specific_package()
        if user_choice == "0":
            self.draw_main()
        if check is False:
            print("Invalid input! Please try again.")
            print("\n")
            input("Press ENTER to continue...")
            self.review_packages_with_notes()

    def review_all_packages(self):
        self.clear()  # Clear screen.
        package_list = []

        # Populate package_list with all packages.
        for value in range(package_hash_table.table.__len__()):
            if package_hash_table.table[value].__len__() != 0:
                for p in package_hash_table.table[value]:
                    package_list.append((int(p[1].id), p[1]))
        package_list.sort(key=lambda tup: tup[0])  # Sort list by package ID.

        # Print header for data display.
        print("\n All Packages:\n\nPackage ID\t\tDeliver To\t\t\t\t\t\t\t\t\tDeadline\tAssigned\tNote")

        # Print individual package information.
        for package in package_list:
            buffered_address = package[1].destination.address
            address_offset = 40 - len(package[1].destination.address)
            buffered_assignment = str(package[1].assigned)
            if package[1].assigned == True and package[1].route != 0:
                buffered_assignment = "Route " + str(package[1].route)
            for p in range(address_offset):
                buffered_address = buffered_address + " "
            print(package[1].id + "\t\t\t\t" + buffered_address + "\t" + package[1].deadline + "\t\t" +
                  buffered_assignment + "\t\t" + package[1].note)

        # Present user with an option to view more details about a package or assign a package to a route.
        print("\nPlease choose an option:")
        print("1. View details about or assign a specific package to a route.")
        print("0. Return to main menu.")
        user_choice = input("\n\nEnter a number and press \"Enter\" >")
        check = False
        if user_choice == "1":
            check = True
            self.review_specific_package()
        if user_choice == "0":
            self.draw_main()
        if check is False:
            print("Invalid input! Please try again.")
            print("\n")
            input("Press ENTER to continue...")
            self.review_all_packages()

    def review_specific_package(self):

        # Prompt user for id of package to review.
        print('\nWhich Package ID would you like to review?:')
        user_input = input("Please input a Package ID: >")
        check = False
        found_package = None
        if user_input.isnumeric():  # Ensure user input is a number.
            found_package = package_hash_table.lookup(user_input)
            if found_package is not None:
                check = True
        if not check:
            print("Package ID: " + user_input + " was not found. Please try again!")
            self.review_specific_package()
        self.clear()  # Clear screen.

        # Prints information for package specified.
        print("Specific Package information for Package ID: " + user_input)
        print("\nPackage ID: " + found_package.id + "\nDelivery Address: " + found_package.destination.address)
        print("City: " + found_package.destination.city + "\nState: " + found_package.destination.state)
        print("Zip-Code: " + found_package.destination.zip_code + "\nDelivery Deadline: " + found_package.deadline)
        route_buffer = None
        if found_package.route == 0:
            route_buffer = "None"
        else:
            route_buffer = str(found_package.route)
        print("Weight: " + found_package.weight + "\nStatus: " + found_package.status + "\nRoute: " + route_buffer)
        print("Note: " + found_package.note)

        # If package has not yet been assigned to a route, ask user if they want to assign to a route.
        if found_package.route == 0:
            check = False
            user_choice = None
            while not check:
                if user_choice is not None:
                    print("Invalid input! Please try again.")
                print("\nWould you like to assign this package to a route?\n Please enter 1 for \"yes\", and 0 for "
                      "\"No\"")
                user_choice = input()
                if user_choice == "1":
                    self.assign_package_to_route(found_package.id)
                    check = True
                if user_choice == "0":
                    self.draw_main()
        else:  # If package has a route already, let the user know and go back to the main menu.
            print("\n")
            input("This package has already been assigned to a route. Please press ENTER to return to the main menu.")
            self.draw_main()

    def review_packages_temporal(self):
        self.clear()  # Clear screen.

        # Prompt user for a time-input to display the status of all packages at.
        print("Review status of all packages at a specific time: \n")
        print("Please input the 4-digit 24-hour clock numeric time you would like to review package status at: ")
        print("For example: for 2:00PM, please enter 1400. Alternative enter 9999 to exit to main menu.\n")
        user_input = input()
        check = False
        if user_input == "9999":
            check = True
        while not check:
            if not user_input.isnumeric() or user_input.__len__() != 4 or int(user_input[2:4]) > 59 or int(
                    user_input[0:2]) > 23:

                user_input = input("Invalid Input! Please try again.")
                if user_input == "9999":
                    break
            else:
                check = True
        if user_input == "9999":
            self.draw_main()

        # Load a list with all packages and sort by package ID.
        package_list = []
        for value in range(package_hash_table.table.__len__()):
            if package_hash_table.table[value].__len__() != 0:
                for p in package_hash_table.table[value]:
                    package_list.append((int(p[1].id), p[1]))
        package_list.sort(key=lambda tup: tup[0])

        # Print each package's information: ID: id Route/Truck: route_number Status: status_at_time
        for p in package_list:
            if p[1].route == 0:  # If package is unassigned to a route.
                print("Package ID: " + p[1].id + "\tRoute/Truck: Unassigned\t Status: Awaiting Assignment")
            else:
                if p[1].route == 10:  # If route is Truck 1, route 1.
                    status = ""
                    node = r1_0.head  # Start at head of node.
                    while node.package.id != p[1].id:  # Loop through list until finding node.
                        node = node.next
                        if node is None:
                            break
                    if int(r1_0.get_package_delivery_time(graph, node)) < int(user_input):
                        status = "Delivered"  # If the time entered is after the estimated delivery time.
                    else:
                        if int(r1_0.start_time) > int(user_input):
                            status = "Awaiting Truck Departure"  # If time entered is before start time of route.
                        else:
                            status = "Out for Delivery"  # If time entered is after route start but not yet delivered.
                    print("Package ID: " + p[1].id + "\tRoute/Truck: Truck 1 Route 1\t Status: " + status)
                if p[1].route == 11:  # If route is Truck 1, route 2. The rest of the logic is the same as above.
                    status = ""
                    node = r1_1.head
                    while node.package.id != p[1].id:
                        node = node.next
                        if node is None:
                            break
                    if int(r1_1.get_package_delivery_time(graph, node)) < int(user_input):
                        status = "Delivered"
                    else:
                        if int(r1_1.start_time) > int(user_input):
                            status = "Awaiting Truck Departure"
                        else:
                            status = "Out for Delivery"
                    print("Package ID: " + p[1].id + "\tRoute/Truck: Truck 1 Route 2\t Status: " + status)
                if p[1].route == 20:  # If route is Truck 2 route 1. The rest of the logic is the same as above.
                    status = ""
                    node = r2_0.head
                    while node.package.id != p[1].id:
                        node = node.next
                        if node is None:
                            break
                    if int(r2_0.get_package_delivery_time(graph, node)) < int(user_input):
                        status = "Delivered"
                    else:
                        if int(r2_0.start_time) > int(user_input):
                            status = "Awaiting Truck Departure"
                        else:
                            status = "Out for Delivery"
                    print("Package ID: " + p[1].id + "\tRoute/Truck: Truck 2 Route 1\t Status: " + status)
                if p[1].route == 21:  # If route is Truck 2 route 2. The rest of the logic is the same as above.
                    status = ""
                    node = r2_1.head
                    while node.package.id != p[1].id:
                        node = node.next
                        if node is None:
                            break
                    if int(r2_1.get_package_delivery_time(graph, node)) < int(user_input):
                        status = "Delivered"
                    else:
                        if int(r2_1.start_time) > int(user_input):
                            status = "Awaiting Truck Departure"
                        else:
                            status = "Out for Delivery"
                    print("Package ID: " + p[1].id + "\tRoute/Truck: Truck 2 Route 2\t Status: " + status)
        input("Press ENTER to continue...")
        self.draw_main()

    def manual_package_assignment(self):

        # Grabs all packages and sorts them by package ID.
        self.clear()
        package_list = []
        for value in range(package_hash_table.table.__len__()):
            if package_hash_table.table[value].__len__() != 0:
                for p in package_hash_table.table[value]:
                    if p[1].assigned is False and p[1].route == 0:
                        package_list.append((int(p[1].id), p[1]))
        package_list.sort(key=lambda tup: tup[0])

        # Prints header for package data.
        print("\n All Unassigned Packages:\n\nPackage ID\t\tDeliver To\t\t\t\t\t\t\t\t\tDeadline\tAssigned\tNote")

        # Print data per package.
        for package in package_list:
            buffered_address = package[1].destination.address
            address_offset = 40 - len(package[1].destination.address)
            buffered_assignment = str(package[1].assigned)
            if package[1].assigned == True and package[1].route != 0:
                buffered_assignment = "Route " + str(package[1].route)
            for p in range(address_offset):
                buffered_address = buffered_address + " "
            print(package[1].id + "\t\t\t\t" + buffered_address + "\t" + package[1].deadline + "\t\t" +
                  buffered_assignment + "\t\t" + package[1].note)

        # Prompt user to choose a package to view details and optionally assign to a route.
        print("\nPlease choose an option:")
        print("1. View details about or assign a specific package to a route.")
        print("0. Return to main menu.")
        user_choice = input("\n\nEnter a number and press \"Enter\" >")
        check = False
        if user_choice == "1":
            check = True
            self.review_specific_package()
        if user_choice == "0":
            self.draw_main()
        if check is False:
            print("Invalid input! Please try again.")
            print("\n")
            input("Press ENTER to continue...")
            self.review_all_packages()

    def automatic_package_assignment(self):

        #
        # Automatically assigns leftover packages to lists.
        #

        # Grab all packages that are unassigned and have notes.
        self.clear()
        package_list = []
        for value in range(package_hash_table.table.__len__()):
            if package_hash_table.table[value].__len__() != 0:
                for a in package_hash_table.table[value]:
                    if len(a[1].note) != 0 and a[1].route == "0":
                        package_list.append((int(a[1].id), a[1]))
        # If there are still unassigned packages that have notes, skip assignment and go back to main menu.
        if package_list.__len__() > 0:
            print("There are still packages with notes that have not been manually assigned.")
            print("You must manually assign packages with notes before you can automatically assigning other packages.")
            print()
            input("Please press ENTER to continue...")
        else:
            # Assign route in specific order. Truck 1, trip one -> Truck 2, trip one -> Truck 1, trip two -> Truck 2, t2
            r1_0.auto_assign_routes(graph, 10)
            r2_0.auto_assign_routes(graph, 20)
            r1_1.auto_assign_routes(graph, 11)
            r2_1.auto_assign_routes(graph, 21)
            print("Packages assigned successfully.")
            input("Please press ENTER to continue.")
        self.draw_main()

    def assign_package_to_route(self, package_id: int):  # Takes package ID and prompts user to assign that package.
        self.clear()

        # Prompt user.
        print("Add Package To Route:\n")
        print("Which route would you like to add Package ID: " + str(package_id) + " to?")
        count = 0  # Routes are only shown if they are not full in this screen.
        r10 = 0  # In order to properly map user input to the choice presented, count is incremented upon displaying
        r11 = 0  # a route, and the specific value per each route is stored.
        r20 = 0  # The user input is checked against the specific value stored instead of against a simple reference.
        r21 = 0  # This allows the correct choice to be reflected even if not all elements are shown.

        # Print choices.
        if r1_0.size < r1_0.max_nodes:
            count = count + 1
            r10 = count
            print("\n" + str(count) + ". Truck 1, Route 1:\t\tPackages Assigned: " + str(r1_0.size) + "\tSpace Left: " +
                  str(r1_0.max_nodes - r1_0.size) + "\tDeparting Time: " + str(r1_0.start_time))
        if r1_1.size < r1_1.max_nodes:
            count = count + 1
            r11 = count
            print("\n" + str(count) + ". Truck 1, Route 2:\t\tPackages Assigned: " + str(r1_1.size) + "\tSpace Left: " +
                  str(r1_1.max_nodes - r1_1.size) + "\tDeparting Time: " + str(r1_1.start_time))
        if r2_0.size < r2_0.max_nodes:
            count = count + 1
            r20 = count
            print("\n" + str(count) + ". Truck 2, Route 1:\t\tPackages Assigned: " + str(r2_0.size) + "\tSpace Left: " +
                  str(r2_0.max_nodes - r2_0.size) + "\tDeparting Time: " + str(r2_0.start_time))
        if r2_1.size < r2_1.max_nodes:
            count = count + 1
            r21 = count
            print("\n" + str(count) + ". Truck 1, Route 2:\t\tPackages Assigned: " + str(r2_1.size) + "\tSpace Left: " +
                  str(r2_1.max_nodes - r2_1.size) + "\tDeparting Time: " + str(r2_1.start_time))
        print("\n0. Exit\n")

        # Prompt user for a choice. Once a choice is made, add the package to the route.
        check = False
        user_input = None
        while not check:
            if user_input is not None:
                "Invalid Input! Please try again."
            user_input = input("Please enter a number to make a selection: >")
            if user_input == str(r10):
                package = package_hash_table.lookup(package_id)
                package.route = 10
                package.assigned = True
                r1_0.add_node(RouteNode(package))
                check = True
            if user_input == str(r11):
                package = package_hash_table.lookup(package_id)
                package.route = 11
                package.assigned = True
                r1_1.add_node(RouteNode(package))
                check = True
            if user_input == str(r20):
                package = package_hash_table.lookup(package_id)
                package.route = 20
                package.assigned = True
                r2_0.add_node(RouteNode(package))
                check = True
            if user_input == str(r21):
                package = package_hash_table.lookup(package_id)
                package.route = 21
                package.assigned = True
                r2_1.add_node(RouteNode(package))
                check = True
            if user_input == "0":
                check = True
        self.draw_main()

    def print_route_info(self):
        self.clear()  # Clear screen,

        # Print routes along with basic info for the routes before the user is prompted to select a route.
        print("\nPlease select a route to show information for:")
        count = 0
        r10 = 0
        r11 = 0
        r20 = 0
        r21 = 0
        if r1_0.size <= r1_0.max_nodes:
            count = count + 1
            r10 = count
            print("\n" + str(count) + ". Truck 1, Route 1:\t\tPackages Assigned: " + str(r1_0.size) + "\tSpace Left: " +
                  str(r1_0.max_nodes - r1_0.size) + "\tDeparting Time: " + str(r1_0.start_time))
        if r1_1.size <= r1_1.max_nodes:
            count = count + 1
            r11 = count
            print("\n" + str(count) + ". Truck 1, Route 2:\t\tPackages Assigned: " + str(r1_1.size) + "\tSpace Left: " +
                  str(r1_1.max_nodes - r1_1.size) + "\tDeparting Time: " + str(r1_1.start_time))
        if r2_0.size <= r2_0.max_nodes:
            count = count + 1
            r20 = count
            print("\n" + str(count) + ". Truck 2, Route 1:\t\tPackages Assigned: " + str(r2_0.size) + "\tSpace Left: " +
                  str(r2_0.max_nodes - r2_0.size) + "\tDeparting Time: " + str(r2_0.start_time))
        if r2_1.size < r2_1.max_nodes:
            count = count + 1
            r21 = count
            print("\n" + str(count) + ". Truck 1, Route 2:\t\tPackages Assigned: " + str(r2_1.size) + "\tSpace Left: " +
                  str(r2_1.max_nodes - r2_1.size) + "\tDeparting Time: " + str(r2_1.start_time))
        print("\n0. Exit\n")

        # Prompt the user to make a selection. Once the selection is made, print each route stop along with information.
        check = False
        user_input = None
        while not check:
            if user_input is not None:
                "Invalid Input! Please try again."
            user_input = input("Please enter a number to make a selection: >")

            # If choice was Truck 1, Route 1.
            if user_input == str(r10):
                check = True
                self.clear()
                print("\nRoute information for Truck 1 Route 1:\n")
                if r1_0.size == 0:
                    print("No packages assigned to Truck 1 Route 1!")
                for i in range(r1_0.size):
                    count_to_decrement = i
                    node_to_print = r1_0.head
                    while count_to_decrement > 0:
                        node_to_print = node_to_print.next
                        count_to_decrement = count_to_decrement - 1
                    print("Delivery #" + str(i) + ".\t\tPackage ID: " + node_to_print.package.id + "\tApproximate "
                                                                                                   "delivery time: " +
                          r1_0.get_package_delivery_time(graph, node_to_print) + " Deadline Time: " + \
                          node_to_print.package.deadline)
                print("\nWould you like to make any changes to the start time of this route?\n")
                print("1. Yes\nAny other input: No")
                time_change_choice = input("Please enter a number to make a selection:")
                if time_change_choice == "1":
                    time_check = False
                    time_input = None
                    while not time_check:
                        print("What time would you like the route to start?")
                        print("Please provide the time in 4-digit 24-hour time:")
                        print("For example: for 2:00PM, please enter 1400. Alternative enter 9999 to exit to main menu."
                              "\n")
                        time_input = input()
                        if time_input == "9999":
                            break
                        if not time_input.isnumeric() or time_input.__len__() != 4 or int(
                                time_input[2:4]) > 59 or int(
                            time_input[0:2]) > 23:
                            print("Invalid input! Please try again.")
                        else:
                            time_check = True
                    r1_0.set_start_time(int(time_input))

            # If choice was Truck 1, Route 2. Start time for this route is automatically set via route sorting.
            if user_input == str(r11):
                check = True
                self.clear()
                print("\nRoute information for Truck 1 Route 2:\n")
                if r1_1.size == 0:
                    print("No packages assigned to Truck 1 Route 2!")
                for i in range(r1_1.size):
                    count_to_decrement = i
                    node_to_print = r1_1.head
                    while count_to_decrement > 0:
                        node_to_print = node_to_print.next
                        count_to_decrement = count_to_decrement - 1
                    print("Delivery #" + str(i) + ".\t\tPackage ID: " + node_to_print.package.id + "\tApproximate "
                                                                                                   "delivery time: "
                          + r1_1.get_package_delivery_time(graph, node_to_print) + " Deadline Time: " + \
                          node_to_print.package.deadline)

            # If choice was Truck 2, Route 1.
            if user_input == str(r20):
                check = True
                self.clear()
                print("\nRoute information for Truck 2 Route 1:\n")
                if r2_0.size == 0:
                    print("No packages assigned to Truck 2 Route 1!")
                for i in range(r2_0.size):
                    count_to_decrement = i
                    node_to_print = r2_0.head
                    while count_to_decrement > 0:
                        node_to_print = node_to_print.next
                        count_to_decrement = count_to_decrement - 1
                    print("Delivery #" + str(i) + ".\t\tPackage ID: " + node_to_print.package.id + "\tApproximate "
                                                                                                   "delivery time: "
                          + r2_0.get_package_delivery_time(graph,
                                                           node_to_print) + " Deadline Time: " \
                          + node_to_print.package.deadline)
                print("\nWould you like to make any changes to the start time of this route?\n")
                print("1. Yes\nAny other input: No")
                time_change_choice = input("Please enter a number to make a selection:")
                if time_change_choice == "1":
                    time_check = False
                    time_input = None
                    while not time_check:
                        print("What time would you like the route to start?")
                        print("Please provide the time in 4-digit 24-hour time:")
                        print("For example: for 2:00PM, please enter 1400. Alternative enter 9999 to exit to main menu."
                              "\n")
                        time_input = input()
                        if time_input == "9999":
                            break
                        if not time_input.isnumeric() or time_input.__len__() != 4 or int(
                                time_input[2:4]) > 59 or int(
                            time_input[0:2]) > 23:
                            print("Invalid input! Please try again.")
                        else:
                            time_check = True
                    r2_0.set_start_time(int(time_input))

            # If choice was Truck 2, Route 2. Start time for this route is automatically set via route sorting.
            if user_input == str(r21):
                check = True
                self.clear()
                print("\nRoute information for Truck 2 Route 2:\n")
                if r2_1.size == 0:
                    print("No packages assigned to Truck 1 Route 2!")
                for i in range(r2_1.size):
                    count_to_decrement = i
                    node_to_print = r2_1.head
                    while count_to_decrement > 0:
                        node_to_print = node_to_print.next
                        count_to_decrement = count_to_decrement - 1
                    print("Delivery #" + str(i) + ".\t\tPackage ID: " + node_to_print.package.id + "\tApproximate "
                                                                                                   "delivery time: "
                          + r2_1.get_package_delivery_time(graph,
                                                           node_to_print) + " Deadline Time: "
                          + node_to_print.package.deadline)
            if user_input == "0":
                check = True
            else:
                input("\nPlease press ENTER to continue...")
        self.draw_main()


gui = GUI()
gui.draw_main()
