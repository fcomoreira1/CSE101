import random
import graphics

class Ship:
    """A ship that can be placed on the grid."""

    def __repr__(self):
        return f"Ship('{self.name}', {self.positions})"
    
    def __str__(self):
        return f'{repr(self)} with hits {self.hits}'

    def __init__(self, name, positions):
        self.name = name
        self.positions = positions
        self.hits = set()

    def __eq__(self, other):
        return self.name == other.name and self.positions == other.positions and self.hits == other.hits

    def is_afloat(self):
        """Check if here are any positions of the ship that have not been hit"""
        for position in self.positions:
            if position not in self.hits:
                return True

        return False

    def take_shot(self, shot):
        """Check if the shot hits the ship. If so, remember the hit.
        Returns one of 'MISS', 'HIT', or 'DESTROYED'.
        """
        if shot in self.positions and shot not in self.hits:
            self.hits.add(shot)
            if len(self.hits) == len(self.positions):
                return 'DESTROYED'
            else:
                return 'HIT'
        return 'MISS'

class Grid:
    """Encodes the grid on which the Ships are placed.
    Also remembers the shots fired that missed all of the Ships.
    """
    ship_types = [('Battleship',4),('Carrier',5),('Cruiser',3),('Destroyer',2),('Submarine',3)]
    
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.ships = []
        self.misses = set()
        self.sunken_ships = []
        self.hits = set() 

    def add_ship(self, ship):
        """
        Add a Ship to the grid at the end of the ships list if it does not
        collide with other ships already there
        """
        for position in ship.positions:
            for othership in self.ships:
                for otherposition in othership.positions:
                    if position == otherposition:
                        return

        self.ships.append(ship)

    def shoot(self, position):
        for ship in self.ships:
            output = ship.take_shot(position)
            if output == 'DESTROYED':
                self.hits.add(position)
                self.sunken_ships.append(ship)
                return (output, ship)
            if output == 'HIT':
                self.hits.add(position)
                return (output, None)

        self.misses.add(position)
        return ('MISS', None)

    def random_ship(self):
        q_ships = len(self.ships)
        dir = [(1,0), (0,1), (-1,0), (0,-1)]
        while q_ships == len(self.ships):
            i = random.randint(1,self.x_size)
            j = random.randint(1,self.y_size)
            indx = random.randint(0,3)
            k = random.choice(self.ship_types)
            positions = set()
            if i + k[1] * dir[indx][0] <= self.x_size and i + k[1] * dir[indx][0] >= 1:
                if j + k[1] * dir[indx][1] <= self.y_size and j + k[1] * dir[indx][1] >= 1:
                    for t in range(k[1]):
                        positions.add((i+t*dir[indx][0], j + t*dir[indx][1]))

            if len(positions) != k[1]:
                continue
            
            self.add_ship(Ship(k[0], positions))
            if q_ships != len(self.ships):
                return Ship(k[0], positions)

    def create_random(self,n):
        while len(self.ships) < n:
            self.random_ship()

class BlindGrid:
    """Encodes the opponent's view of the grid."""

    def __init__(self, grid):
        self.x_size = grid.x_size
        self.y_size = grid.y_size
        self.misses = grid.misses
        self.hits = grid.hits
        self.sunken_ships = grid.sunken_ships 


def create_ship_from_line(line):
    list = line.split(' ')
    positions = set()
    for i in range(1,len(list)):
        a, b = list[i].split(':')
        positions.add((int(a), int(b)))

    return Ship(list[0], positions)

def load_grid_from_file(filename):
    with open(filename, 'r') as file:
        line = file.readline()
        x_size, y_size = map(int, line.split(':'))
        g = Grid(x_size, y_size)
        for line in file:
            g.add_ship(create_ship_from_line(line))

        return g
    
