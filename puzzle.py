from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Knight = Truth teller
# Knave = Lier

# Each person is either a knight or a knave. Not both at the same time.
my_knowledge = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave))
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    my_knowledge,
    Implication(AKnight, And(AKnight, AKnave)), # If A is saying the truth, then A is both a knight and a knave
    Implication(AKnave, Not(And(AKnight, AKnave))) # If A is a lier, then A is not both a knight and a knave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    my_knowledge,

    # A says "We are both knaves."
    Implication(AKnight, And(AKnave, BKnave)), # If A is saying the truth
    Implication(AKnave, Not(And(AKnave, BKnave))) # If A is a lier
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    my_knowledge,

    # A says "We are the same kind."
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), # If A is saying the truth
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))), # If A is a lier
                
    # B says "We are of different kinds."
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))), # If B is saying the truth
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))) # If B is a lier
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
