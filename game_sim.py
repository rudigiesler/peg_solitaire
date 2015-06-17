from board import Board, BoardCache

# A smaller board for performance profiling
small_starting_board = [
    [None, 'X', 'X', 'X', None],
    ['X',  'X', 'X', 'X', 'X'],
    ['X',  'X', 'O', 'X', 'X'],
    ['X',  'X', 'X', 'X', 'X'],
    [None, 'X', 'X', 'X', None],
]

# The standard peg solitaire starting board, English version
starting_board = [
    [None, None, 'X', 'X', 'X', None, None],
    [None, None, 'X', 'X', 'X', None, None],
    ['X',  'X',  'X', 'X', 'X', 'X',  'X'],
    ['X',  'X',  'X', 'O', 'X', 'X',  'X'],
    ['X',  'X',  'X', 'X', 'X', 'X',  'X'],
    [None, None, 'X', 'X', 'X', None, None],
    [None, None, 'X', 'X', 'X', None, None],
]

# The weird peg solitaire starting board I found on the weekend away
other_starting_board = [
    [None, None, None, 'X', 'X', 'X', None, None, None],
    [None, None, None, 'X', 'X', 'X', None, None, None],
    [None, None, None, 'X', 'X', 'X', None, None, None],
    ['X',  'X',  'X',  'X', 'X', 'X', 'X',  'X',  'X'],
    ['X',  'X',  'X',  'X', 'O', 'X', 'X',  'X',  'X'],
    ['X',  'X',  'X',  'X', 'X', 'X', 'X',  'X',  'X'],
    [None, None, None, 'X', 'X', 'X', None, None, None],
    [None, None, None, 'X', 'X', 'X', None, None, None],
    [None, None, None, 'X', 'X', 'X', None, None, None],
]

# There are a lot of possible moves, but a lot less possible board states.
# If we keep a cache of all the board states we have visited, we don't
# need to revisit them, because we know where they lead, eliminating
# a lot of unnecessary calculation.
board = Board(starting_board)
board_cache = BoardCache([board])


# Depth first search because we only want to find one solution
def get_moves(board):
    if board.win:
        return board.history
    for move in board.moves:
        new_board = Board.from_board(board)
        new_board.move(*move)
        if new_board not in board_cache:
            solution = get_moves(new_board)
            if solution is not None:
                return solution
    return None

print get_moves(board)
