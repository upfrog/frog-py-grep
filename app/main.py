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


'''

The fundamental problem is that whatever I do to handle backwards movement,
it must be done in each of my cases, and by different amounts.
Ways to handle backwards movement:
    - Have a seperate function which iterates indices
    - Pass a third parameter into matchhere, which indicates whether to move back or forward
    - Combine the two above. Whenever it's time to increment an index, pass it off
    to a dedicated increment() function, which takes the direction indicator,
    the strings, and the size of the movement, and returns the correct strings
        - This has the added advantage of helping clean up matchhere()
    -Make a seperate block of code, identical to matchhere(), except 
    that it goes backwards
        - This will keep the individual matching functions simpler
    - Re-write my code so that it passes the input string, the pattern, 
    and the index to start on, rather than passing slices of the input
    and the pattern. Then add checks to each of my increment statement,
    to determine which direction to increment towards
        - I think this will be helpful when I need to start integrating
        matches for 0 or more instances of a character
        - The downside is that this will clog up my code


    - Is this all over-complicated? I can just pass a number as well;
    either -1 or +1. Multiply all increments by this amount.
        - This requires that all increments are symmetric... I don't think
        it will be enough, since I'm regularly passing string slices around,
        and the structure of those slices will need to change. Still,
        this was a good idea. Good job for thinking of it.


    This is all silly! I don't need to reverse this! I can just match as 
    normal, and if the last character of the pattern isn't the last in
    the string, I return false.

    Problem; does this work if there are multiple occurences of the
    pattern, only one of which is at the end?

    We can limit our negatory to once we are at the end...?

    This should work, actually! Since the overall loop is handled in
    match(), it can notice that we have reached the end in the context
    of the rest of the string

    ... That description doesn't make very much sense.

'''


def matchhere(s, p):
    if len(p) == 0:
        return True
    elif len(p) > 1 and p[1] == "+": #first check prevents out of bounds
        if s[0] == p[0]:
            s_i = 1
            while s_i < len(s) and s[s_i] == p[0]:
                s_i += 1
            return matchhere(s[s_i:], p[2:])
        else:
            return False


    #NOT WORKING - debug and see whats up!
    elif len(p) > 1 and p[1] == "?":
        if len(s) == 0:
            return matchhere(s, p[2:]) #In case p still has more conditions
        elif s[0] == p[0]:
                return matchhere(s[1:], p[2:])
        
                '''
                For if I do need to avoid repeated characters
                if len(s) > 0 and s[1] == p[0]: #I don't know if this is a case I care about or not... must it match no more than one time?
                return False
                else:
                '''
        else:
            return matchhere(s, p[2:])
            

        '''
        What are the possible conditions here?
        1) There are zero instances of the character
        2) there is one isntance of the character
        3) there is more than one instance of the character
        4) There are no more characters at all
        
        '''

        '''
        if len(s) == 1 and s[0] == p[0]:
            return True
        if len(s) > 1 and s[1] != p[0]:
            s_increment = 0
            if s[0] == [0]:
                s_increment = 1
            
            return matchhere(s[s_increment:], p[2:])
        else:
            return False'''


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
    elif p[0] == "$":
        if len(s) == 0:
            return True
        else:
            return False 
   

    
    elif len(s) == 0:
        '''Running out of pattern characters before the input is over
        is fine. Running out of input before the pattern is over is not
        '''
        return False
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
    s = "dogs"
    pattern = "dogs?"'''

    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match(s, pattern):
        print(s)
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
