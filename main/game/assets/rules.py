# constants
# types
OBJECT = "OBJECT"
VERB = "VERB"
ACTION = "ACTION"
CONNECTIVE = "CONNECTIVE"

# objects
WALL = "WALL"
ROCK = "ROCK"
BABA = "BABA"
KEKE = "KEKE"
FLAG = "FLAG"
DOOR = "DOOR"
KEY = "KEY"
WATER = "WATER"


# verbs
IS = "IS"
HAS = "HAS"
MAKE = "MAKE"

# actions
YOU = "YOU"
PUSH = "PUSH"
WIN = "WIN"
FLOAT = "FLOAT"
MELT = "MELT"
HOT = "HOT"
SINK = "SINK"

# connectives
AND = "AND"


class Token:
    def __init__(self, text: str, type: str) -> None:
        self.text = text
        self.type = type


# type dict
type = {
    WALL: OBJECT,
    ROCK: OBJECT,
    BABA: OBJECT,
    KEKE: OBJECT,
    FLAG: OBJECT,
    DOOR: OBJECT,
    KEY: OBJECT,
    WATER: OBJECT,
    IS: VERB,
    HAS: VERB,
    MAKE: VERB,
    YOU: ACTION,
    PUSH: ACTION,
    WIN: ACTION,
    FLOAT: ACTION,
    MELT: ACTION,
    HOT: ACTION,
    SINK: ACTION,
    AND: CONNECTIVE,
}


class Rule:
    def __init__(self, subject_list: list[str], verb: str, object: str) -> None:
        self.subject_list = subject_list
        self.verb = verb
        self.object = object


def parse_rule(symbols: list[str]) -> Rule | None:
    """
    parses a list of symbols into a rule, checking for typedness
    type checking is done by checking the type of the current symbol against
    the expected type, as given by the following BNF grammar:

        rule: complex_object verb object
            | complex_object IS action

        object: BABA
              | KEKE
              | WALL
              | FLAG
              | ROCK
              | WATER
              | KEY
              | DOOR

        verb: IS
            | HAS
            | MAKE

        action: PUSH
              | STOP
              | YOU
              | FLOAT
              | MELT
              | HOT
              | SINK

    params:
        symbols: a list of strings corresponding to adjacent text blocks

    returns:
        if symbols is a correctly typed string:
            a Rule object with the appropriate values for subjects, verb, and object
        else:
            None
    """
    length = len(symbols)
    subject_list = []
    curr_pointer = 0

    current_symbol = symbols[curr_pointer]
    # type check
    if type[current_symbol] != OBJECT:
        return

    subject_list.append(current_symbol)
    curr_pointer += 1

    while curr_pointer < length and symbols[curr_pointer] == AND:
        curr_pointer += 1
        # type check
        if type[current_symbol] != OBJECT:
            return
        subject_list.append(symbols[curr_pointer])
        curr_pointer += 1

    # type check
    if type[current_symbol] != VERB:
        return
    verb = symbols[curr_pointer]
    curr_pointer += 1

    # type check
    if type[current_symbol] != OBJECT and type[current_symbol] != ACTION:
        return
    object = symbols[curr_pointer]

    if _is_valid_rule(verb, object):
        return Rule(subject_list, verb, object)


def _is_valid_rule(verb: str, object: str) -> bool:
    if type[object] == ACTION and verb != IS:
        return False
    return True
