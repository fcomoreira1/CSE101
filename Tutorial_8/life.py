# from graph import GraphicalLife

class Point:
    """
    Encodes a live point in the Game of Life.
    Data attributes: (x,y) the coordinates
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'

    def __eq__(self, other) -> bool:
        return other.x == self.x and other.y == self.y

    def __hash__(self) -> int:
        # We are assuming (x, y) are immutable here 
        return hash((self.x, self. y))

    def get_neighbors(self) -> set:
        neighbors = set() 
        for i in range(-1,2):
            for j in range(-1,2):
                if i == j and j == 0:
                    continue
                neighbors.add(Point(self.x + j, self.y + i))

        return neighbors


class Board:
    """
    A Board to play the Game of Life on.
    Attributes: points -> a set of points
                x_size -> size in the x-direction
                y_size -> size in the y-direction
    """
    def __init__(self, x_size, y_size, points):
        self.points = points
        self.x_size = x_size
        self.y_size = y_size

    def is_legal(self, point) -> bool:
        """ Check if a Point is in the board"""
        return (0 <= point.x and point.x < self.x_size and 0 <= point.y and point.y < self.y_size)

    def number_live_neighbors(self, p) -> int:
        """ Compute the number of live neighbors of p on the Board."""
        neighbors = p.get_neighbors()
        q_alive_neighbors = 0
        for point in neighbors:
            if self.is_legal(point) and point in self.points:
                q_alive_neighbors += 1

        return q_alive_neighbors

    def next_step(self):
        """ Compute the points alive in the next round and update the points of the Board """
        alive_points = set()
        for i in range(self.x_size):
            for j in range(self.y_size):
                alive_neighbors = self.number_live_neighbors(Point(i,j))
                if alive_neighbors == 2  or alive_neighbors == 3:
                    if Point(i,j) not in self.points and alive_neighbors == 3:
                        alive_points.add(Point(i,j))
                    if Point(i,j) in self.points:
                        alive_points.add(Point(i,j))

        self.points = alive_points

    def load_from_file(self, filename):
        """Load a board configuration from file in the following format:
        - The first two lines contain a number representing the size in
            x- and y-coordinates, respectively.
        - Each of the following lines gives the coordinates of a single
            point, with the two coordinate values separated by a comma.
            Those are the points that are alive on the board.
        """
        with open(filename, 'r') as file:
            first_line = file.readline()
            first_line.rstrip()
            second_line = file.readline()
            second_line.rstrip()
            self.x_size = int(first_line)
            self.y_size = int(second_line)
            new_points = set()
            for line in file:
                filtered_line = line.rstrip().split(',')
                 
                new_points.add(Point(int(filtered_line[0]), int(filtered_line[1])))

            self.points = new_points

    def toggle_point(self, x, y):
        """Add Point(x,y) if it is not in points, otherwise delete it
        from points.
        """
        if Point(x,y) in self.points:
            self.points.discard(Point(x,y))
        else:
            self.points.add(Point(x,y))

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(str(self.x_size))
            file.write('\n')
            file.write(str(self.y_size))
            file.write('\n')
            for point in self.points:
                file.write(f"{point.x},{point.y}\n")

def is_periodic(board):
    existent_boards = [board.points]
    while True:
        board.next_step()
        for i in range(len(existent_boards)):
            if existent_boards[i] == board.points:
                if i == 0:
                    return (True, 0)
                else:
                    return (False, i)

        existent_boards.append(board.points)

class TextView:
    """A text visualization of Board instances.
    Data attributes:
    ...
    """
    def __init__(self, board):
        # Initialize the board...
        self.board = board

    def show(self):
        print('o'*(self.board.x_size + 2))
        for j in range(self.board.y_size):
            print('o', end='')
            for i in range(self.board.x_size):
                if Point(i,j) in self.board.points:
                    print('X', end='')
                else:
                    print(' ', end='')
            print('o')
        print('o'*(self.board.x_size + 2))

    def tick(self):
        """Advance one step forward in time."""
        input('Press Enter for next step')



class LifeGame:
    """The game loop for the text based Game of Life.
    Data attributes:
    board -- the game board
    view  -- a TextView to visualize the game
    """

    def __init__(self, board):
        # Initialize the board and create a TextView for it.
        self.board = board
        self.view = TextView(board)
    def run(self, steps):
        """Run the game of life for the given number of steps.
        At every step, show the board and prompt the user to continue
        by calling tick() on the TextView.
        """
        for _ in range(steps):
            self.view.show()
            self.board.next_step()
            self.view.tick()


