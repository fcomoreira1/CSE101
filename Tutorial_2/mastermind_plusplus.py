import random

COLORS = ['Odin', 'Thor', 'Freya', 'Skadi', 'Frigg', 'Heimdall', 'Loki']

def str_with_suffix(n):
    """Convert the integer n to a string expressing the corresponding 
    position in an ordered sequence.
    Eg. 1 becomes '1st', 2 becomes '2nd', etc.
    """
    if int(n) % 100 == 11:
        return str(n) + 'th'
    elif int(n) % 100 == 12:
        return str(n) + 'th'
    elif int(n) % 100 == 13:
        return str(n) + 'th'
    if int(n) % 10 == 1:
        return str(n) + 'st'
    elif int(n) % 10 == 2:
        return str(n) + 'nd'
    elif int(n) % 10 == 3:
        return str(n) + 'rd'
    else:
        return str(n) + 'th'

def input_color(color):
    """Return True if the given input color can be found in COLORS
       Use a for-loop to iterate over the list of COLORS.
    """
    for col in COLORS:
        if col == color:
            return True
    return False

def create_code():
    """Return 4-element list of strings randomly chosen from
    COLORS with repetition.
    """
    list = []
    for i in range(4):
        list.append(random.choice(COLORS))
    return list

def black_pins(guess, code):
    """guess, code: 4-element lists of strings from COLORS
    Returns the number of black pins, determined by the standard
    Mastermind rules
    """
    pins = 0
    for i in range(min(len(guess), len(code))):
        if guess[i] == code[i]:
            pins += 1

    return pins
    
def score_guess(guess, code):
    """guess, code: 4-element lists of strings
    Return (black, white) where
    black is the number of black pins (exact matches), and
    white is the number of white pins (correct colors in wrong places)
    """
    black = black_pins(guess, code)
    total = 0
    for color in COLORS:
        total += min(guess.count(color), code.count(color))
    return (black, total - black)

def input_guess(input_size):
    """Input four colors from COLORS and return as list.
    """
    print("Enter your guess: ")
    list = []
    for i in range(1,input_size + 1):
        num = str_with_suffix(i)
        print()
        color = check_input(num)
        list.append(color)
    return list

def check_input(num):
    while True:
        color = input(f"{num} color: ")
        quantity = 0
        final_color = color
        for col in COLORS:
            if col.startswith(color):
                quantity += 1
                final_color = col
        if quantity == 0:
            print(f"Please input a color from the list {COLORS}")
            print()
        elif quantity == 1:
            return final_color
        else:
            print("Please input an unambiguous prefix of a color from the list")
            print(COLORS)
            print()

        
def one_round(code):
    """Input guess, score guess, print result, and return True iff
    user has won.
    """
    guess = input_guess(len(code))
    score = score_guess(guess, code)
    print(f"Score: {score[0]} black, {score[1]} white")
    if score[0] == len(code) + 1:
        return True
    else:
        return False

def play_mastermind(code):
    """Let user guess the code in rounds, use a while-loop
    """
    i = 0
    while True:
        i += 1
        print()
        print(f"Round {i}")
        if one_round(code):
            break;
    print("You win!")
