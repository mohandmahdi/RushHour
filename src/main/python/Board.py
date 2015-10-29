from io import open
from copy import copy
from Orientation import Orientation
from Car import Car
from Copyable import Copyable


class Board(Copyable):
    def __init__(self, cars, finish, player_car_label='R', width=6, height=6):
        self.cars = cars
        self.finish = finish
        self.player_car_label = player_car_label
        self.width = width
        self.height = height

    def prettify(self):
        empty_board = [['_' for _ in range(self.width)] for _ in range(self.height)]
        for label, car in self.cars.iteritems():
            start = car.x if car.is_horizontal() else car.y
            for i in range(start, start + car.size):
                if car.is_horizontal():
                    empty_board[car.y][i] = car.label
                else:
                    empty_board[i][car.x] = car.label
        # add finish sign to board
        empty_board[self.finish[1]].insert(self.finish[0], '#')
        # collapse lists into string
        return ''.join([''.join(row) + '\n' for row in empty_board])

    def player_car(self):
        return self.cars[self.player_car_label]

    def move_car(self, label, amount):
        if self.can_move_car(label, amount):
            car = self.cars[label]
            if car.is_horizontal():
                car = car.copy(x = car.x + amount)
            else:
                car = car.copy(y = car.y + amount)
            cars_copy = copy(self.cars)
            cars_copy[label] = car
            return self.copy(cars=cars_copy)
        else:
            return None

    def can_move_car(self, label, amount):
        if label in self.cars:
            car = self.cars[label]
            newpos = None
            if car.is_horizontal():
                newpos = car.copy(x=car.x + amount)
                #bounds check
                if newpos.x < 0 or newpos.x + newpos.size > self.width:
                    return False
            else:
                newpos = car.copy(y=car.y + amount)
                if newpos.y < 0 or newpos.y + newpos.size > self.height:
                    return False

            intersections = [newpos.intersects(other) for _, other in self.cars.iteritems() if other != car]
            if not any(intersections):
                return True
        else:
            return False

    def board_completed(self):
        player_car = self.player_car()
        return player_car.x + player_car.size == self.finish[0]

def board_from_file(file):
    board = []
    finish_position = None
    row_size = 0

    handle = open(file, 'r')
    lines = handle.read().splitlines()
    handle.close()

    for rowIndex, line in enumerate(lines):
        row = []
        for colIndex, pos in enumerate(line):
            # finish position
            if pos == '#':
                finish_position = (colIndex, rowIndex)
            # car or empty spot
            else:
                row.append(pos)

        # first row counts the number of columns in a row
        row_length = len(row)
        if rowIndex == 0:
            row_size = row_length
        # check if row size is the same as every preceding one
        elif row_length != row_size:
            print('not all rows have the same size in level {}'.format(file))
            return None

        board.append(row)

    if not finish_position:
        print("could not find the finish in " + file)
        return None
    else:
        cars = find_cars(board)
        cars.extend(find_cars(board, True))

        cars = dict([(car.label, car) for car in cars])
        board = Board(cars, finish_position)
        if board.player_car_label not in cars:
            print('could not find player car with label {} in level {}'.format(board.player_car_label, file))
        else:
            # verify player is a horizontal car
            if board.player_car().is_vertical():
                print("player car can only be horizontal")
            elif board.player_car().y != board.finish[1]:

                print("player car is on a different row ({} != {}) as the finish in level {}".format(board.player_car().y, board.finish[1], file))
            else:
                return board
    return None


def find_cars(board, transpose=False):
    if transpose:
        board = [list(x) for x in zip(*board)]

    found_cars = []
    for rowIndex, row in enumerate(board):
        offset = 0
        length = 0
        start = 0
        current = row[offset]
        while offset < len(row):
            # skip empty spaces
            while current == '_' and offset < len(row) - 1:
                offset += 1
                start = offset
                current = row[offset]

            while offset < len(row) and row[offset] == current:
                length += 1
                offset += 1

            if length > 1:
                orientation = Orientation.VERTICAL if transpose else Orientation.HORIZONTAL
                car = Car(current, rowIndex if transpose else start, start if transpose else rowIndex, length, orientation)
                found_cars.append(car)

            if offset < len(row):
                current = row[offset]
                start = offset
                length = 0
            else:
                offset += 1
    return found_cars
