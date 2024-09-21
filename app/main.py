#!/usr/bin/python3

import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!

def match(s, p):
    
    if p[0] == "^":
        return matchhere(s, 0, p, 1)
    for i, c in enumerate(s):
        global groups 
        groups = []
        if (matchhere(s, i, p, 0)):
            return True

    return False


def matchhere(s, si, p, pi):
    '''si is the current index in s, and pi is the current index in p
    '''
    p_remainder = len(p) - (pi)
    s_remainder = len(s) - (si)
    if p_remainder == 0:
        return True
    elif p_remainder > 1 and p[pi+1] == "+": #first check prevents out of bounds
        if s[si] == p[pi]:
            
            matches = 0
            while (matches + si) < s_remainder and s[matches+1] == p[pi]:
                matches += 1
            return matchhere(s, si+matches, p, pi + 2)
        else:
            return False
    elif p_remainder > 1 and p[pi + 1] == "?":
        if s_remainder == 0:
            return matchhere(s, si, p, pi + 2) #In case p still has more conditions
        elif s[si] == p[pi]:
                return matchhere(s, si + 1, p, pi + 2)
        else:
            return matchhere(s, si, p, pi+2)
    elif p[pi] == "[":
        group_end = p.find("]")#I should have a way to throw an error if it isn't found.
        if p[pi+1] == "^":
            if s[si] not in p[pi+2:group_end]:
                return matchhere(s, si, p, pi+group_end+1)
        elif s[si] in p[pi+1:group_end]:
            return matchhere(s, si+1, p, pi+group_end+1)
        else:
            return False
    elif p[pi] == "\\":
        if p[pi+1] == "d":
            if s[si].isnumeric() is True:
                return matchhere(s, si+1,p, pi+2)
            else:
                return False
        elif p[pi+1] == "w":
            if (s[si].isnumeric() or s[si].isalpha() or s[si] == "_"):
                return matchhere(s, si+1, p, pi+2)
    elif p[pi] == "$":
        if s_remainder == 0:
            return True
        else:
            return False
    elif p[0] == "(": #We have a group. Lets see what type it is.

        elems = []
        prev_devider = 0

        for i, c in enumerate(p):
            if c == "|":
                elems.append(p[prev_devider+1:i])
                prev_devider = i

        elems.append(p[prev_devider+1:-1])

        #Asking for forgiveness, not permission
        for elem in elems:
            try:
                if elem == s[0:len(elem)]:
                    return matchhere(s[len(elem)+1 : ], p[p.index(")")+1 : ])
            except: pass

        return False



        '''
        Okay. Would my planned modification actually help?

        The plan is to pass the entirety of s and p at all times, as well
        as indices for the two. I'll advance through the two strings as normal,
        but all my function calls will have more terms, which will be a bit annoying.

        But with that, at any given point I can check the current location in
        global context. Perhaps after every match I can iterate a global 
        highest-matched variable? When I get out of recursing on nested groups, I will know how
        far I went, which is really all I need; I can already make new additions
        to the grouplist to capture the correct order. The only problem is knowing how far
        into s a recursive subpath went, so that I know exactly what to influde
        in each match.

        '''







        #First we parse the top level of the group.
        #This is necesarry for... Reasons THAT I SHOULD CLARIFY AND SPECIFY
        #For one thing, a simple group (is that a good term?) should return false when it stops matching, but an optional one shouldn't... That's bad and dumb.

        elems = []
        prev_divider = 0
        paren_stack = []
        i = 0


        for i, char in enumerate(p):
            '''This divides the group into it it's elements, but only at
            the top level. It does not divide supgroubs, which is why 
            before we add anything to the list of elements, we first
            need to make sure that we are at the same level of 
            parenthesis as we started at.
            '''
            
            if char == "(":
                paren_stack.append(char)
            elif char == ")" and len(paren_stack) == 1 and paren_stack[0] == "(":
                elems.append(p[prev_divider+1 : i])
                break #We have reached the end of the group level
            elif char == ")" and paren_stack[-1] == "(" :
                paren_stack.pop()
            elif char == "|" and len(paren_stack) == 1:
                elems.append(p[prev_divider+1 : i])
                prev_divider = i
            
        for e in elems:
            if matchhere(s, e) == True: #match inwards
                #add to grouplist
                #then match outwards
                #Or do we just return true after adding to the list?



                #use the group list to check where the end of the currently parsed content is!
                return matchhere(s, p[i+1 : ])
                
            else:
                return False
        
        
        '''
        What is the problem? The problem, fundamentally, is that in order
        to advance as normal, I need to know how far to advance in my
        pattern, and my input string. But because I am breaking the chain
        of direct recursive descent, I don't have a way to do that. I
        parse some pattern e, but I have no way of knowing how far into
        s it goes!

        I need to build a way to track the final, matched result of groups. If
        I can do this, then I solve the above problem, because I just go to the
        end of the matched groups.

        Could I build them iteratively? No, there is no inherent way
        to distinguish a nested backreference group - which would need
        to include subsequent group(s) - from sequential ones, which would not

        Could I put all of s into the most recent capture group, then cut out parts I don't need??
        I get to a parenthesis


        Nooooo this won't work because it still relies on knowing how far I've gone..

        I think?

        I get to a parenthesis, and copy [here:end] into the last spot in
        my group list. Then I go through... Pretty much the same process I have here, except the if
        statement which is giving me so much trouble is just a plain old return. At the end of the 
        paren matching, I observe where I am now, search the last index
        of the grouplist until I find it, then cut out everything after.

        How do I observe where I am now? -_-

        Add 1 character to the end of every saved group. Let's say that "A" means
        the group has been terminated, and "B" means that it contains other groups.

        Then, when I'm modifying the second group, I go back and double check the previous one. 
        If it has a "B", then I copy the second group over to it.

        '''


        '''
        elems = []
        prev_devider = 0

        for i, c in enumerate(p):
            if c == "|":
                elems.append(p[prev_devider+1:i])
                prev_devider = i

        elems.append(p[prev_devider+1:-1])

        #Asking for forgiveness, not permission
        for elem in elems:
            try:
                if elem == s[0:len(elem)]:
                    return matchhere(s[len(elem)+1 : ], p[p.index(")")+1 : ])
            except: pass

        return False'''

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
        return False


