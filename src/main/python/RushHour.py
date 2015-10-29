from Board import *
from Solver import solve
from Tkinter import Tk
from tkFileDialog import askopenfilename

def step(board, label, amount):
    newboard = board.move_car(label, amount)
    if newboard:
        print('moving ({},{}): {}'.format(label, amount, newboard is not None))
        print(newboard.prettify())
        print('completed: {}\n'.format(newboard.board_completed()))
    else:
        print('invalid move: ({}, {})'.format(label, amount))
        print(board.prettify())
    class NextStep():
        def __init__(self, board):
            self.board = board

        def step(self, label, amount): return step(self.board, label, amount)
    return NextStep(newboard if newboard else board)

if __name__ == '__main__':
    Tk().withdraw()
    file_name = askopenfilename(title='Select a level to solve')

    if(file_name):
        print('solving {}...'.format(file_name))
        board = board_from_file(file_name)
        if board:

            print('initial board: ')
            print(board.prettify())
            print('solving, please wait...')

            solved = solve(board)

            if solved:
                print ("solution: ")

                board_ref = board
                for move in solved.moves:

                    board_ref = board_ref.move_car(move.label, move.amount)
                    print('({}, {})'.format(move.label, move.amount))
                    print(board_ref.prettify())
                print('solved in {} steps'.format(len(solved.moves)))

            else:
                print("no solution")