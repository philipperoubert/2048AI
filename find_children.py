from board import Board


def find_children(board, is_initial=False):
    """
    Find children of a given parent node. Simulates each move (w,a,s,d), and then finds all possible spawn
    possibilities. All these possibilities are considered children of the parent node.
    Parameters:
        board: the parent node being a Board object
        is_initial: Boolean value, to be used in the case we do not want to
                    simulate all possible moves, but just find all possible
                    spawn locations, to be used for depth 1 cases.
    Returns:
        A list of a all children nodes represented by Board objects, List(Board)
    """
    parents = []
    children = []
    if not is_initial:
        for move in board.moves_available(True):
            moved_board = Board(board.board, board.points)
            moved_board.make_move(move, False)
            parents.append(moved_board)
            del moved_board
    else:
        parents = [board]
    for parent in parents:
        for cell_index in parent.free_cells():
            for two_four in [2]:
                spawned_board = Board(parent.board, parent.points)
                spawned_board.spawn_number(
                    pick_random=False, rand=cell_index, spawn_number=two_four)
                children.append(spawned_board)
                del spawned_board
    return children
