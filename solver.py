from typing import Set

from board import *
from reader import Reader

debug = True


def next_state(board: Board, checkpoints: Set[Point]) -> Tuple[List[Board], bool]:
    '''
    **Parameters**

        board: *Board object*
            
        checkpoints: *set*
            A set of point that needs to be passed by laser.

    **Returns**

        next_boards: *list*
            A list that save the state of next board.
        completed: *bool*
            If true, all the points in checkpoints have been passed thru by lasers.
    '''
    covered = set()
    blocks = set()

    # lasers: list of laser.
    # laser: *Tuple[Point, Direction]*
    # Point, direction: *Tuple[int, int]*
    lasers = board.calculate_all_lasers()
    for laser in lasers:
        direction = laser[1]
        path, _, _ = calculate_track_by_laser(laser, board)
        # print(path)

        # Calculate the blocks occupied by the points that laser pass thru. 
        for pos in path[:-1]:
            block = calculate_block_by_point_and_direction(pos, direction)
            blocks.add(block)
        covered.update(path)

    completed = False
    # Check if covered is a super set of checkpoints
    if covered >= checkpoints:
        completed = True

    next_boards = []
    # blocks = pick_blocks
    # print(board.n_blocks_list, blocks)
    for type_, value in enumerate(board.n_blocks_list):
        if not value:
            continue

        if completed:
            all_blocks = set()
            for i in range(board.rows):
                for j in range(board.cols):
                    all_blocks.add((i, j))
            blocks = all_blocks
        if type_ == B:
            blocks = set()
            for i in range(board.rows):
                for j in range(board.cols):
                    blocks.add((i, j))

        for block in blocks:
            if board.grid[block[0]][block[1]] != O:
                continue
            # Here, we perform deepcopy for grid so that next_board won't affect original board.
            next_board = board.copy()
            next_board.set_block(block, type_)
            next_boards.append(next_board)
    return next_boards, completed


def featurize_board(board: Board) -> Tuple:
    '''
    Give a certain layout of board a feature.
    '''
    # grid: List[List[int]]
    # sum(iterable, start): returns the sum of list + start. iterable: *list, int*
    # e.g. sum([list1, list2],start = []) = [list1[0]+list2[0], list1[1]+list2[1], list1[2]+list2[2]]
    return tuple(sum(board.grid, []))


def solve(start: Board, checkpoints: Set[Point]) -> Board:
    '''
    This will save a maze object to a file.

    **Parameters**

        board: *Board object*
            
        checkpoints: *set*
            A set of point that needs to be passed by laser.

    **Returns**

        board: *Board object*
            The completed board.
    '''
    queue = [start]
    known = set()
    # Record a certain layout of board.
    known.add(featurize_board(start))

    while queue:
        board = queue.pop(0)

        next_boards, completed = next_state(board, checkpoints)

        if completed and sum(board.n_blocks_list, 0) == 0:
            return board

        for next_board in next_boards:
            feature = featurize_board(next_board)
            if feature in known:
                continue
            queue.append(next_board)
            known.add(feature)


if __name__ == '__main__':
    start, checkpoints = Reader('maps/tiny_5.bff')

    solution = solve(start, checkpoints)
    print(start)
    print(checkpoints)
    print(solution)
