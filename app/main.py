#!/usr/bin/python3

import sys

'''
This is a basic, not-very-performant regular expression engine.

It supports:
- Literal matches ("x")
- Matches with numeric and alphanumeric character classes ("\\d", "\\w")
- Custom positive and negative character groups ("[]", "[^])
- Start and end-of-line anchors  ("^", "$")
- Alternation  ("(A|B)")
- A wildcard (".")
- Matching one or more times ("+")
- Matching zero or one times  ("?")
- Backreferences ("\n")

It has not been exhastively tested; there are almost certainly some 
un-handled edge cases.

It is has now advanced to the beta phase. Some improvement I'd like to make:
- File input (right now it just functions on one line of input)
- More graceful rejection of ill-formed inputs
- More rigorous testing
- A more scaleable implementation of repetition markers such as "+" and "?"
- A finite repeition marker
- Refactor to avoid using a global list to store matched groups
- Consider refactoring most (all?) of the token-level matching into subfunctions


'''


def match(s, p) -> bool:
    global groups
    
    if p[0] == "^":
        groups = []
        return matchhere(s, 0, p, 1)
    for i, c in enumerate(s):
        groups = []
        if (matchhere(s, i, p, 0)):
            return True

    return False


def matchhere(s, si, p, pi):
    '''si is the current index in s, and pi is the current index in p
    '''
    global groups #Global variable - probably best to factor out
    
    #These make some of the future conditionals clearer
    p_remainder = len(p) - (pi)
    s_remainder = len(s) - (si)
    
    #These are purely to simplify using the debugger.
    try:
        p_val = p[pi]
        s_val = s[si]
    except:
        pass

    if p_remainder == 0:
        #If we have finished the pattern, then the match is succesfull
        return True
    elif p_remainder > 1 and p[pi + 1] == "+":
        #Match one or more time
        if s[si] == p[pi]:
            matches = 1
            while (matches + si) < s_remainder and s[si + matches] == p[pi]:
                matches += 1
            return matchhere(s, si + matches, p, pi + 2)
        else:
            return False
    elif p_remainder > 1 and p[pi + 1] == "?":
        #Match zero or one times
        if s_remainder == 0:
            return matchhere(s, si, p, pi + 2) #In case p still has more conditions
        elif s[si] == p[pi]:
                return matchhere(s, si + 1, p, pi + 2)
        else:
            return matchhere(s, si, p, pi + 2)
    elif p[pi] == "[":
        #Match the beginning of a character group
        group_end = p[pi : ].find("]") + pi #I should throw an error if it isn't found
        
        if len(p) > group_end + 1 and p[group_end + 1] == "+":
            #mMtch the group for 1 or more times
            if p[pi + 1] == "^":
                while si < len(s):
                    if s[si] not in p[pi + 2 : group_end]:
                        si += 1
                    else:
                        return False
                    return True
            else:
                if s[si] not in p[pi + 1 : group_end]:
                    return False
                while s[si] in p[pi + 1 : group_end]:
                    si += 1

            return matchhere(s, si, p, group_end + 2)
        elif len(p) > group_end + 1 and p[group_end + 1] == "?":
            #Match the group one or zero times - whether it matches or not, we continue!
            return matchhere(s, si, p, pi + group_end + 1)
        else:
            #Match the group once
            if p[pi+1] == "^":
                if s[si] not in p[pi + 2 : group_end]:
                    return matchhere(s, si, p, pi + group_end + 1)
                else:
                    return False
            else:
                if s[si] not in p[pi + 1 : group_end]:
                    return False
                else:
                    return matchhere(s, si + 1, p, group_end + 1)
    elif p[pi] == "\\":
        #Match one of the several tokens which start with a backslash
        k = p[pi + 1]
        if len(p) > pi + 2 and p[pi + 2] == "+":
            if k == "d":
                #Match 1 or more digits
                if s[si].isnumeric() is True:
                    si += 1
                    while s[si].isnumeric() is True:
                        si += 1
                    return matchhere(s, si, p, pi + 3)
                else:
                    return False
            elif k == "w":
                #Match an 1 or more alphanumeric characters
                if (s[si].isnumeric() or s[si].isalpha() or s[si] == "_"):
                    si += 1
                    while (s[si].isnumeric() or s[si].isalpha() or s[si] == "_"):
                        si += 1
                    return matchhere(s, si, p, pi + 3)
                else:
                    return False
            elif int(k) <= len(groups):
                #Match 1 or more backreferences
                k = int(k) - 1
                begin = groups[k][0]
                end = groups[k][1]
                back_reference = s[begin : end]

                if s[si: si+(end-begin)] == back_reference:
                    #it's true! We can move on
                    si += len(back_reference)
                    while s[si : si + len(back_reference)] == back_reference:
                        si+= len(back_reference)
                    return matchhere(s, si + (end-begin), p, pi + 2)
                else:
                    return False
        if len(p) > pi + 2 and p[pi + 2] == "?":
            pass
        else:
            if k == "d":
                #Match a digit
                if s[si].isnumeric() is True:
                    return matchhere(s, si + 1, p, pi + 2)
                else:
                    return False
            elif k == "w":
                #Match an alphanumeric character
                if (s[si].isnumeric() or s[si].isalpha() or s[si] == "_"):
                    return matchhere(s, si + 1, p, pi + 2)
            elif int(k) <= len(groups):
                #Match a backreference
                k = int(k) - 1
                begin = groups[k][0]
                end = groups[k][1]
                back_reference = s[begin : end]

                if s[si: si+(end-begin)] == back_reference:
                    #it's true! We can move on
                    return matchhere(s, si + (end-begin), p, pi + 2)
            else:
                return False
    elif p[pi] == "$":
        #Anchor to the end of the string
        if s_remainder == 0:
            return True
        else:
            return False
    elif p[pi] == "(":
        #Open a group, and record it's start
        groups.append([si])   
        choices = get_choices(p, pi + 1)

        for elem in choices:
            if matchhere(s, si, p, elem):
                return True

        return False
    elif p[pi] == ")":
        #Close a group, and record it's end.
        i = len(groups) - 1
        while i >= 0 and len(groups[i]) != 1:
            i -= 1
        groups[i].append(si) 
        return matchhere(s, si, p, pi + 1)
    elif p[pi] == "|":
        '''To be here, we must have matched at least one option, so we can ignore 
        any future options.
        '''
        i = find_group_end(p, pi)
        return matchhere(s, si, p, i) #go to it, not past it; we want to document the group end
    elif s_remainder == 0:
        '''Running out of pattern characters before the input is over
        is fine. Running out of input before the pattern is over is not.
        '''
        return False
    elif p[pi] == ".":
        '''So long as there is some character here, it's fine. Because
        this is after the check for remaining characters, it is
        guaranteed to pass.
        '''
        return matchhere(s, si + 1, p, pi + 1) 
    elif s[si] == p[pi]:
        return matchhere(s, si + 1, p, pi + 1)
    else:
        return False


