#!/usr/bin/python3

import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!



'''
Regex matching technique:

the equivalent to a loop with two indices; one for the pattern, and one
for the input line.


start with both indices at zero.

Start with the pattern at index zero, then check if there is a match in the input line. If there is,
then then go to the next pattern token, and increment the input line index appropriately.
 If not, break and return false.

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



def parse_pattern(s, pattern):
    s_i = 0 #input counter
    pat_i = 0 #pattern counter

    '''
    Do we want to keep going until we reach the end of the input, or the
    end of the pattern?

    Pattern. By the end of the pattern, we will have a conclusive answer 
    as to whether or not the input matches.
    '''

    '''This covers three circumstances; the next pattern component is a:
    1) character category (preceeded by a backslash)
    2) character group (enclosed by [])
    3) literal character (no additional formatting)

    We iterate through the pattern, and check each token against the 
    appropriate text range (so far, one character) in the input. If 
    there is not a match, we return False. If there is, we continue
    checking. If we reach the end of the pattern, then the input
    matches, and we can return true.

    Maybe I should put each individual match into it's own function... 
    That will make future formatting changes easier
    '''


    '''Problem: Currently, this assumes that the pattern is anchored to
    the start, which is not a correct assumption

    I need a in-match and out-of-match differentiatior. If the match 
    starts 10 characters in, that's fine, but once it has started, it
    must be continuous. At least, I think that's the case...

    Maybe I need a match_started, and a match_completed. That way, if
    there is a substring at point A which is a partial match, and later
    there is a full match at point B, I won't trip over the match at A.

    Alternatively, on a False result, I could just reset the pattern
    counter to 0. My loop would depend on there both being more
    characters in the input, and the pattern. If the loop exits, and
    pat_i == len(pattern), then the match was completed. If however
    pat_i is less than len(pattern), then the match was incomplete


    '''
    
    while pat_i < len(pattern) and s_i < len(s):
        if pattern[pat_i] == "\\":
            if not match_pattern(s[s_i], pattern[pat_i:pat_i+2]):
                pat_i = 0
            else:
                pat_i += 2
        elif pattern[pat_i] == "[":
            group_end = pattern[pat_i:].find("]") + 1
            if not match_pattern(s[s_i], pattern[pat_i:group_end]):
                pat_i = 0;
            else:
                pat_i = group_end + 1
        else:
            if not match_pattern(s[s_i], pattern[pat_i]):
                pat_i = 0;
            else:
                pat_i +=1
            
        s_i += 1
            
    
    return pat_i >= len(pattern)
            





#def find_token_end(pattern, start_index):


def match_pattern(s, pattern):
    if len(pattern) == 1:
        return char_pattern(s, pattern) #Each pattern has a function, for consitency
    elif pattern == "\\d":
        return numeric_pattern(s, pattern)
    elif pattern == "\\w":
        return alphanumeric_pattern(s)
    elif pattern[0] == "[" and pattern[1] == "^" and pattern[-1] == "]":
        return negative_group_pattern(s, pattern)
    elif pattern[0] == "[" and pattern[-1] == "]": #is this a bad place for input validation?
        return positive_group_pattern(s, pattern)
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


def main():
    
    pattern = sys.argv[2]
    s = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)
    
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if parse_pattern(s, pattern):
        print(s)
        exit(0)
    else:
        exit(1)



def char_pattern(s, pattern):
    '''Returns True if s contains pattern
    '''
    return pattern in s


def numeric_pattern(s, pattern):
    '''Returns True if s contains any numbers
    '''
    return any(c.isnumeric() for c in s)       


def alphanumeric_pattern(s):
    '''Returns True if s contains numbers, letters, or _
    '''
    return any((c.isnumeric() or c.isalpha() or c == "_") 
        for c in s)

def positive_group_pattern(s, pattern):
    '''Returns True if s contains any characters from pattern
    '''
    pattern_set = set(pattern[1:-1])
    input_set = set(s)

    return not (pattern_set.isdisjoint(input_set))

def negative_group_pattern(s, pattern):
    '''Returns True if s contains no characters from pattern.
    '''
    pattern_set = set(pattern[2:-1])
    input_set = set(s)

    return pattern_set.isdisjoint(input_set)

if __name__ == "__main__":
    main()
