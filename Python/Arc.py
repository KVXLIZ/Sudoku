class Arc():
    def __init__(self, x, y):
        self.node1 = x
        self.node2 = y

class Node():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.box = self.calcBox(row, col)

    def calcBox(self, row, col):
        box = 0
        if row<3:
            if col<3:
                box = 0
            elif col<6:
                box = 1
            else:
                box = 2
        elif row<6:
            if col<3:
                box = 3
            elif col<6:
                box = 4
            else:
                box = 5
        else:
            if col<3:
                box = 6
            elif col<6:
                box = 7
            else:
                box = 8