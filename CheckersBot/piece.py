from checkerGame import *
from heuristicTree import *

class Piece(object):
    def __init__(self, color, xPos, yPos):
        self.color = color
        self.xPos = xPos
        self.yPos = yPos
        self.isKing = False
        self.isDead = False
        canGoUp = False
        if (color == "black"):
            canGoUp = True
        self.goesUp = canGoUp
        self.canGoLeft = False
        self.canGoRight = False

    def getColor(self):
        return self.color

    def getXPos(self):
        return self.xPos

    def getYPos(self):
        return self.yPos

    def getIsKing(self):
        return self.isKing

    def getIsDead(self):
        return self.isDead

    def newPosition(self, newX, newY):
        self.xPos = newX
        self.yPos = newY

    def becomeKing(self):
        self.isKing = True

    def becomeDead(self):
        self.isDead = True

    def getCanGoUp(self):
        return self.goesUp

    def setCanGoRight(self, truthVal):
        self.canGoRight = truthVal

    def setCanGoLeft(self, truthVal):
        self.canGoLeft = truthVal

    def getCanGoLeft(self):
        return self.canGoLeft

    def getCanGoRight(self):
        return self.canGoRight

    def setCanGoUp(self):
        self.goesUp = not self.goesUp