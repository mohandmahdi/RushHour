from Board import *
import collections
from copy import copy
import math


def solve(board):
    return level([Solution(board, [])], {board.prettify()}, 500)


Solution = collections.namedtuple('Solution', ['board', 'moves'])

Move = collections.namedtuple('Move', ['label', 'amount'])


def level(to_explore, seen, steps_left):
    if steps_left > 0:
        print ("level: " + str(steps_left))
        next_to_explore = []

        for solution in to_explore:
            for car in solution.board.cars:
                for step in [x for x in range(-5, 6) if x != 0]:
                    newboard = solution.board
                    # perform the move in steps
                    for _ in range(0, int(math.fabs(step))):
                        if newboard:
                            newboard = newboard.move_car(car, int(math.copysign(1, step)))
                    if newboard:
                        newboard_string = newboard.prettify()
                        if newboard_string not in seen:
                           seen.add(newboard_string)

                        # valid move, we might explore it later
                        previous_moves = copy(solution.moves)
                        previous_moves.append(Move(car, step))
                        new_solution = Solution(newboard, previous_moves)
                        next_to_explore.append(new_solution)
                        # we found a solution
                        if newboard.board_completed():
                            return new_solution
        return level(next_to_explore, seen, steps_left - 1)
    return None
