from os import wait
import sys
sys.setrecursionlimit(120)

def is_palindrome(word):
    """Check if input is a palindrome."""
    if len(word) <= 1:
        return True
    return word[0] == word[-1] and is_palindrome(word[1:-1])

def rec_pow(a, b):
    """Compute a**b recursively"""
    if b == 0:
        return 1
    if b == 1:
        return a
    return (rec_pow(a,b//2)**2) * (a if b % 2 else 1)

def binary_search(sorted_list, lower, upper, element):
    """Return the position of the element in the sublist of sorted_list
    starting at position lower up to (but excluding) position upper 
    if it appears there. Otherwise return -1.
    """
    if upper <= lower:
        return -1
    mid = (upper + lower)//2
    if sorted_list[mid] == element:
        return mid
    if sorted_list[mid] < element:
        return binary_search(sorted_list, mid+1 , upper, element)
    if sorted_list[mid] > element:
        return binary_search(sorted_list, lower, mid, element)

import random

def random_increasing_integer_sequence(length):
    """Return an increasing list of integers of the given length."""
    current = 0
    res = []
    for _ in range(length):
        current += random.randint(1, 10)
        res.append(current)
    return res

def pp_words():
    with open('sortedpp.txt') as file:
        return [w.strip() for w in file]

def read_positive_integer_custom(text, position):
    """Read a number starting from the given position, return it and the first
    position after it in a tuple. If there is no number at the given position
    then return None.
    """
    if position >= len(text) or (not text[position].isdigit()):
        return ("", position)

    t, pos = read_positive_integer_custom(text, position + 1)
    t = str(t) 
    t = text[position] + t
    return (int(t), pos)

def read_positive_integer(text, position):
    """Formats the output of read_positive_integer_custom"""
    t, pos = read_positive_integer_custom(text, position)
    if not t:
        return (int(t), pos)

def check_simple_expression(expression):
    if expression[0] != "(" or expression[-1] != ")":
        return False
    # save if there is a number, then a operation, then a number in this expression
    prev, sign, post = False, False, False
    for c in expression[1:-1]:
        if c.isdigit():
            if not sign:
                prev = True
            else:
                post = True
        elif (c == "+" or c == "-" or c == "*"):
            if sign == False:
                sign = True
            else:
                return False
        if (not c.isdigit()) and c != "+" and c != "-" and c != "*":
            return False

    return prev and post and sign 

def evaluate(expression, position):
    """Evaluate the expression starting from the given position.
    Return the value and the first position after the read
    sub-expression. If the string starting at the given expression
    is not an arithmetic expression, return None.
    """
    if expression[position].isdigit():
        return read_positive_integer_custom(expression, position)
    elif expression[position+1].isdigit():
        val, pos = evaluate(expression, position+1)
    else:
        qtd_open = 0
        for i in range(position+1, len(expression)):
            if expression[i] == '(':
                qtd_open += 1
            elif expression[i] == ')':
                qtd_open -= 1
            if qtd_open == 0:
                pos = position + i + 2
                val, _ = evaluate(expression, position+1)
                break
    sign = expression[pos]
    if sign == "+":
        return (val + evaluate(expression, pos+1)[0], len(expression))
    if sign == "-":
        return (val - evaluate(expression, pos+1)[0], len(expression))
    if sign == "*":
        return (val * evaluate(expression, pos+1)[0], len(expression))

