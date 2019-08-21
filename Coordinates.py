class Coordinates:
    def __init__(self):
        self.row = 0
        self.col = 0

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def setRow(self, row):
        self.row = row

    def setCol(self, col):
        self.col = col

    def __str__(self):
        str = self.getRow(), self.getCol()
        return str
