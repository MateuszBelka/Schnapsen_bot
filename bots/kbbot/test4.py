import sys
from kb import KB, Boolean, Integer, Constant

# Define our propositional symbols
# J1 is true if the card with index 1 is a jack, etc
# You need to initialise all variables that you need for you strategies and game knowledge.
# Add those variables here.. The following list is complete for the Play Jack strategy.
A0 = Boolean('a0')
J1 = Boolean('j1')
J2 = Boolean('j2')
J3 = Boolean('j3')
J4 = Boolean('j4')
A5 = Boolean('a5')
J6 = Boolean('j6')
J7 = Boolean('j7')
J8 = Boolean('j8')
J9 = Boolean('j9')
A10 = Boolean('a10')
J11 = Boolean('j11')
J12 = Boolean('j12')
J13 = Boolean('j13')
J14 = Boolean('j14')
A15 = Boolean('a15')
J16 = Boolean('j16')
J17 = Boolean('j17')
J18 = Boolean('j18')
J19 = Boolean('j19')
PA0 = Boolean('pa0')
PJ1 = Boolean('pj1')
PJ2 = Boolean('pj2')
PJ3 = Boolean('pj3')
PJ4 = Boolean('pj4')
PA5 = Boolean('pa5')
PJ6 = Boolean('pj6')
PJ7 = Boolean('pj7')
PJ8 = Boolean('pj8')
PJ9 = Boolean('pj9')
PA10 = Boolean('pa10')
PJ11 = Boolean('pj11')
PJ12 = Boolean('pj12')
PJ13 = Boolean('pj13')
PJ14 = Boolean('pj14')
PA15 = Boolean('pa15')
PJ16 = Boolean('pj16')
PJ17 = Boolean('pj17')
PJ18 = Boolean('pj18')
PJ19 = Boolean('pj19')

# Create a new knowledge base
kb = KB()

# GENERAL INFORMATION ABOUT THE CARDS
# This adds information which cards are Jacks
kb.add_clause(A0)
kb.add_clause(A5)
kb.add_clause(A10)
kb.add_clause(A15)
# Add here whatever is needed for your strategy.

# DEFINITION OF THE STRATEGY
# Add clauses (This list is sufficient for this strategy)
# PA is the strategy to play jacks first, so all we need to model is all x PA(x) <-> A(x),
# In other words that the PA strategy should play a card when it is a jack
kb.add_clause(~A0, PA0)
kb.add_clause(~A5, PA5)
kb.add_clause(~A10, PA10)
kb.add_clause(~A15, PA15)
kb.add_clause(~PA0, A0)
kb.add_clause(~PA5, A5)
kb.add_clause(~PA10, A10)
kb.add_clause(~PA15, A15)
# Add here other strategies

kb.add_clause(~PA0)
# print all models of the knowledge base
for model in kb.models():
    print(model)

# print out whether the KB is satisfiable (if there are no models, it is not satisfiable)
print(kb.satisfiable())
