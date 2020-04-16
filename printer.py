from typing import Tuple, Set

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


# solution
from board import *
from reader import Reader

# reader = Reader(file='maps/mad_1.bff')
# blocks = reader.blocks
# grid = [2 * blocks[0], 2 * blocks[1]]
from solver import solve

def output_img(board: Board, checkpoints: Set[Point]):
    '''
    **Parameters**

        board: *Board object*
            
        checkpoints: *set*
            A set of point that needs to be passed by laser.

    **Returns**

        None
    '''
    rows = board.rows
    cols = board.cols

    plt.xlim(0, rows * 2)
    # move the x axis to top
    plt.gca().xaxis.tick_top()
    # invert the order of y axis
    plt.ylim(cols * 2, 0)
    # plot the grid with black
    plt.grid(color = '0.8')

    for x in range(rows):
        for y in range(cols):
            type_ = board.grid[x][y]

            if type_ == A:
                # fc = facecolor; ec = edgecolor
                # Rectangles(x, y, length, width) draws rectangle from the bottom left corner
                rect = mpatches.Rectangle((x * 2, y * 2), 2, 2, color='b')
                plt.gca().add_patch(rect)

            elif type_ == B:
                rect = mpatches.Rectangle((x * 2, y * 2), 2, 2, color='0.8')
                plt.gca().add_patch(rect)

            elif type_ == C:
                rect = mpatches.Rectangle((x * 2, y * 2), 2, 2, color='g')
                plt.gca().add_patch(rect)

            elif type_ == X:
                rect = mpatches.Rectangle((x * 2, y * 2), 2, 2, color='k')
                plt.gca().add_patch(rect)

    # plot the laser path
    for laser in board.calculate_all_lasers():
        path, _, _ = calculate_track_by_laser(laser, board)

        # transpose
        xs, ys = list(zip(*path))
        plt.plot(xs, ys, color='r')

    # plot checkpoints
    for point in checkpoints:
        # plot point(x,y) 
        plt.plot([point[0]], [point[1]], marker='o', markersize=10, color="red")

    # Set the figure size in inches.
    # fig.set_size_inches(w, h)
    plt.gcf().set_size_inches(rows * 2, cols * 2)

    my_x_ticks = np.arange(0, rows * 2 + 1, 1)
    my_y_ticks = np.arange(0, cols * 2 + 1, 1)
    # xticks(ticks, [labels])
    # Set locations and labels
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)

    reflect = mpatches.Patch(color='b', label='Reflect')
    opaque = mpatches.Patch(color='0.8', label='Opaque')
    refract = mpatches.Patch(color='g', label='Refract')
    no_block = mpatches.Patch(color='k', label='No_Block')
    # bbox_to_anchor=(1, 0.5): put the legend right next to the fig.
    plt.legend(handles=[reflect, opaque, refract, no_block], bbox_to_anchor=(1.12, 0.5))
    plt.title('Lazor Soltuion')
    plt.show()


if __name__ == "__main__":
    map = [
        "dark_1",
        # "mad_1",
        # "mad_2",
        # "mad_3",
        # "mad_4",
        # "mad_5",
        # "mad_7",
        # "numbered_6",
        # "showstopper_4",
        # "tiny_5",
        # "yarn_5",
    ][0]
    start, checkpoints = Reader(f'maps/{map}.bff')
    output_img(start, checkpoints)

    solution = solve(start, checkpoints)
    output_img(solution, checkpoints)
