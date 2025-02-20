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
                    if isinstance(ob, Text):
                        rule_texts = []
                        for dir in [RIGHT, DOWN]:
                            rule_texts.extend(self._get_text_blocks(ob, (row, tile), dir))
                        new_rules = [self._parse_rule(rule_text) for rule_text in rule_texts]
                        rules.extend(new_rules)

    def _get_text_blocks(self, pos, dir):
        """
            recursively checks for text blocks along a given direction

            params:
                ob: text object of the current tile
                pos: current position of search
                dir: direction of current search

            returns:
                rule text: a list of contiguous text tokens
        """
        if not self._in_bounds(pos):
            return []

        text = []
        for ob in self.board[pos[0]][pos[1]]:
            if isinstance(ob, Text):
                text.append(ob.text)
                next_pos = self._vec_add(pos, dir)
                text.extend(self._get_text_blocks(next_pos, dir))
        return text

    def _in_bounds(self, pos):
        return 0 < pos[0] < self.n_rows and 0 < pos[1] < self.n_cols

    def _vec_add(self, v1, v2):
        return (v1[0] + v2[0], v1[1] + v2[1])

    def _parse_rule(self, rule):
        pass

    def update(self, input):
        pass
