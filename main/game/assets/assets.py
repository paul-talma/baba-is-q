import json


# directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRS = [UP, DOWN, LEFT, RIGHT]

# text
WALL = "WALL"
ROCK = "ROCK"
BABA = "BABA"
WIN = "WIN"
PUSH = "PUSH"
IS = "IS"
YOU = "YOU"
FLAG = "FLAG"
WATER = "WATER"
KEY = "KEY"


class Object:
    def __init__(self):
        self.pushable: bool
        self.x: int
        self.y: int


class Text(Object):
    def __init__(self, text: str):
        self.pushable = True
        self.text = text


class Wall(Object):
    def __init__(self):
        pass


class Baba(Object):
    def __init__(self):
        pass


class Flag(Object):
    def __init__(self):
        pass


class Key(Object):
    def __init__(self):
        pass


class Board:
    def __init__(self, path):
        self.board = self._load_board(path)
        self.rules = self._get_rules()

    def _load_board(self, path):
        """
            reads the initial state of the board from a .json file
            and stores it in a dictionary.

            params:
                path: string, path to a .json file of the level

            returns:
                board: dict of dicts with row and col indices as keys and lists
                    of objects as values
        """
        try:
            with open(path, "r") as file:
                board = json.load(file)

        except FileNotFoundError:
            print("Error: file not found: {e}")

        except json.JSONDecodeError:
            print("Error: the file contains invalid jason: {e}")

        return board

    def _has_text(self, pos):
        """
            checks whether board[pos] contains a text block
        """
        return any([isinstance(ob, Text) for ob in self.board[pos[0]][pos[1]]])

    def _get_rules(self):
        """
            iterate through board looking for rules

            returns:
                rules: a list of currently active rules
        """
        rules = []
        for row in self.board:
            for tile in row:
                for ob in tile:
                    if self._is_text(ob):
                        rule_texts = []
                        for dir in [RIGHT, DOWN]:
                            rule_texts.extend(self._get_text_blocks(ob, (row, tile), dir))
                        new_rules = [self._parse_rule(rule_text) for rule_text in rule_texts]
                        rules.extend(new_rules)

    def _get_text_blocks(self, pos, dir):
        """
            scans along dir for text blocks

            params:
                pos: board position
                dir: search direction

            returns:
                text: list of text strings encountered
        """
        # TODO: handle multiple text objects in same block
        text = []
        while self._in_bounds(pos) and self._has_text(pos):
            for ob in self.board[pos[0]][pos[1]]:
                if isinstance(ob, Text):
                    text.append(ob.text)
            pos = self._vec_add(pos, dir)
        return text

    def _in_bounds(self, pos):
        """
            returns True iff pos is in the bounds of the board
        """
        return 0 < pos[0] < self.n_rows and 0 < pos[1] < self.n_cols

    def _vec_add(self, v1, v2):
        """
            performs vector addition
        """
        return (v1[0] + v2[0], v1[1] + v2[1])

    def _parse_rule(self, text_blocks):
        """
            parses a text block into a rule

            the grammar of the language is specified by the following BNF:

            S: complex_object verb object
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


            note that the grammar for complex objects has been simplified to not
                include adjectives or modifiers

            params:
                text_blocks: a list of strings corresponding to the text
                    on contiguous text blocks

            returns:
                tree: a syntax tree representing the structure of the text, or
                    None if the text does not correspond to a valid rule
        """
        pass

    def update(self, input):
        pass
