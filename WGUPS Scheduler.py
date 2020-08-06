# Tylen Wells twell56

import csv
from os import system, name
import time
import sys


class Package:

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

    def __init__(self, address: str, city: str, state: str, zip_code: str) -> None:
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code


class RouteNode:

    def __init__(self, package):
        self.package = package
        self.vertex = None
        for i in vertex_list:
            if i.destination.address == self.package.destination.address:
                self.vertex = i
        self.next = None


class RouteList:

    def __init__(self, truck: int, max_nodes=15):
        self.truck = truck  # If value of truck is 0, this route has not had a truck assigned yet.
        self.head = None
        self.tail = None
        self.size = 0
        self.max_nodes = max_nodes  # This is the maximum number of packages allowed per route.
        self.active = False
        self.start_time = "0800"

    def set_start_time(self, start_time: int):  # Ensures start time is set as an 4 digit number between 0800 and 1200.
        if start_time > 1200 or start_time < 800:
            return None
        else:
            buffered_time = str(start_time)
            if buffered_time.__len__() == 3:
                buffered_time = "0" + buffered_time
            self.start_time = buffered_time

    def add_node(self, new_node: RouteNode = None, new_node_list=None, *args):
        if new_node is not None and new_node_list is None:
            if self.size == 0:
                self.head = new_node
                self.tail = new_node
                self.size = 1
                self.active = True
            else:
                self.tail.next = new_node
                self.tail = new_node
                self.size = self.size + 1
                self.sort_route(graph)
        if new_node_list is not None and new_node is None:
            if self.size == 0:
                self.head = new_node_list[0]
                self.tail = new_node_list[0]
                self.size = 1
                self.active = True
                new_node_list.remove(new_node_list[0])
            for node in new_node_list:
                self.tail.next = node
                self.tail = node
                self.size = self.size + 1
            self.sort_route(graph)

    def sort_route(self, graph):
        list_to_sort = []  # List to aggregate nodes that have been added to this route.
        for r in range(self.size):  # Adds all nodes in route to the list.
            buffer = r
            node_to_add = self.head
            while buffer > 0:
                node_to_add = node_to_add.next
                buffer = buffer - 1
            list_to_sort.append(node_to_add)
        selected_node = (0.0, None)  # Buffer to hold highest distance node from Hub, this will be our first stop.
        for node in list_to_sort:  # Get Distance from Hub to Node, store it if it's higher than selected_node.
            distance = graph.edge_weights.get((vertex_list[0], node.vertex))
            if distance > selected_node[0]:
                selected_node = (distance, node)
        self.head = selected_node[1]  # Adds furthest node to the head of the route. This will be our first stop.
        self.tail = selected_node[1]
        list_to_sort.remove(selected_node[1])  # Remove the head node from the list to sort as it has been sorted.
        while list_to_sort.__len__() > 0:
            selected_node = (0.0, None)
            for node in list_to_sort:
                distance = graph.edge_weights.get((self.tail.vertex, node.vertex))
                if distance > selected_node[0]:
                    selected_node = (distance, node)
            self.tail.next = selected_node[1]
            self.tail = selected_node[1]
            list_to_sort.remove(selected_node[1])

        #
        # Update Start Times of Route 2 for each Truck.
        #
        r1_0_last_package_time = self.get_package_delivery_time(graph, r1_0.tail)
        r2_0_last_package_time = self.get_package_delivery_time(graph, r2_0.tail)
        r1_0_minutes_to_add = (graph.edge_weights.get((vertex_list[0], r1_0.tail.vertex)) * 60) / 18
        r2_0_minutes_to_add = (graph.edge_weights.get((vertex_list[0], r2_0.tail.vertex)) * 60) / 18
        r1_0_hours_to_add = int(r1_0_minutes_to_add / 60)
        r1_0_minutes_to_add = round((r1_0_minutes_to_add % 60) + int(r1_0_last_package_time[2]
                                                                     + r1_0_last_package_time[3]))
        if r1_0_minutes_to_add > 59:
            r1_0_hours_to_add = r1_0_hours_to_add + 1
            r1_0_minutes_to_add = r1_0_minutes_to_add - 60
        r1_0_start_hours = str(int(r1_0_last_package_time[0:2]) + r1_0_hours_to_add)
        r1_0_start_minutes = str(r1_0_minutes_to_add)
        if r1_0_start_hours.__len__() != 2:
            r1_0_start_hours = "0" + r1_0_start_hours
        if r1_0_start_minutes.__len__() != 2:
            r1_0_start_minutes = "0" + r1_0_start_minutes
        r1_1.set_start_time(r1_0_start_hours + r1_0_start_minutes)

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
        r2_1.set_start_time(r2_0_start_hours + r2_0_start_minutes)

    def get_package_delivery_time(self, graph, node) -> str:
        current = self.head
        next = current.next
        total_distance = graph.edge_weights.get((vertex_list[0], current.vertex))
        for i in range(self.size):
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
            if current.next is not None:
                total_distance = total_distance + graph.edge_weights.get((current.vertex, next.vertex))
                current = current.next
                next = current.next

    def auto_assign_routes(self, route_number: int):
        unassigned_packages = []
        for value in range(package_hash_table.table.__len__()):  # Get list of all packages that are unassigned.
            if package_hash_table.table[value].__len__() != 0:
                for a in package_hash_table.table[value]:
                    if a[1].route == "0":
                        unassigned_packages.append(a[1])
        if self.size == 0:  # If route has no nodes.
            node_to_add = None
            for package in unassigned_packages:  # Find furthest node and use it as starting node.
                v = None
                for i in vertex_list:
                    if i.destination.address == package.destination.address:
                        v = i
                distance = graph.edge_weights.get((vertex_list[0], v))
                if distance > node_to_add[0]:
                    node_to_add = (distance, package)
            self.add_node(RouteNode(node_to_add[1]))
            node_to_add[1].route = route_number
            node_to_add[1].assigned = True
            unassigned_packages.remove(node_to_add[1])
            node_to_add = None
            while self.size < self.max_nodes:
                for package in unassigned_packages:
                    v = None
                    for i in vertex_list:
                        if i.destination.address == package.destination.address:
                            v = i
                    distance = graph.edge_weights.get((self.tail.vertex, v))
                    if distance < node_to_add[0]:
                        node_to_add = (distance, package)
                self.add_node(RouteNode(node_to_add[1]))
                node_to_add[1].route = route_number
                node_to_add[1].assigned = True
                unassigned_packages.remove(node_to_add[1])
        else:
            node_to_add = None
            while self.size < self.max_nodes:
                for package in unassigned_packages:
                    v = None
                    for i in vertex_list:
                        if i.destination.address == package.destination.address:
                            v = i
                    distance = graph.edge_weights.get((self.tail.vertex, v))
                    if distance < node_to_add[0]:
                        node_to_add = (distance, package)
                self.add_node(RouteNode(node_to_add[1]))
                node_to_add[1].route = route_number
                node_to_add[1].assigned = True
                unassigned_packages.remove(node_to_add[1])


