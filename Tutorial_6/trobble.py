import random

class Trobble:
    """Trobbles: simplified digital pets.

    Data Attributes:
    name -- the Trobble's name.
    sex -- 'male' or 'female'.
    age -- a non-negative integer
    health -- an integer between 0 (dead) and 10 (full health) inclusive
    hunger -- a non-negative integer (0 is not hungry)
    """
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        self.age = 0
        self.health = 10
        self.hunger = 0
        self.breeding = 0
    
    def __str__(self):
        return f"{self.name}: {self.sex}, health {self.health}, hunger {self.hunger}, age {self.age}"
    
    def next_turn(self):
        """End the turn for the instance and recompute the attribute values
        for the next turn.
        """
        if self.health == 0:
            return

        self.age += 1
        self.hunger += self.age
        self.health = max( self.health - self.hunger // 20, 0)

        if self.age >= 4:
            self.breeding = random.randint(1,4)

    def feed(self):
        """Feed the Trobble instance to decrease the hunger by 25
        with a minimum value of 0.
        """
        self.hunger = max(self.hunger - 25, 0)

    def cure(self):
        self.health = min(10, self.health + 5)

    def have_fun(self):
        """Increase the health of the instance by 2 up to the maximum of 10 
        and increase the hunger by 4.
        """
        self.hunger += 4
        self.health = min(10, self.health + 2)

    def is_alive(self):
        """Return True if the health of the instance is positive,
        otherwise False.
        """
        if self.health <= 0:
            return False
        else:
            return True

def which_trobble():
    return input("What is the name of the Trobble? ")

def check_name(name, trobbles):
    if name in trobbles.keys():
        return True 
    return False

def print_state(trobbles):
    for i in trobbles.values():
        print(f"{i}, breeding {i.breeding}")

def increase_age(trobbles):
    for i in trobbles.values():
        i.next_turn()

def feed(trobbles):
    nameM = which_trobble()
    if check_name(nameM, trobbles):
        trobbles[nameM].feed()
    else:
        return "There is no such Trobble"
def have_fun(trobbles):
    nameM = which_trobble()
    if check_name(nameM, trobbles):
        trobbles[nameM].have_fun()
    else:
        return "There is no such Trobble"

def cure(trobbles):
    nameM = which_trobble()
    if check_name(nameM, trobbles):
        trobbles[nameM].cure()
    else:
        return "There is no such Trobble"

def breed(trobbles):
    nameM = ''
    nameF = ''
    while not check_name(nameM, trobbles):
        nameM = input('Name of the First Trobble in the breeding: ')
    while not check_name(nameF, trobbles):
        nameF = input('Name of the Second Trobble on the breeding: ')
    name_offspring = which_trobble()
    new_trobble = random_mate(trobbles[nameM], trobbles[nameF], name_offspring)
    if new_trobble != None:
        trobbles[name_offspring] = new_trobble
        return "A new trobble is born :)"
    else:
        return "No new trobble is born :("

def multi_play():
    nameM = input('Please give your new male Trobble a name: ')
    nameF = input('Please give your new female Trobble a name: ')
    trobbles = {}
    trobbles[nameM] = Trobble(nameM, 'male')
    trobbles[nameF] = Trobble(nameF, 'female')
    actions = {'feed': feed, 'cure': cure , 'have_fun': have_fun, 'increase_age': increase_age, 'breed': breed, 'print_state': print_state, 'stop_game': 'stop_game'}
    print(f'Your actions are {actions.keys()}')
    while True:
        action = input()
        if action == 'stop_game':
            break
        if action in actions:
            actions[action](trobbles)
    print('Thank you for playing')

def random_mate(trobble1, trobble2, name_offspring):
    """Check if the given Trobbles can procreate and if so give back a new
    Trobble that has the sex of trobble1 and the name 'name_offspring'.
    Otherwise, return None.

    For the random Trobbles to procreate it was discovered that the female has to have 
    its breeding likelyness to be exactly 3
    """
    if trobble1.age >= 4 and trobble2.age >=4:
        if trobble1.sex != trobble2.sex:
            if trobble1.is_alive() and trobble2.is_alive():
                if (trobble1.sex == 'female' and trobble1.breeding == 3) or (trobble2.sex == 'female' and trobble2.breeding == 3):
                    return Trobble(name_offspring, trobble1.sex)
    return None

def get_action(actions):
    while True:
        prompt = f"Type one of {', '.join(actions.keys())} to perform the action: "
        action_string = input(prompt)
        if action_string not in actions:
            print('Unknown action!')
        else:
            return actions[action_string]

def get_name():
    return input('Please give your new Trobble a name: ')

def get_sex():
    sex = None
    while sex is None:
        prompt = 'Is your new Trobble male or female? Type "m" or "f" to choose: '
        choice = input(prompt)
        if choice == 'm':
            sex = 'male'
        elif choice == 'f':
            sex = 'female'
    return sex
def play():
    name = get_name()
    sex = get_sex()
    trobble = Trobble(name, sex)
    actions = {'feed': trobble.feed, 'cure': trobble.cure, 'have_fun': trobble.have_fun}
    while trobble.is_alive():
        print('You have one Trobble named ' + str(trobble))
        action = get_action(actions)
        action()
        trobble.next_turn()
        if trobble.age % 10 == 0:
            print(f'Happy Birthday, {trobble.name}!')
            trobble.feed()
    print(f'Unfortunately, your Trobble {trobble.name} has died at the age of {trobble.age}')
    
def mate(trobble1, trobble2, name_offspring):
    """Check if the given Trobbles can procreate and if so give back a new
    Trobble that has the sex of trobble1 and the name 'name_offspring'.
    Otherwise, return None.
    """
    if trobble1.age >= 4 and trobble2.age >=4:
        if trobble1.sex != trobble2.sex:
            if trobble1.is_alive() and trobble2.is_alive():
                    return Trobble(name_offspring, trobble1.sex)
    return None