def main():
    try:
        pattern = sys.argv[2]
        s = sys.stdin.read()

        if sys.argv[1] != "-E":
            print("Expected first argument to be '-E'")
            exit(1)
        print("Logs from your program will appear here!")


    except:
        print("Logs from your program will appear here!")

        s = "cat"
        pattern = ("ca?t")


        # Uncomment this block to pass the first stage
        if match(s, pattern):
            print(s)
            exit(0)
        else:
            exit(1)
    else:
        # Uncomment this block to pass the first stage
        if match(s, pattern):
            print(s)
            exit(0)
        else:
            exit(1)

if __name__ == "__main__":
    main()



















'''
        To do this, we ideally need to parse the entire group as one. 
        Groups should be able to nest arbitrarilly.

        At it's core, two groups with no divider should be &&, and a 
        divider should represent ||.

        New approach: Assess groups live instead of parsing first.

        Find the end of the first group. Check for equality. If NOT
        equal, then check the next character. If it's not |, then
        return false. If it is |, then repeat for the next one.

        That doesn't work! It fails at nested groups. Bad stuff!

        Lets trace this through

        catdogbatfoeneutral
        (cat (dog (bat|rat (friend|foe) ) neutral) #spaces for clarity

        Find open paren
        Enter group
        Check c - True
        Check a - True
        Check t - True
        Find open paren
        
        Enter group
        check d - True
        check o - True
        check g - True
        Find open paren

        Enter group
        check b - True
        check a - True
        check t - True
        find | - dimiss because this is already true (how do I do that in recursive descent!)
        search for next "(" or ")"
            - We know this works, because we MUST either close the current group, or 
            enter a new one
        find open paren

        Enter group
        check f - True
        check r - False
        oof! search for |
        Find |
        check f - True
        check o - True
        check e - True
        find close paren - return true. Should we? What if we come across a random open paren?

        Re-enter previous group
        The r

        
        Run more constrained matchhere()s? For example, given two options, run both, limited only to their scope. If option one is two characters, 
        pass those two characters of p, two characters of s, and nothing else.. No, no, no. Pass only the two characters of p, but pass all of s.
        That way, if there are any repetition characters, you can handle them. And running out of p but not s is fine. 

        So, we pass off two different version of p. If one is true, then we know that that this group is true. And I believe this will nest fine.

        This does break the "return matchhere()" shtick, to an extent. We But that's not a catastrophe. I don't even think it's the first time I've
        done it in this very project!


        Let's think about this a bit. You get to a parenthesis. So you know it's a group
        of some kind. But you don't know if it's a constant, or an option.



        


        Backtracking Groups:
        Have a global list of groups. Just append new ones, and they
        will appear in order... Or will they? Also, will I get weird
        issues with it being global? I should make a new one with call 
        of matchhere() from match(), right? I'll only be using it in
        matchhere(), but I will have many different recursive calls to
        that function, so life will.... Probably? be easier if I make it
        global. It's better than constantly passing it around the function
        calls, at least.



        The fundamental modification is that when I am exitting a group;
        that is, when I am in the code to process a group, and have 
        matched everything, and only need to end the code, instead of
        returning some sort of matchhere, I need to confirm that everything
        has matched, then add the group to the list, then return matchhere()

        ...

        That doesn't make much sense, does it?


        When I find an open paren, I should immediately add a place-holder
        to the grouplist. Make sure to save the index; you might add a dozen
        new groups before you get back to this! When I find the close 
        paren, I should add everything in s between the two parens to 
        to the grouplist.

        Problem: I need to be moving ranges of text from s, not ranges of p,
        so I need to keep track of what maps to the start of the range in s
        called out by p.


        -------------------------
        So you get all the elements of that group - which will either be a list of strings, seperated by |, (isn't there a function for that!?), or there
        are no seperators, or rather, there is an open paren before the next seperator. This means it's all one big T/F.
        In the second case, start iterating. Match characters literally, until you get to the next open paren. Then repeat this. 

        
        (hello(steve|tom))
        This has an ( before the next |, so when we enter, we treat it as a simple group. Advance and match char by char until we reach the second
        (, then repeat. This one does have a |, so parse the list.

        No, we need to parse a whole level at a time. A statement must know whether it's | or not before it enters the next statement.

        We enter a group. Then iterate through the group, keeping a stack of open/close parens. Add (, when we meet a ), pop.

        If we find |, and the stack is empty, then we add the entire term - ( to | - to the list of elements, then repeat.

        This will get us some number of high-level elements, each of which may have an arbitrary number of additional groups. We check each one for truth.
        
        Once we have established that a group matches, we add the text it matches to our grouplist

        Problem; how can a group know whether it should just return true, or return the next round of matchhere()?
            -This actually isn't a problem! Since groups will be processed as slices, after each close paren we can call matchhere() again, and get a True
            result to push up the call stack. When it goes sufficiently far up that there are still characters available after the close paren, the code
            will continue, and everything will be fine!

        (hello(Lord(Grantham|Hepsworth)|Lady(Flincher|Napier)))
        
        [  hello(Lord(Grantham|Hepsworth)|Lady(Flincher|Napier))  ]

        [  Lord(Grantham|Hepsworth)|Lady(Flincher|Napier)  ]

        [  Lord(Grantham|Hepsworth), Lady(Flincher|Napier)  ]

        [  Grantham, Hepsworth  ]

        [  Flincher, Napier  ]

        
        ((each)(of)(these)(must)(be)(matched))

        (each)(of)(these)(must)(be)(matched)

        My primary challenge was finding a good way to process groups so that they evaluated correctly, and backreferencing worked as intended.
        
        One big tradeoff was how to move data around the program. Recursive
        descent is really handy, until you need to move complex information up
        the chain. 
        '''