# noinspection PyRedeclaration
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

    def insert(self, package: Package) -> None:
        package = package
        key = self._generate_key(package.id)
        self._add_to_list(key, package)

    def __count__(self, reference_string="") -> int:
        count = 0
        if reference_string is "":
            for value in range(self.table.__len__()):
                count = count + self.table[value].__len__()
        if reference_string is "note":
            for value in range(self.table.__len__()):
                if self.table[value].__len__() != 0 and len(self.table[value][0][1].note) != 0:
                    count = count + 1
        if reference_string is "unresolved":
            for value in range(self.table.__len__()):
                if self.table[value].__len__() != 0 and len(self.table[value][0][1].note) != 0 and \
                        self.table[value][0][1].route == 0:
                    count = count + 1
        if reference_string is "unassigned":
            for value in range(self.table.__len__()):
                if self.table[value].__len__() != 0 and self.table[value][0][1].route == 0:
                    count = count + 1
        return count

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
                 package_note)

    package_hash_table.insert(p1)

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
        pass

    @staticmethod
    def clear():
        if name == 'nt':
            _ = system('cls')
        if name == 'posix':
            _ = system('clear')

    def draw_main(self):

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
        if user_choice == "1":
            check = True
            self.review_packages_with_notes()
        if user_choice == "2":
            check = True
            self.review_all_packages()
        if user_choice == "3":
            check = True
            self.review_specific_package()
        if user_choice == "4":
            check = True
            self.review_packages_temporal()
        if user_choice == "5":
            check = True
            self.manual_package_assignment()
        if user_choice == "6":
            check = True
            self.automatic_package_assignment()
        if user_choice == "7":
            check = True
            self.print_route_info()
        if user_choice == "0":
            sys.exit()
        if check is False:
            print("Invalid input! Please try again.")
            print("\n")
            input("Press ENTER to continue...")
            self.draw_main()

    def review_packages_with_notes(self):
        self.clear()
        package_list = []
        for value in range(package_hash_table.table.__len__()):
            if package_hash_table.table[value].__len__() != 0:
                for a in package_hash_table.table[value]:
                    if len(a[1].note) != 0:
                        package_list.append((int(a[1].id), a[1]))
        package_list.sort(key=lambda tup: tup[0])
        print("\n All Packages with Notes:\n\nPackage ID\t\tDeliver To\t\t\t\t\t\t\t\t\tDeadline\tAssigned\tNote")
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
        self.clear()
        package_list = []
        for value in range(package_hash_table.table.__len__()):
            if package_hash_table.table[value].__len__() != 0:
                for p in package_hash_table.table[value]:
                    package_list.append((int(p[1].id), p[1]))
        package_list.sort(key=lambda tup: tup[0])
        print("\n All Packages:\n\nPackage ID\t\tDeliver To\t\t\t\t\t\t\t\t\tDeadline\tAssigned\tNote")
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
        print('\nWhich Package ID would you like to review?:')
        user_input = input("Please input a Package ID: >")
        check = False
        found_package = None
        if user_input.isnumeric():
            found_package = package_hash_table.lookup(user_input)
            if found_package is not None:
                check = True
        if not check:
            print("Package ID: " + user_input + " was not found. Please try again!")
            self.review_specific_package()
        self.clear()
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
        else:
            print("\n")
            input("This package has already been assigned to a route. Please press ENTER to return to the main menu.")
            self.draw_main()

    def review_packages_temporal(self):
        self.clear()
        print("Review status of all packages at a specific time: \n")
        print("Please input the 4-digit 24-hour clock numeric time you would like to review package status at: ")
        print("For example: for 2:00PM, please enter 1400. Alternative enter 9999 to exit to main menu.\n")
        user_input = input()
        check = False
        if user_input == "9999":
            check = True
        while not check:
            if not user_input.isnumeric() or user_input.__len__() != 4 or int(user_input[2:4]) > 60 or int(
                    user_input[0:2]) > 23:

                user_input = input("Invalid Input! Please try again.")
                if user_input == "9999":
                    break
            else:
                check = True
        if user_input == "9999":
            self.draw_main()
        package_list = []
        for value in range(package_hash_table.table.__len__()):
            if package_hash_table.table[value].__len__() != 0:
                for p in package_hash_table.table[value]:
                    package_list.append((int(p[1].id), p[1]))
        package_list.sort(key=lambda tup: tup[0])
        for p in package_list:
            if p[1].route == 0:  # If package is unassigned to a route.
                print("Package ID: " + p[1].id + "\tRoute/Truck: Unassigned\t Status: Awaiting Assignment")
            else:
                if p[1].route == 10:
                    status = ""
                    node = r1_0.head
                    while node.package.id != p[1].id:
                        node = node.next
                        if node is None:
                            break
                    if int(r1_0.get_package_delivery_time(graph, node)) < int(user_input):
                        status = "Delivered"
                    else:
                        if int(r1_0.start_time) > int(user_input):
                            status = "Awaiting Truck Departure"
                        else:
                            status = "Out for Delivery"
                    print("Package ID: " + p[1].id + "\tRoute/Truck: Truck 1 Route 1\t Status: " + status)
                if p[1].route == 11:
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
                if p[1].route == 20:
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
                if p[1].route == 21:
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
                    print("Package ID: " + p[1].id + "\tRoute/Truck: Truck 2 Route 2\t Status: " + status)
        input("Press ENTER to continue...")
        self.draw_main()

    def manual_package_assignment(self):
        self.clear()
        package_list = []
        for value in range(package_hash_table.table.__len__()):
            if package_hash_table.table[value].__len__() != 0:
                for p in package_hash_table.table[value]:
                    if p[1].assigned is False and p[1].route == 0:
                        package_list.append((int(p[1].id), p[1]))
        package_list.sort(key=lambda tup: tup[0])
        print("\n All Unassigned Packages:\n\nPackage ID\t\tDeliver To\t\t\t\t\t\t\t\t\tDeadline\tAssigned\tNote")
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
        self.clear()
        package_list = []
        for value in range(package_hash_table.table.__len__()):
            if package_hash_table.table[value].__len__() != 0:
                for a in package_hash_table.table[value]:
                    if len(a[1].note) != 0 and a[1].route == "0":
                        package_list.append((int(a[1].id), a[1]))
        if package_list.__len__() > 0:
            print("There are still packages with notes that have not been manually assigned.")
            print("You must manually assign packages with notes before you can automatically assigning other packages.")
            print()
            input("Please press ENTER to continue...")
        else:
            r1_0.auto_assign_routes(10)
            r2_0.auto_assign_routes(11)
            r1_1.auto_assign_routes(20)
            r2_1.auto_assign_routes(21)
            print("Packages assigned successfully.")
            input("Please press ENTER to continue.")
        self.draw_main()

    def assign_package_to_route(self, package_id: int):
        # TODO Fix Algo/Function and check deadline times as well as second routes start times.
        self.clear()
        print("Add Package To Route:\n")
        print("Which route would you like to add Package ID: " + str(package_id) + " to?")
        count = 0
        r10 = 0
        r11 = 0
        r20 = 0
        r21 = 0
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

        check = False
        user_input = None
        while not check:
            if user_input is not None:
                "Invalid Input! Please try again."
            user_input = input("Please enter a number to make a selection: >")
            if user_input == str(r10):
                package = package_hash_table.lookup(package_id)
                r1_0.add_node(RouteNode(package))
                package.route = 10
                package.assigned = True
                check = True
            if user_input == str(r11):
                package = package_hash_table.lookup(package_id)
                r1_1.add_node(RouteNode(package))
                package.route = 11
                package.assigned = True
                check = True
            if user_input == str(r20):
                package = package_hash_table.lookup(package_id)
                r2_0.add_node(RouteNode(package))
                package.route = 20
                package.assigned = True
                check = True
            if user_input == str(r21):
                package = package_hash_table.lookup(package_id)
                r2_1.add_node(RouteNode(package))
                package.route = 21
                package.assigned = True
                check = True
            if user_input == "0":
                check = True
        self.draw_main()

    def print_route_info(self):  # PRINT ROUTE INFO
        self.clear()
        print("\nPlease select a route to show information for:")
        count = 0
        r10 = 0
        r11 = 0
        r20 = 0
        r21 = 0
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

        check = False
        user_input = None
        while not check:
            if user_input is not None:
                "Invalid Input! Please try again."
            user_input = input("Please enter a number to make a selection: >")
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


r2_1.set_start_time(905)
gui = GUI()
gui.draw_main()