def get_choices(p, pi) -> list:
    '''Finds all options (seperated by "|", if there is more than one) on a given
    group level.

    pi should be the first character after the opening (
    '''
    choices = [pi]
    paren_stack = []
    end = find_group_end(p, pi) #choices must be in *this* group

    while pi < end: 
        if p[pi] == "|" and len(paren_stack) == 0:
            choices.append(pi + 1)
        elif p[pi] == "(":
            paren_stack.append("(")
        elif p[pi] == ")":
            paren_stack.pop()

        pi += 1

    return choices


def find_group_end(p, pi) -> int:
    '''Finds the closing bracket of the current group level.

    pi should be the first character after the opening
    '''
    paren_stack = []

    while pi < len(p):
        if p[pi] == ")" and len(paren_stack) == 0:
            return pi
        elif p[pi] == ")" and len(paren_stack) != 0:
            paren_stack.pop()
        elif p[pi] == "(":
            paren_stack.append("(")
        pi += 1


def main():
    '''This is here to make manual testing easier. When run from the command line
    with 
    
    $ echo -n "<input>" | ./your_program.sh -E "<pattern>"

    it works as normal. When run directly, it will run on the manually inputted s and pattern
    '''
    try:
        pattern = sys.argv[2]
        s = sys.stdin.read()

        if sys.argv[1] != "-E":
            print("Expected first argument to be '-E'")
            exit(1)
    except:
        s = "YOUR STRING HERE"
        pattern = "YOUR PATTERN HERE"
        
        
    print("Results:")
    if match(s, pattern):
        print(s)
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()