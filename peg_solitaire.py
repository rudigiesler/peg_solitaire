from copy import deepcopy


class Board(object):
    """Implements a game board for the peg solitaire game. Uses a square 2D
    list to represent the boards, with `None` for no holes, `O` for empty
    hold, and `X` for a hole with a peg."""

    def __init__(self, board):
        self.board = deepcopy(board)
        self.history = []
        self.hsh = self._generate_hash()

    def __getitem__(self, key):
        return self.board[key[0]][key[1]]

    def __setitem__(self, key, value):
        self.board[key[0]][key[1]] = value

    def _generate_hash(self):
        hsh = 0
        for i, row in enumerate(self.board):
            for j, val in enumerate(row):
                if val == 'X':
                    hsh += 2 ** (j + i*len(row))
        return hsh

    @classmethod
    def from_board(cls, board):
        """Creates a board by copying an existing board."""
        new_board = cls(board.board)
        new_board.history = deepcopy(board.history)
        new_board.hsh = board.hsh
        return new_board

    @property
    def moves(self):
        """ Returns a generater that gives all valid moves for the board, in
        (from, to) tuple pairs."""
        for i, row in enumerate(self.board):
            for j in range(0, len(row) - 3):
                sub = row[j:j+3]
                if sub == ['X', 'X', 'O']:
                    yield ((i, j), (i, j+2))
                if sub == ['O', 'X', 'X']:
                    yield ((i, j+2), (i, j))
        for j, col in enumerate(zip(*self.board)):
            for i in range(0, len(col) - 3):
                sub = col[i:i+3]
                if sub == ('X', 'X', 'O'):
                    yield ((i, j), (i+2, j))
                if sub == ('O', 'X', 'X'):
                    yield ((i+2, j), (i, j))

    def move(self, frm, to):
        """Performs a move on the board. For performance, doesn't validate if
        the move is correct."""
        self[frm] = 'O'
        self[to] = 'X'
        self[(frm[0] + to[0])/2, (frm[1] + to[1])/2] = 'O'
        self.history.append((frm, to))
        self.hsh = self._generate_hash()

    @property
    def win(self):
        """Win state is when there is only one marble left. Returns True if
        the board is in a win state, False if not."""
        return sum(i.count('X') for i in self.board) == 1

    def __eq__(self, other):
        return self.hsh == other.hsh  # Compare hashes for fast comporison

    def __ne__(self, other):
        return self.hsh != other.hsh  # Compare hashes for fast comporison

    def __str__(self):
        return '\n'.join(' '.join(i or ' ' for i in r) for r in self.board)


class BoardCache(object):
    def __init__(self, boards=[]):
        self.cache = []
        for board in boards:
            self.cache.append(board.hsh)

    def __contains__(self, key):
        if key.hsh not in self.cache:
            self.cache.append(key.hsh)
            return False
        return True
