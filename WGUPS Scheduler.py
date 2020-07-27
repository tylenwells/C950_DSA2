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
        for i in range(initial_capacity):   # Fill list with (initial_capacity) empty lists as bucket placeholders.
            self.table.append([])

    def _generate_key(self, key):
        self.key_buffer = key * 9001
        return self.key_buffer % 64

    def insert(self, package_id, address, deadline, city, state, zip_code, weight, status, note=""):
        destination = Destination(address, city, state, zip_code)
        package = Package(package_id, destination, deadline, weight, status, note)
        key = self._generate_key(package.id)

        if self.table[key].__len__() is 0:
            self.table[key] = [(package.id, package)]
        else   # TODO Implement remainder of hash table