from typing import Set
from board import *


def Reader(file) -> Tuple[Board, Set[Point]]:
    '''
    Reader function serves to read the board.bff files. 
    It collects the positions and the numbers of all A, B and C blocks as well as the "o" and "x" elements.
    The starting point of lazer and its original direction will also be extracted and stored.

    **Parameters**
        file: *str*
            The name of the .bff file to be read in.

    **return**
        board: *Board object*
            
        checkpoints: *set*
            A set of point that needs to be passed by laser.
    '''   
    
    grid = []
    n_blocks_list = [0, 0, 0]

    # the designated points to pass through
    checkpoints: Set[Point] = set()

    lasers: List[Laser] = []

    grid_start = False

    with open(file, 'r') as file:

        # Y=the number of lines, and X= the length of lines
        for line in file.readlines():
            line = line.strip()
            # spilt the elements with space and get the lists
            cells = line.split()  

            if line == "GRID START":
                grid_start = True

            elif line == "GRID STOP":
                grid_start = False

            # get the coordinate of each elements
            # index labeling
            elif grid_start:
                row = []
                for col, cell in enumerate(cells):
                    # A, B, C, o, x is imported from board
                    if cell == 'A':
                        row.append(A)
                    if cell == 'B':
                        row.append(B)
                    if cell == 'C':
                        row.append(C)
                    if cell == 'o':
                        row.append(O)
                    if cell == 'x':
                        row.append(X)

                grid.append(row)
            else:
                if line != "":
                    tokens = line.split()
                    # A, B, C is imported from board
                    if tokens[0] == "A":
                        n_blocks_list[A] = int(tokens[1])
                    if tokens[0] == "B":
                        n_blocks_list[B] = int(tokens[1])
                    if tokens[0] == "C":
                        n_blocks_list[C] = int(tokens[1])
                    if tokens[0] == "L":
                        origin = (int(tokens[1]), int(tokens[2]))
                        direction = (int(tokens[3]), int(tokens[4]))
                        lasers.append((origin, direction))
                    if tokens[0] == "P":
                        checkpoints.add((int(tokens[1]), int(tokens[2])))

    # transpose, switch the x and y position to fit the coordinate.
    grid = list(map(list, zip(*grid)))

    board = Board(
        grid=grid,
        n_blocks_list=n_blocks_list,
        lasers=lasers,
    )
    return board, checkpoints
