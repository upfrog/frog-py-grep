#!/usr/bin/python3

import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!

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
    elif len(p) > 1 and p[1] == "+": #first check prevents out of bounds
        if s[0] == p[0]:
            s_i = 1
            while s_i < len(s) and s[s_i] == p[0]:
                s_i += 1
            return matchhere(s[s_i:], p[2:])
        else:
            return False
    elif len(p) > 1 and p[1] == "?":
        if len(s) == 0:
            return matchhere(s, p[2:]) #In case p still has more conditions
        elif s[0] == p[0]:
                return matchhere(s[1:], p[2:])
        else:
            return matchhere(s, p[2:])
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
    elif p[0] == "(":
        '''This needs to be cleaned up a bit. In particular:
            - I am not convinced I actually need the try-except clauses,
            since the indices are already guaranteed to be in p
            - Somewhere along the way, I think I lost the "improperly
            formed input" exception code. I should put that back in, 
            and develop a consistent way of integrating input validation
            with the rest of the code.
            - This code is just.... Ugly. It's ugly and unclear.
            - Try to expand this to handle arbitrary numbers of groups.
        '''
        group_end = p.find(")")
        divider = p.find("|")
        if divider == -1 or group_end == -1: 
            exit(1)

        try:
            e1 = p[1:divider]
        except:
            return False

        if s[0:len(e1)] == e1:
            return matchhere(s[len(e1):], p[group_end+1:])
        
        try:
            e2 = p[divider+1:group_end]
        except:
            return False
        
        if s[0:len(e2)] == e2:
            return matchhere(s[len(e2):], p[group_end+1:])
        
        return False
        
    elif len(s) == 0:
        '''Running out of pattern characters before the input is over
        is fine. Running out of input before the pattern is over is not
        '''
        return False
    elif p[0] == ".":
        '''So long as there is some character here, it's fine. Because
        this is after the check for remaining characters, it is
        guaranteed to pass.
        '''
        return matchhere(s[1:], p[1:]) 
    
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
    s = "cat"
    pattern = ("(bat|caf)")'''

    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match(s, pattern):
        print(s)
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
