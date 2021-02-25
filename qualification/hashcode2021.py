from collections import deque

class Street:

    def __init__(self, start, end, name, length):
        self.length, self.name, self.start, self.end = length, name, start, end


class Intersection:

    def __init__(self, id):
        self.id, self.in_streets, self.out_streets = id, [], []
        self.green = None
        self.car_queues = {}

    def add_car_to_queue(self, car, street):
        if street.name not in self.car_queues.keys():
            self.car_queues[street.name] = []
        self.car_queues[street.name].append(car)

    def remove_car_from_queue(self, street):
        return self.car_queues[street.name].popleft()

    def add_in_street(self, street):
        self.in_streets.append(street)

    def add_out_street(self, street):
        self.out_streets.append(street)

class Car:

    def __init__(self, path):
        self.path = path


input_file = 'a.txt'
with open(input_file) as f:
    lines = f.readlines()

    duration, num_inter, num_streets, num_cars, bonus = lines[0].split()

    duration = int(duration)
    num_inter = int(num_inter)
    num_streets = int(num_streets)
    num_cars = int(num_cars)

    streets = {}
    intersections = {}
    for street in lines[1:num_streets+1]:
        start, end, name, length = street.split()
        streets[name] = Street(start, end, name, length)

        if start not in intersections.keys():
            intersections[start] = Intersection(start)
        intersections[start].add_in_street(streets[name])

        if end not in intersections.keys():
            intersections[end] = Intersection(end)
        intersections[end].add_out_street(streets[name])

    cars = []
    for car in lines[num_streets+1:]:
        path = []
        for street in car.split()[1:]:
            path.append(streets[street])
        car_obj = Car(path)
        cars.append(car_obj)

        intersections[path[0].end].add_car_to_queue(car_obj, path[0])

    # simulation
    #for t in range(duration):


    
