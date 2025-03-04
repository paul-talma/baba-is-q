import json
import utils.utils as utils

type Dir = tuple[int, int]
type Pos = tuple[int, int]

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
        self.pos: Pos
        self.is_push: bool
        self.is_stop: bool
        self.is_win: bool
        self.is_loss: bool


class Text(Object):
    def __init__(self, text: str):
        self.pushable: bool = True
        self.text: str = text
        self.is_win = False
        self.is_loss = False


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


class AST:
    pass


class Rule(AST):
    def __init__(self, complex_object, verb, object):
        self.complex_object = complex_object
        self.verb = verb
        self.object = object


class Board:
    def __init__(self, path):
        self.board: dict[int, dict[int, list[Object | None]]] = self._load_board(path)
        self.rules = self._get_rules()
        self.objects: list[Object] = []
        self.win_objects: list[Object] = []
        self.loss_objects: list[Object] = []
        self.you_pos: Pos
        self.you_objects: list[Object]
        self.n_rows: int = len(self.board)
        self.n_cols: int = len(self.board[0])

    def _load_board(self, path: str):
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

    def _get_objects(self, pos: Pos):
        """
            returns a list of all objects at a board pos
        """
        return self.board[pos[0]][pos[1]]

    def _has_text(self, pos: Pos):
        """
            checks whether board[pos] contains a text block
        """
        return any([isinstance(ob, Text) for ob in self._get_objects(pos)])

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

    def _get_text_blocks(self, pos: Pos, dir: Dir):
        """
            scans along dir for text blocks

            params:
                pos: board position
                dir: search direction

            returns:
                text: list of text strings encountered
        """
        # TODO: handle multiple text objects in same block
        text_blocks = []
        while self._in_bounds(pos) and self._has_text(pos):
            for ob in self._get_objects(pos):
                if isinstance(ob, Text):
                    text_blocks.append(ob.text)
            pos = utils.vec_add(pos, dir)
        return text_blocks

    def _in_bounds(self, pos: Pos):
        """
            returns True iff pos is in the bounds of the board
        """
        return 0 < pos[0] < self.n_rows and 0 < pos[1] < self.n_cols

    def _parse_rule(self, text_blocks):
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
        pass

    def _update_board(self, dir: Dir):
        """
            updates the position of each YOU object
        """
        for you in self.you_objects:
            if self._can_move(you, dir):
                self._update_posisition(you, dir)

    def _can_move(self, object: Object, dir: Dir):
        """
            returns true if object can move in direction dir
        """
        curr_pos = object.pos
        next_pos = utils.vec_add(curr_pos, dir)

        if not self._in_bounds(next_pos):
            return False

        for obj in self._get_objects(next_pos):
            if obj.is_stop:
                return False

            if obj.is_push and not self._can_move(obj, dir):
                return False

        return True

    def _update_posisition(self, curr_pos: Pos, dir: Dir):
        next_pos = utils.vec_add(curr_pos, dir)
        next_objects = self._get_objects(next_pos)

        if all([not o.is_push for o in next_objects]):
            self._move_tile(curr_pos, next_pos)
            return

        self._update_posisition(next_pos, dir)
        self._move_tile(curr_pos, next_pos)

    # TODO: Pick up here
    def _move_tile(self, curr_pos: Pos, dir: Dir):
        curr_objects = self._get_objects(curr_pos)

        you_indices = []
        for id, object in enumerate(curr_objects):
            if object.is_you:
                pass

    def update(self, input):
        pass
