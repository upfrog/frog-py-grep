#!/usr/bin/python3

import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return char_pattern(input_line, pattern) #Each pattern has a function, for consitency
    elif pattern == "\\d":
        return numeric_pattern(input_line, pattern)
    elif pattern == "\\w":
        return alphanumeric_pattern(input_line)
    elif pattern[0] == "[" and pattern[1] == "^" and pattern[-1] == "]":
        return negative_group_pattern(input_line, pattern)
    elif pattern[0] == "[" and pattern[-1] == "]": #is this a bad place for input validation?
        return positive_group_pattern(input_line, pattern)
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        print(input_line)
        exit(0)
    else:
        exit(1)



def char_pattern(input_line, pattern):
    '''Returns true if input_line contains pattern
    '''
    return pattern in input_line


def numeric_pattern(input_line, pattern):
    '''Returns true if input_line contains any numbers
    '''
    return any(c.isnumeric() for c in input_line)       


def alphanumeric_pattern(input_line):
    '''Returns true if input_line contains numbers, letters, or _
    '''
    return any((c.isnumeric() or c.isalpha() or c == "_") 
        for c in input_line)

def positive_group_pattern(input_line, pattern):
    '''Returns true if input_line contains any characters from pattern
    '''

    pattern_set = set(pattern[1:-1])
    input_set = set(input_line)

    return not (pattern_set.isdisjoint(input_set))

def negative_group_pattern(input_line, pattern):
    pattern_set = set(pattern[2:-1])
    input_set = set(input_line)

    return pattern_set.isdisjoint(input_set)

if __name__ == "__main__":
    main()
