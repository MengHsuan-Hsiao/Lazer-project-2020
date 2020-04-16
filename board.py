from copy import deepcopy
from typing import List, Tuple, Set

Point = Tuple[int, int]
Block = Tuple[int, int]
Direction = Tuple[int, int]
Laser = Tuple[Point, Direction]

A = 0
B = 2
C = 1
O = 8
X = 9

debug = False


class Board(object):
    '''
    **Parameters**

        self: *class object*
            object's name.
        grid: *list[list]*
            A list of lists that constructs the grid for blocks.
        n_blocks_list: *list[int, int, int]*
            A list of numbers of type A, B, C block respectively.
        lasers: *list*
            A list of all the given lasers.
            laser: *Tuple[Point, Direction], Point, direction: Tuple[int, int]*
    '''

    grid: List[List[int]]
    n_blocks_list: List[int]
    lasers: Set[Laser]

    def __init__(self, grid, n_blocks_list, lasers):
        self.grid = grid
        self.n_blocks_list = n_blocks_list
        # Change the lasers from list to set.
        self.lasers = set(lasers)

    def __str__(self):
        grid = ''
        for row in self.grid:
            grid += f'    {row}\n'

        return f'\n' \
               f'  grid:\n{grid}' \
               f'  n_blocks_list: {self.n_blocks_list}\n' \
               f'  lasers: {self.lasers}'

    def copy(self):
        '''
        **Returns**

            Board: *Board object*
                Return the board with the current n_blocks_list as input.
        '''
        return Board(
            # copy(from copy module): shallow copy, any changes made to a copy of obeject will affect the original object.
            # deepcopy: any changes to the copy object will not affect the original object.
            deepcopy(self.grid),
            # The copy here is not from copy module, but the copy fcn defined here.
            self.n_blocks_list.copy(),
            self.lasers
        )

    # Using @porperty as a decorator
    # Act as a getter fcn, used to get the value of attribute.
    @property
    def rows(self):
        return len(self.grid)

    @property
    def cols(self):
        return len(self.grid[0])

    def set_block(self, block: Block, type_: int):
        '''
        **Parameters**

            self: *Board object*

            block: *Tuple[int, int]*
                Current position of the block.
            type_: *int*
                block type defined by given int.
        
        **Returns**

            None
        '''
        # deduct the number of certain block type once it get set.
        self.n_blocks_list[type_] -= 1
        self.grid[block[0]][block[1]] = type_

    # def unset_block(self, point: Point):
    #     type_ = self.grid[point[0]][point[1]]
    #     self.grid[point[0]][point[1]] = O
    #     self.n_blocks_list[type_] += 1

    def calculate_all_lasers(self):
        '''
        **Returns**

            known: *set*
                A set of all lasers.
        '''
        # queue is a set of lasers
        queue = self.lasers.copy()
        known = set()

        while queue:
            laser = queue.pop()

            if laser in known:
                continue
            known.add(laser)

            _, sub_lasers, _ = calculate_track_by_laser(laser, self)
            # add sub_laser to the queue set.
            queue.update(sub_lasers)

        return known


def calculate_point_by_direction(point: Point, direction: Direction) -> Point:
    '''
    **Parameters**

        point: *Tuple[int, int]*
            A tuple of current position.
        direction: *Tuple[int, int]*
            A tuple of current direction.

    **Returns**

        new_point: *Tuple[int, int]*
            The newly calculated point.
    '''
    return point[0] + direction[0], point[1] + direction[1]

def calculate_block_by_point_and_direction(point: Point, direction: Direction) -> Point:
    '''
    **Parameters**

        point: *Tuple[int, int]*
            A tuple of current position.
        direction: *Tuple[int, int]*
            A tuple of current direction.

    **Returns**

        next_block: *Tuple[int, int]*
            The block position where next point sits at.
    '''
    # dest: destination
    dest = calculate_point_by_direction(point, direction)
    if point[0] % 2 == 0:
        # if x is even, the next block of next point will sit on horizontal direction
        return dest[0] // 2, point[1] // 2
    else:
        # if x is odd, the next block of next point will sit on vertical directioin
        return point[0] // 2, dest[1] // 2

def calculate_track_by_laser(laser: Laser, board: Board) -> Tuple[List[Point], List[Laser], bool]:
    '''
    **Parameters**

        laser: *Tuple[Point, Direction]*
            Point, direction: Tuple[int, int]
            Current laser position and its direction.
        board: *Board object*

    **Returns**

        path: *list*
            A list of given point w/ laser.
            point: *Tuple[int, int]*
        lasers: *list*
            A list of all the calculated lasers.
            laser: *Tuple[Point, Direction], Point, direction: Tuple[int, int]*
        is_open: *bool*
            Determine whether the position is taken by block or out of bounds.
    '''
    point, direction = laser
    path = []
    lasers = []
    is_open = True

    while True:
        path.append(point)
        block = calculate_block_by_point_and_direction(point, direction)

        if is_block_out(block, board):
            break
        
        type_ = board.grid[block[0]][block[1]]
        if type_ == A:
            # if the laser hit the top or bottom of the block
            if point[1] % 2 == 0:
                next_direction = (direction[0], -direction[1])

            # if the laser hit the left or right of the block
            else:
                next_direction = (-direction[0], direction[1])

            lasers.append((point, next_direction))

            is_open = False
            break

        elif type_ == B:
            is_open = False
            break

        elif type_ == C:
            # Add a new point that reflect
            if point[1] % 2 == 0:
                next_direction = (direction[0], -direction[1])
            else:
                next_direction = (-direction[0], direction[1])
            lasers.append((point, next_direction))

            # Add a new point that pass thru
            next_point = calculate_point_by_direction(point, direction)
            lasers.append((next_point, direction))

            is_open = False
            break

        elif type_ == X or type_ == O:
            pass

        # Simply calculate the next point if no block at all.
        point = calculate_point_by_direction(point, direction)

        if is_point_out(point, board):
            break

    # print(path, lasers, is_open)
    return path, lasers, is_open


def is_point_out(point: Point, board: Board) -> bool:
    '''
    **Parameters**

        Point: *Tuple[int, int]*
            Current position of the point.
        board: *Board object*

    **Returns**

        bool
    '''
    x, y = point

    # Multipy the rows and columns by two since the grid was originally designed for blocks. 
    if x > board.rows * 2:
        return True
    if x < 0:
        return True
    if y > board.cols * 2:
        return True
    if y < 0:
        return True

    return False


def is_block_out(block: Block, board: Board) -> bool:
    '''
    **Parameters**

        block: *Tuple[int, int]*
            Current position of the block.
        board: *Board object*

    **Returns**

        bool
    '''
    x, y = block

    if x >= board.rows:
        return True
    if x < 0:
        return True
    if y >= board.cols:
        return True
    if y < 0:
        return True

    return False
