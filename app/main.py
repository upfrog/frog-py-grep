#!/usr/bin/python3

import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!

def match(s, p):
    global groups
    
    if p[0] == "^":
        
        groups = []
        return matchhere(s, 0, p, 1)
    for i, c in enumerate(s):
         
        groups = []
        if (matchhere(s, i, p, 0)):
            return True

    return False

'''
How do I modify my capture groups?
- Degenerate form: check the end+1th character. If it is a special match... Write special code to
handle each
- Slightly less degenerate form. Write the end+1th check, and use it to set a max and/or a min number
of occurences for the capture group. Then pass those off to a loop, which basically contains your
current code.


What modification (? or +) situations do I need to handle?
- modification of a constant
- modification of a group?
- modification of a capture group


'''
def matchhere(s, si, p, pi):
    '''si is the current index in s, and pi is the current index in p
    '''

    global groups #THIS SEEMS REALLY BAD
    p_remainder = len(p) - (pi)
    s_remainder = len(s) - (si)
    try:
        p_val = p[pi]
        s_val = s[si]
    except:
        pass
    if p_remainder == 0:
        return True
    elif p_remainder > 1 and p[pi+1] == "+": #first check prevents out of bounds
        #Match one or more time
        if s[si] == p[pi]:
            
            matches = 1
            while (matches + si) < s_remainder and s[si+matches] == p[pi]:
                matches += 1
            return matchhere(s, si+matches, p, pi + 2)
        else:
            return check_exit(s, si, p, pi)
    elif p_remainder > 1 and p[pi + 1] == "?":
        #Match zero or 1 times
        if s_remainder == 0:
            return matchhere(s, si, p, pi + 2) #In case p still has more conditions
        elif s[si] == p[pi]:
                return matchhere(s, si + 1, p, pi + 2)
        else:
            return matchhere(s, si, p, pi+2)
    elif p[pi] == "[":
        group_end = p[pi:].find("]") + pi #I should have a way to throw an error if it isn't found.
        
        if len(p) > group_end + 1 and p[group_end + 1] == "+":
            #match the group for 1 or more times
            if p[pi+1] == "^":
                while si < len(s):
                    if s[si] not in p[pi+2:group_end]:
                        si += 1
                        #return matchhere(s, si, p, pi+group_end+1)
                    else:
                        return False
                    return True
            else:
                if s[si] not in p[pi+1:group_end]:
                    return False
                while s[si] in p[pi+1:group_end]:
                    si += 1

            return matchhere(s, si, p, group_end + 2)
        else:
            #Match the group once
            if p[pi+1] == "^":
                if s[si] not in p[pi+2:group_end]:
                    return matchhere(s, si, p, pi+group_end+1)
                else:
                    return False
            else:
                if s[si] not in p[pi+1:group_end]:
                    return False
                else:
                    return matchhere(s, si+1, p, group_end + 1)
    elif p[pi] == "\\":
        k = p[pi+1]
        if len(p) > pi + 2 and p[pi+2] == "+":
            if k == "d":
                #Match 1 or more digits
                if s[si].isnumeric() is True:
                    si += 1
                    while s[si].isnumeric() is True:
                        si += 1
                    return matchhere(s, si,p, pi+3)
                else:
                    return False
            elif k == "w":
                #Match an 1 or more alphanumeric characters
                if (s[si].isnumeric() or s[si].isalpha() or s[si] == "_"):
                    si += 1
                    while (s[si].isnumeric() or s[si].isalpha() or s[si] == "_"):
                        si += 1
                    return matchhere(s, si, p, pi+3)
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
                    while s[si: si + len(back_reference)] == back_reference:
                        si+= len(back_reference)
                    return matchhere(s, si + (end-begin) + 1, p, pi+2)
                else:
                    return False
                
        if len(p) > pi + 2 and p[pi+2] == "?":
            pass
        else:
            if k == "d":
                #Match a digit
                if s[si].isnumeric() is True:
                    return matchhere(s, si+1,p, pi+2)
                else:
                    return check_exit(s, si, p, pi+1)
            elif k == "w":
                #Match an alphanumeric character
                if (s[si].isnumeric() or s[si].isalpha() or s[si] == "_"):
                    return matchhere(s, si+1, p, pi+2)
            elif int(k) <= len(groups):
                #Match a backreference
                k = int(k) - 1
                begin = groups[k][0]
                end = groups[k][1]
                back_reference = s[begin : end]
                if s[si: si+(end-begin)] == back_reference:
                    #it's true! We can move on
                    return matchhere(s, si + (end-begin) + 1, p, pi+2)
            else:
                return check_exit(s, si, p, pi + 1)
    elif p[pi] == "$":
        #Anchor to the end of the string
        if s_remainder == 0:
            return True
        else:
            return check_exit(s, si, p, pi + 1)
    elif p[pi] == "(":
        groups.append([si])   
        choices = get_choices(p, pi+1)

        for elem in choices:
            if matchhere(s, si, p, elem):
                return True

        return False
    elif p[pi] == ")":
        i = len(groups) - 1

        while i >= 0 and len(groups[i]) != 1:
            i -= 1

        groups[i].append(si-1) 
        return matchhere(s, si, p, pi+1)
    elif p[pi] == "|":
        '''
        It doesn't matter how many additional optional terms there are, and how many groups
        deep they go. to be here, we must have matched the previous option, so we can
        ignore the future options. Therefor, we want to go straight to the end of the group        
        '''
        i = find_group_end(p, pi)
        return matchhere(s, si, p, i) #go to it, not past it; we want to document the group end
    elif s_remainder == 0:
        '''Running out of pattern characters before the input is over
        is fine. Running out of input before the pattern is over is not
        '''
        return False
    elif p[pi] == ".":
        '''So long as there is some character here, it's fine. Because
        this is after the check for remaining characters, it is
        guaranteed to pass.
        '''
        return matchhere(s, si+1, p, pi+1) 
    elif s[si] == p[pi]:
        return matchhere(s, si+1, p, pi+1)
    else:
        return check_exit(s, si, p, pi)


def get_choices(p, pi) -> list:
    '''
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
    '''
    pi should be the first character after the opening (
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


def check_exit(s, si, p, pi) -> bool:
    return False


def main():
    try:
        pattern = sys.argv[2]
        s = sys.stdin.read()

        if sys.argv[1] != "-E":
            print("Expected first argument to be '-E'")
            exit(1)


    except:

        s = "once a dreaaaamer, always a dreaaamer"
        pattern = "once a (drea+mer), alwaysz? a \\1"
        
        print("Logs from your program will appear here!")
        if match(s, pattern):
            print(s)
            exit(0)
        else:
            exit(1)
    else:
        print("Logs from your program will appear here!")
        if match(s, pattern):
            print(s)
            exit(0)
        else:
            exit(1)


    if match(s, pattern):
        print(s)
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()

