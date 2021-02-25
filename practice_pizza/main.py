import sys
import heapq


# classes
class Pizza:
    def __init__(self, identifier, ingredients):
        self.identifier = identifier
        self.ingredients = ingredients

    def num_ingredients(self):
        return len(self.ingredients)

    def __lt__(self, other):
        return self.num_ingredients() <  other.num_ingredients()

class Teams:
    def __init__(self, team_size, num_teams):
        self.team_size = team_size
        self.num_teams = num_teams


# main
input_file = sys.argv[1]
with open(input_file) as f:
    lines = f.readlines()

    # read input file
    all_teams = []
    team_size = 2
    for num_teams in lines[0].split()[1:]:
        all_teams.append(Teams(team_size, int(num_teams)))
        team_size +=1

    pizzas = []
    identifier = 0
    for line in lines[1:]:
        ingredients = line.split()[1:]
        heapq.heappush(pizzas, Pizza(identifier, ingredients))
        identifier += 1 

    # make delivieries
    deliveries = []
    for teams in all_teams:
        for i in range(teams.num_teams):
            delivery = str(teams.team_size) + ' '
            for i in range(teams.team_size):
                if len(pizzas) == 0:
                    break
                pizza = heapq.heappop(pizzas)
                delivery += str(pizza.identifier) + ' '

            if len(pizzas) != 0:
                deliveries.append(delivery)

    # write output file
    with open(input_file + '.out', 'w') as out:
        out.write(str(len(deliveries)))
        out.write('\n')
        for delivery in deliveries:
            out.write(delivery)
            out.write('\n')
