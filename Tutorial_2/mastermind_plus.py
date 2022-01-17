import random

COLORS = ['RED', 'GREEN', 'BLUE', 'PURPLE', 'BROWN', 'YELLOW']

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

def input_guess():
    """Input four colors from COLORS and return as list.
    """
    print("Enter your guess: ")
    list = []
    for i in range(1,5):
        num = str_with_suffix(i)
        print()
        color = input(f"{num} color: ")
        while color not in COLORS:
            print(f"Please input a color from the list {COLORS}")
            print()
            color = input(f"{num} color: ")
        else:
            list.append(color)
    return list
        
def one_round(code):
    """Input guess, score guess, print result, and return True iff
    user has won.
    """
    guess = input_guess()
    score = score_guess(guess, code)
    print(f"Score: {score[0]} black, {score[1]} white")
    return score
def play_mastermind(code):
    """Let user guess the code in rounds, use a while-loop
    """
    i = 0
    while True:
        i += 1
        print(f"Round {i}")
        if one_round(code):
            break;
    print("You win!")

def all_codes():
    list = []
    for i1 in range(6):
        for i2 in range(6):
            for i3 in range(6):
                for i4 in range(6):
                    list.append([COLORS[i1],COLORS[i2],COLORS[i3],COLORS[i4]])
    return list

def test_guess(test_code, expected_score, guess):
    score = score_guess(guess, test_code)
    if expected_score == score:
        return True
    else:
        return False

def all_pins():
    list = []
    for i1 in range(4):
        for i2 in range(4):
            if i1 + i2 <= 4:
                list.append((i1, i2))
    return list
def autoplay_mastermind(code):
    all_possible = all_codes() 
    pins = all_pins()
    color1 = COLORS[0]
    color2 = COLORS[1]
    guess = [color1, color1, color2, color2]
    score = score_guess(guess, code)
    time = 0 
    print(guess)
    while score[0] != 4:
        time += 1
        copy_possible = all_possible.copy()
        for atry in copy_possible:
            if not test_guess(atry, score, guess):
                all_possible.remove(atry)

        minmax = [0, -1]
        for i in range(0, len(all_possible)):
            atry = all_possible[i]
            localMininum = 10000000000000
            for pin in pins:
                quantity = 0
                for guess in all_possible:
                    quantity += 1 - test_guess(atry, pin, guess)
                quantity = min(quantity, localMininum)
            if localMininum >= minmax[0]:
                minmax[0] = localMininum
                minmax[1] = i

        guess = all_possible[minmax[1]]
        score = score_guess(guess, code)
        print(guess)

    return time
