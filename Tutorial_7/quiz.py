def sorted_lines(filename):
    """Returns a list consisting of the lines of the file, sorted in alphabetical order."""
    with open(filename, 'r') as input_file:
        lines = input_file.readlines()
        return lines.sort()
