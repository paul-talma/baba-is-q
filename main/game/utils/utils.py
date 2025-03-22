def vec_add(v1: tuple[int, int], v2: tuple[int, int]):
    """
    performs vector addition
    """
    return (v1[0] + v2[0], v1[1] + v2[1])


#############
#   TYPES   #
#############
OBJECT = "OBJECT"
VERB = "VERB"
ACTION = "ACTION"
CONNECTIVE = "CONNECTIVE"


#############
#   TEXT    #
#############

# objects
WALL = "WALL"
ROCK = "ROCK"
BABA = "BABA"
KEKE = "KEKE"
FLAG = "FLAG"
WATER = "WATER"
KEY = "KEY"
DOOR = "DOOR"


# verbs
IS = "IS"
HAS = "HAS"
MAKE = "MAKE"

# actions
YOU = "YOU"
PUSH = "PUSH"
WIN = "WIN"

# connectives
AND = "AND"


class Token:
    def __init__(self, type: str, text: str) -> None:
        self.type = type
        self.text = text


class AST:
    pass


class TextObject(AST):
    pass


class Object(TextObject):
    def __init__(self, name) -> None:
        self.name = name


class Verb(TextObject):
    def __init__(self, verb: str) -> None:
        self.verb = verb


class Action(TextObject):
    def __init__(self, action: str) -> None:
        self.action = action


class ComplexObject(AST):
    def __init__(self, object_list: list[TextObject]) -> None:
        self.object_list = object_list


class Rule(AST):
    def __init__(self, complex_object: TextObject, verb: Verb, obj: TextObject) -> None:
        self.complex_object = complex_object
        self.verb = verb
        self.obj = obj


class Parser:
    """
    parses a text block into a rule

    the grammar of the language is specified by the following BNF:

    RULE: complex_object verb object
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

    complex_object: object (AND object)*


    note that the grammar for complex objects has been simplified to
        exclude adjectives or modifiers

    params:
        text_blocks: a list of strings corresponding to the text
            on contiguous text blocks

    returns:
            None if the text does not correspond to a valid rule
    """

    def __init__(self, tokens: list[Token]):
        """
        params:
            tokens: list of Token objects
        """
        self.tokens = tokens
        self.token: Token = tokens[0]
        self.pos: int = 0
        self.len: int = len(tokens)

    # TODO: does this need a param?
    def _parse(self, text: list[str]):
        self._rule()

    # TODO: graceful exit
    def _exit(self):
        pass

    def _eat(self, type: str):
        if self.token.type == type:
            tk = self._next_token()
            if tk:
                self.token = tk
            else:
                self._exit()
        else:
            # TODO: need to fail gracefully here
            self._exit()

    def _next_token(self):
        self.pos += 1
        if self.pos < self.len:
            return self.tokens[self.pos]
        return None

    def _rule(self) -> Rule:
        """
        RULE: complex_object verb object
            | complex_object IS action
        """
        complex_object = self._complex_object()
        verb = self._verb()
        obj = self._obj()
        if obj.text == ACTION and verb.verb != IS:
            self._exit()
        return Rule(complex_object, verb, obj)

    def _complex_object(self) -> ComplexObject:
        """
        complex_object: object (AND object)*
        """
        object_list: list[str] = []
        object_list.append(self._obj())

        while self.token == AND:
            self._eat(AND)
            object_list.append(self._obj())

        return ComplexObject(object_list)

    def _verb(self) -> Verb:
        """
        verb: IS
            | HAS
            | MAKE
        """
        tk = self.token
        self._eat(tk.type)
        return Verb(tk.text)

    def _obj(self) -> Object:
        """
        object: BABA
              | KEKE
              | WALL
              | FLAG
              | ROCK
              | WATER
              | KEY
              | DOOR
        """
        tk = self.token
        obj = Object(tk.text)
        self._eat(OBJECT)
        return obj

    def _action(self) -> Action:
        tk = self.token
        self._eat(tk.type)
        return Action(tk.text)


# want the parser to be created once, then have a method to feed it rule texts and parse these
# if rule text is invalid, return Null
# if rule text is valid, return ast for interpreter
# traverse the list
# keep track of what you're expecting
# if you get something you don't expect, abort
# if you get something you expect, update on what you expect next and add what you got to the tree
