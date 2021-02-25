from collections import deque
import sys 
class Street:

    def __init__(self, start, end, name, length):
        self.length, self.name, self.start, self.end = length, name, start, end


class Intersection:

    def __init__(self, id, duration):
        self.id, self.in_streets, self.out_streets = id, [], []
        self.green = None
        self.car_queues = {}
        self.schedule = []
        self.duration = duration

    def add_car_to_queue(self, car, street):
        if street.name not in self.car_queues.keys():
            self.car_queues[street.name] = deque() 
        self.car_queues[street.name].append(car)

    def remove_car_from_queue(self, street):
        return self.car_queues[street.name].popleft()

    def add_in_street(self, street):
        self.in_streets.append(street)
        if len(self.schedule) == 0:
            self.schedule = [street.name for i in range(self.duration)]

    def add_out_street(self, street):
        self.out_streets.append(street)

    def get_busiest_street(self):
        max_cars = 0
        busiest_street = ''

        for street in self.car_queues.keys():
            if len(self.car_queues[street]) > max_cars:
                busiest_street = street
                max_cars = len(self.car_queues[street])

        return busiest_street

class Car:

    def __init__(self, path):
        self.path = path
        self.distance_to_go = 0
        self.current_idx_of_path = 0

    def cross_intersection(self):
        if self.current_idx_of_path >= len(self.path) - 1:
            return
        self.current_idx_of_path += 1
        self.distance_to_go = self.path[self.current_idx_of_path].length + 1

    def move(self):
        self.distance_to_go -= 1

    def get_target_intersection(self):
        return self.path[self.current_idx_of_path].end

    def get_street(self):
        return self.path[self.current_idx_of_path]



input_file = sys.argv[1]
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
        start = int(start)
        end = int(end)
        length = int(length)
        streets[name] = Street(start, end, name, length)

        if start not in intersections.keys():
            intersections[start] = Intersection(start, duration)
        intersections[start].add_out_street(streets[name])

        if end not in intersections.keys():
            intersections[end] = Intersection(end, duration)
        intersections[end].add_in_street(streets[name])

    cars = []
    for car in lines[num_streets+1:]:
        path = []
        for street in car.split()[1:]:
            path.append(streets[street])
        car_obj = Car(path)
        cars.append(car_obj)

        intersections[path[0].end].add_car_to_queue(car_obj, path[0])

    # simulation
    print("start simulation")
    for t in range(duration):
        for id in intersections.keys():
            intersection = intersections[id]
            if intersection.get_busiest_street() != '':
                intersection.green = intersection.get_busiest_street()
                if intersection.green not in set(intersection.schedule):
                    for s in intersection.schedule[t:]:
                        s = intersection.green
                    car = intersection.remove_car_from_queue(streets[intersection.green])
                    car.cross_intersection()   
                           

        for car in cars:
            if car.distance_to_go > 0:
                car.move() 
            else:
                intersections[car.get_target_intersection()].add_car_to_queue(car, car.get_street())

        t+=1

    print("end simulation")

#output
with open(input_file + '.out', 'w') as out:
    out.write(str(len(intersections.keys())))
    out.write('\n')
    for intersection_key in intersections.keys():
        intersection = intersections[intersection_key]
        out.write(str(intersection.id))
        out.write('\n')
        out.write(str(len(set(intersection.schedule))))
        out.write('\n')
        counter = 0
        street_name = intersection.schedule[0]
        for idx, street in enumerate(intersection.schedule):
            counter += 1
            if street != street_name:
                out.write(street_name + " " + str(counter))
                out.write('\n')
                counter = 0
                street_name = street
            elif idx == len(intersection.schedule) - 1:
                out.write(street_name + " " + str(counter))
                out.write('\n')



    
