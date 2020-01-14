import sys
from kb import KB, Boolean, Integer, Constant

exercise = 5

if exercise == 0:
    # Define our symbols
    A = Boolean('A')
    B = Boolean('B')
    C = Boolean('C')

    # Create a new knowledge base
    kb = KB()

    # Add clauses
    kb.add_clause(A, B, C)
    kb.add_clause(~A, B)
    kb.add_clause(~B, C)
    kb.add_clause(B, ~C)
    kb.add_clause(~B, ~C) # My clause

    # Print all models of the knowledge base
    for model in kb.models():
        print(model)

    # Print out whether the KB is satisfiable (if there are no models, it is not satisfiable)
    print(kb.satisfiable())
elif exercise == 3:
    # Define our symbols
    A = Boolean('A')
    B = Boolean('B')
    C = Boolean('C')
    D = Boolean('D')

    # Create a new knowledge base
    kb = KB()

    kb.add_clause(A, B)
    kb.add_clause(~B, A)
    kb.add_clause(~A, C)
    kb.add_clause(~A, D)
    kb.add_clause(~A) # Ex 4
    kb.add_clause(~C) # Ex 4
    kb.add_clause(~D) # Ex 4

    # Print all models of the knowledge base
    for model in kb.models():
        print(model)

    # Print out whether the KB is satisfiable (if there are no models, it is not satisfiable)
    print(kb.satisfiable())
elif exercise == 5:
    # Define our symbols
    P = Boolean('P')
    Q = Boolean('Q')
    R = Boolean('R')

    # Create a new knowledge base
    kb = KB()

    # Add clauses
    kb.add_clause(P,Q)
    kb.add_clause(~Q,R)
    kb.add_clause(~R,~P)
    # ~P v ~Q ^ Q v P
    kb.add_clause(~P,~Q) # entailed by
    kb.add_clause(P,Q) # entailed by
    # P v Q ^ Q v ~P
    kb.add_clause(P,Q) # check unsatisfiability
    kb.add_clause(~P,Q) # check unsatisfiability

    # Print all models of the knowledge base
    for model in kb.models():
        print(model)

    # Print out whether the KB is satisfiable (if there are no models, it is not satisfiable)
    print(kb.satisfiable())
