#!/usr/bin/python3

import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!



'''
Regex matching technique:

the equivalent to a loop with two indices; one for the pattern, and one
for the input line.


start with both indices at zero.

Start with the pattern at index zero, then check if there is a match in 
the input line. If there is, then then go to the next pattern token, and
increment the input line index appropriately. If not, break and return 
false.

I need some sense of tokenization. I could do this by actually building a tokenizer, but I might be
better off doing it less formally.

Structure. Tokenizing both in advance isn't very efficient.



My current plan is to have main() poit to match_input(). match_input() will
iterate through both the pattern, and the input. For each iteration, it will analyze the current
pattern, find it's end, and pass the tokenized pattern, along with the correct number of characters
from the input, to the _pattern() function.


Problem: some patterns apply to the entire input...?
- Nope! [] only applies to the next character

Can token size be predicted in advance? Are all input tokens of legnth 1?
'''


def match(s, p):
    
    if p[0] == "^":
        return matchhere(s, p[1:])
    
    for i, c in enumerate(s):
        if (matchhere(s[i:], p)):
            return True

    return False


def matchhere(s, p):
    if len(p) == 0:
        return True
    elif len(s) == 0:
        '''Running out of pattern characters before the input is over
        is fine. Running out of input before the pattern is over is not
        '''
        return False
    elif p[0] == "[":
        group_end = p.find("]")#I should have a way to throw an error if it isn't found.
        if p[1] == "^":
            if s[0] not in p[2:group_end]:
                return matchhere(s[1:], p[group_end+1:])
        elif s[0] in p[1:group_end]:
            return matchhere(s[1:], p[group_end+1:])
        else:
            return False
    elif p[0] == "\\":
        if p[1] == "d":
            if s[0].isnumeric() is True:
                return matchhere(s[1:],p[2:])
            else:
                return False
        elif p[1] == "w":
            if (s[0].isnumeric() or s[0].isalpha() or s[0] == "_"):
                return matchhere(s[1:], p[2:])
    elif s[0] == p[0]:
        return matchhere(s[1:], p[1:])
    else:
        return False


def main():
    
    pattern = sys.argv[2]
    s = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)
    
    '''
    s = "log"
    pattern = "^log"'''
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match(s, pattern):
        print(s)
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
