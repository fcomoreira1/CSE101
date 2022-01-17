from os import remove


def split_type(line):
    """Splits off the first word in the line and returns both parts in a tuple.
    Also eliminates all leading and trailing spaces.
    Example:
        split_type('ROW ##.##') returns ('ROW', '##.##')
        split_type('CLUE (0,1) down: Of or pertaining to the voice (5)') returns
            ('CLUE', '(0,1) down: Of or pertaining to the voice (5)')
        split_type('  ROW    ##.##   ') returns ('ROW', '##.##')

    """
    new_list = line.split(" ")
    while '' in new_list:
        new_list.remove('')
    return (new_list[0], ' '.join(new_list[1:]))

def remove_multiple_spaces(sentence):
    list = sentence.split(' ')
    while '' in list:
        list.remove('')
    return str(' '.join(list))

def read_row(row):
    """Reads a row of a crossword puzzle and decomposes it into a list. Every
    '#' is blocking the current box. Letters 'A', ..., 'Z' and 'a', ..., 'z'
    are values that are already filled into the box. These letters are capitalized
    and then put into the list. All other characters stand
    for empty boxes which are represented by a space ' ' in the list.
    Examples:
        read_row('#.#') gives ['#', ' ', '#']
        read_row('C.T') gives ['C', ' ', 'T']
        read_row('cat') gives ['C', 'A', 'T']
    """
    
    lower = 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
    upper = 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
    list = []
    for char in row:
        if char in lower:
            list.append(char.upper())
        elif char in upper:
            list.append(char)
        elif char == '#':
            list.append('#')
        else:
            list.append(' ')
    return list

def coord_to_int(coordstring):
    """Reads a coordinate into a couple in the following way: The input is of the form
        '(x,y)' where x, y are integers. The output should then be
        (x, y), where (x, y) is a tuple of values of type int.
    None of these values are strings.
    Example:
        coord_to_int('(0,1)') returns
        (0, 1)
    """
    comma = coordstring.find(',')
    first_int = int(coordstring[1:comma])
    second_int = int(coordstring[comma+1:-1])
    return (first_int, second_int)

def read_clue(cluestring):
    """Reads a clue into a tuple in the following way: The input is of the form
        '(x,y) direction: question (length)'
    where x, y and length are integers, direction is 'across' or 'down'
    and question is the text of the clue. The output should then be
        ((x, y), direction, length, question)
    where (x, y) is a tuple of values of type int and length is of type int.
    There may be arbitrarily many spaces between the different parts of the input.
    Example:
        read_clue('(0,1) down: Of or pertaining to the voice (5)') returns
        ((0, 1), 'down', 5, 'Of or pertaining to the voice')
    """
    cluestring = remove_multiple_spaces(cluestring) 
    out_list = cluestring.split(' ', 2)
    out_list[0] = coord_to_int(out_list[0])
    out_list[1] = out_list[1].replace(':', '')
    hint = out_list[2]
    open_par = hint.find('(')
    close_par = hint.find(')')
    size_word = int(hint[open_par + 1 : close_par])
    out_list[2] = size_word
    out_list.append(hint[:open_par - 1])
    return tuple(out_list)

def read_file(filename):
    """Opens the file with the given filename and creates the puzzle in it.
    Returns a pair consisting of the puzzle grid and the list of clues. Assumes
    that the first line gives the size. Afterwards, the rows and clues are given.
    The description of the rows and clues may interleave arbitrarily.
    """
    size = 0
    out_list = []
    rows = []
    clues = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.replace('\n', '')
            line = split_type(line)
            if line[0] == 'SIZE':
                size = int(line[1])
            elif line[0] == 'ROW':
                rows.append(read_row(line[1]))
            else:
                clues.append(read_clue(line[1]))
        return (rows, clues)
def create_clue_string(clue):
    """ Given a clue, which is a tuple
    (position, direction, length, question),
    create a string in the form 'position direction: question (length)'.
    For example, given the clue
        ((2, 3), 'across', 4, 'Black bird'),
    this function will return
        '(2,3) across: Black bird (4)'
    """
    coordinate = str(clue[0])
    coordinate = coordinate.replace(' ','')
    return f"{coordinate} {clue[1]}: {clue[3]} ({clue[2]})"

def create_grid_string(grid):
    """Return a crossword grid as a string."""
    size = len(grid)
    separator = '  +' + ('-----+')*size
    column_number_line = '   '
    column_number_line += ''.join(f' {j:2}   ' for j in range(size))
    result = f'{column_number_line}\n{separator}\n'
    for (i, row) in enumerate(grid):
        fill = '  |'
        centre_line = f'{i:2}|'
        for entry in row:
            if entry == '#':
                fill += '#####|'
                centre_line += '#####|'
            else:
                fill += '     |'
                centre_line += f'  {entry}  |'
        result += f'{fill}\n{centre_line}\n{fill}\n{separator}\n'
    return result

def create_puzzle_string(grid, clues):
    """ Merges create_grid_string and create_clue_string 
        to output a more human-readable puzzle structure
    """
    gstring = create_grid_string(grid)
    cluestring = "\n"
    for i in range(len(clues)):
        cluestring += create_clue_string(clues[i])
        if i != len(clues) - 1:
            cluestring += '\n'
    return gstring + cluestring

def fill_in_word(grid, word, position, direction):
    """Create and return a new grid (a list of lists) based on the grid
    given in the arguments, but with the given word inserted according
    to position and direction.
        - direction: is either 'down' or 'across'.
        - position: the coordinates of the first letter of the word in the grid.
    *This function may modify its grid argument!*
    """
    x = position[0]
    y = position[1]
    if direction == 'across':
        for i in range(len(word)):
            grid[x][y + i] = word[i]
    else:
        for i in range(len(word)):
            grid[x + i][y] = word[i]
    return grid

def create_row_string(row):
    """Returns a row representation of a string.
    Example:
        create_row_string(['#', 'A', ' ']) returns '#A.'
    """
    rstring = ''.join(row)
    rstring = rstring.replace(' ', '.')
    return rstring

def write_puzzle(filename, grid, clues):
    """Writes the puzzle given by the grid and by the clues to the specified
    file.
    """
    size = len(grid)
    with open(filename, 'w') as file:
        file.write(f'SIZE {size}\n')
        for row in grid:
            file.write(f'ROW {create_row_string(row)}\n')
        for i in range(len(clues)):
            file.write(f'CLUE {create_clue_string(clues[i])}\n')

