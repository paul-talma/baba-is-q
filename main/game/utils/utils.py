def vec_add(v1, v2):
    """
    performs vector addition
    """
    return (v1[0] + v2[0], v1[1] + v2[1])


def render_board(board):
    for row in board.board:
        for tile in row:
            if len(tile) > 1:
                print('!', end='')
            elif tile:
                print(tile[0], end='')
            else:
                print(' ', end='')
        print('\n', end='')
