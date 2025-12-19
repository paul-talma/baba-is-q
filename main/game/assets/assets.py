import json

import main.game.utils.rules as rls


import main.game.utils.utils as utils

type Dir = tuple[int, int]
type Pos = tuple[int, int]

# directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRS = [UP, DOWN, LEFT, RIGHT]

# text
WALL = 'WALL'
ROCK = 'ROCK'
BABA = 'BABA'
WIN = 'WIN'
PUSH = 'PUSH'
IS = 'IS'
YOU = 'YOU'
FLAG = 'FLAG'
WATER = 'WATER'
KEY = 'KEY'


class Object:
    def __init__(self):
        self.pos: Pos
        self.is_push: bool
        self.is_stop: bool
        self.is_win: bool
        self.is_loss: bool


class Text(Object):
    def __init__(self, text: str):
        self.text: str = text
        self.pushable: bool = True
        self.is_win = False
        self.is_loss = False

    def __str__(self):
        return self.text[0]


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
        """
        main game state

        board is loaded from the given path.

        class attributes:
            rules: currently active rules
            objects: existing objects
            win_objects: objects with property WIN
            loss_objects: objects with property DEFEAT
            you_pos: location of YOU objects
            you_objects: list of YOU objects
        """
        self.board: list[list[list[Object]]] = self._load_board(path)
        self.rules = self._get_rules()
        self.objects: list[Object] = []
        self.win_objects: list[Object] = []
        self.loss_objects: list[Object] = []
        self.you_pos: list[Pos]
        self.you_objects: list[Object]
        self.n_rows: int = len(self.board)
        self.n_cols: int = len(self.board[0])

    def _load_board(self, path: str) -> list[list[list[Object]]]:
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
            with open(path, 'r') as file:
                board = json.load(file)

        except FileNotFoundError as e:
            print(f'Error: file not found: {e}')

        except json.JSONDecodeError as e:
            print(f'Error: the file contains invalid jason: {e}')

        # TODO: need to process tile contents into Objects
        return board

    def _get_objects(self, pos: Pos) -> list[Object]:
        """
        returns a list of all objects at a board pos
        """
        return self.board[pos[0]][pos[1]]

    def _has_text(self, pos: Pos) -> bool:
        """
        checks whether board[pos] contains a text block
        """
        return any([isinstance(ob, Text) for ob in self._get_objects(pos)])

    def _get_rules(self) -> list[rls.Rule]:
        """
        iterate through board looking for rules

        returns:
            rules: a list of currently active rules
        """
        rules: list[rls.Rule] = []
        for row_id, row in enumerate(self.board):
            for col_id, tile in enumerate(row):
                for ob in tile:
                    # if tile contains a text object, scan for rules
                    if isinstance(ob, Text):
                        symbol_strings = []

                        # retrieve text blocks in both directions
                        for dir in [RIGHT, DOWN]:
                            symbol_strings.extend(
                                self._get_text_blocks((row_id, col_id), dir)
                            )

                        # parse text sequences of text blocks into rules
                        new_rules = [
                            rls.parse_rule(rule_text) for rule_text in symbol_strings
                        ]
                        new_rules = [rule for rule in new_rules if rule is not None]

                        rules.extend(new_rules)
        return rules

    def _get_text_blocks(self, pos: Pos, dir: Dir) -> list[str]:
        """
        scans along dir for text blocks until board edges or cell with
        no text is encountered

        params:
            pos: board position
            dir: search direction

        returns:
            text: list of text strings encountered
        """
        # TODO: handle multiple text objects in same block
        # is this even possible?
        text_blocks = []
        while self._in_bounds(pos) and self._has_text(pos):
            for ob in self._get_objects(pos):
                if isinstance(ob, Text):
                    text_blocks.append(ob.text)
            pos = utils.vec_add(pos, dir)
        return text_blocks

    def _in_bounds(self, pos: Pos) -> bool:
        """
        returns True iff pos is in the bounds of the board
        """
        return 0 < pos[0] < self.n_rows and 0 < pos[1] < self.n_cols

    def _process_movements(self, dir: Dir) -> None:
        """
        updates the position of each YOU object, as well as any other
        objects thereby displaced
        """
        for you in self.you_objects:
            if self._can_move(you, dir):
                self._move(you, dir)

    def _can_move(self, ob: Object, dir: Dir) -> bool:
        """
        returns true if object can move in direction dir
        returns False if:
            object is at edge of map
            next_pos contains a STOP object
            next_pos contains a PUSH object that recursively can't move
        and True otherwise
        """
        curr_pos = ob.pos
        next_pos = utils.vec_add(curr_pos, dir)

        if not self._in_bounds(next_pos):
            return False

        for obj in self._get_objects(next_pos):
            if obj.is_stop:
                return False

            if obj.is_push and not self._can_move(obj, dir):
                return False

        return True

    def _move(self, ob: Object, dir: Dir) -> None:
        """
        update position of object ob in direction dir
        it is assumed that ob _can_move in dir

        if next tile contains no obstacle, shift object over
        if it does, recursively move them, then move ob
        """
        curr_pos = ob.pos
        next_pos = utils.vec_add(curr_pos, dir)
        next_objects = self._get_objects(next_pos)

        # BUG: doesn't work if next tile contains multiple push objects
        # (will move one object two blocks)
        for o in next_objects:
            if o.is_push:
                self._move(o, dir)
        self._shift_object(ob, dir)

    def _shift_object(self, ob: Object, dir: Dir) -> None:
        """
        move object ob from current state to next state
        """
        curr_pos = ob.pos
        next_pos = utils.vec_add(curr_pos, dir)

        # update board
        self.board[curr_pos[0]][curr_pos[1]].remove(ob)
        self.board[next_pos[0]][next_pos[1]].append(ob)

        # update object
        ob.pos = next_pos
