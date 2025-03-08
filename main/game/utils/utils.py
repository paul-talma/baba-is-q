def vec_add(self, v1, v2):
    """
        performs vector addition
    """
    return (v1[0] + v2[0], v1[1] + v2[1])


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

# misc
AND = "AND"


class AST:
    pass


class SyntaxObject(AST):
    def __init__(self, object_type):
        pass


class Verb(AST):
    def __init__(self, text: str):
        self.text = text


class Action(AST):
    def __init__(self, text: str):
        self.text = text


class ComplexObject(AST):
    def __init__(self, object_list: list[SyntaxObject]):
        self.object_list = object_list


class Rule(AST):
    def __init__(self, complex_object: SyntaxObject, verb: Verb, obj: SyntaxObject):
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
            tree: a syntax tree representing the structure of the text, or
                None if the text does not correspond to a valid rule
    """

    def __init__(self, text: list[str] = None):
        self.text: list[str] = text
        self.token: str = text[0]
        self.pos: int = 0
        self.len: int = len(text)

    def _parse(self, text: list[str]):
        self._rule()

    def _eat(self, token: str):
        if self.token == token:
            self.token = self._next_token()
        else:
            raise Exception()

    def _next_token(self):
        self.pos += 1
        if self.pos < self.len:
            return self.text[self.pos]
        return "EOF"

    def _rule(self):
        """
            RULE: complex_object verb object
                | complex_object IS action
        """
        complex_object = self._complex_object()
        verb = self._verb()
        obj = self._obj()
        return Rule(complex_object, verb, obj)

    def _complex_object(self):
        """
            complex_object: object (AND object)*
        """
        object_list: list[str] = []
        object_list.append(self._obj())

        while self.token == AND:
            self._eat(AND)
            object_list.append(self._obj())

        return ComplexObject(object_list)

    def _verb(self):
        """
            verb: IS
                | HAS
                | MAKE
        """
        token = self.token
        if token == IS:
            self._eat(token)
            return Verb(text=IS)
        if token == HAS:
            self._eat(token)
            return Verb(text=HAS)
        if token == MAKE:
            self._eat(token)
            return Verb(text=MAKE)

    def _obj(self):
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
        token = self.token
        self._eat(token)
        return SyntaxObject(token)
        # if token == BABA:
        #     self._eat(token)
        #     return SyntaxObject(BABA)
        #
        # if token == KEKE:
        #     self._eat(token)
        #     return SyntaxObject(KEKE)
        #
        # if token == WALL:
        #     self._eat(token)
        #     return SyntaxObject(WALL)
        #
        # if token == FLAG:
        #     self._eat(token)
        #     return SyntaxObject(FLAG)
        #
        # if token == ROCK:
        #     self._eat(token)
        #     return SyntaxObject(ROCK)
        #
        # if token == WATER:
        #     self._eat(token)
        #     return SyntaxObject(WATER)
        #
        # if token == KEY:
        #     self._eat(token)
        #     return SyntaxObject(KEY)
        #
        # if token == DOOR:
        #     self._eat(token)
        #     return SyntaxObject(token)

    def _action(self):
        token = self.token
        self._eat(token)
        return Action(token)



# want the parser to be created once, then have a method to feed it rule texts and parse these
# if rule text is invalid, return Null
# if rule text is valid, return ast for interpreter
# traverse the list
# keep track of what you're expecting
# if you get something you don't expect, abort
# if you get something you expect, update on what you expect next and add what you got to the tree
