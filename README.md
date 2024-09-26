A basic implementation of grep in Python, originally built with guidance and test cases from Codecrafters.io

It supports:

    Literal matches ("x")
    Matches with numeric and alphanumeric character classes ("\d", "\w")
    Custom positive and negative character groups ("[]", "[^])
    Start and end-of-line anchors ("^", "$")
    Alternation ("(A|B)")
    A wildcard (".")
    Matching one or more times ("+")
    Matching zero or one times ("?")
    Backreferences ("\n")

It has not been exhastively tested; there are almost certainly some un-handled edge cases.

It is has now advanced to the beta phase. Some improvement I'd like to make:

    File input (right now it just functions on one line of input)
    More graceful rejection of ill-formed inputs
    More rigorous testing
    A more scaleable implementation of repetition markers such as "+" and "?"
    A finite repeition marker
    Refactor to avoid using a global list to store matched groups
    Consider refactoring most (all?) of the token-level matching into subfunctions
