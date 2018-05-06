from Coordinates import Coordinates

class Cell:
    def __init__(self):
        self.coordinates = Coordinates()
        self.symbol = "-"
        self.recent_move = False

    def __init__(self, coordinates, symbol):
        self.coordinates = coordinates
        self.symbol = symbol
        self.recent_move = False

    def getRecentMove(self):
        return self.recent_move

    def getCoordinates(self):
        return self.coordinates

    def getSymbol(self):
        return self.symbol

    def setRecentMove(self, recent_move):
        self.recent_move = recent_move

    def setCoordinates(self, coordinates):
        self.coordinates = coordinates

    def setSymbol(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol