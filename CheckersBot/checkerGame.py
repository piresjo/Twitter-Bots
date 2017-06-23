from heuristicTree import *
from piece import *

class MinimaxWrapper(object):
    def __init__(self, piece, color, isLeft, minimaxScore):
        self.color = color
        self.isLeft = isLeft
        self.minimaxScore = minimaxScore
        self.piece = piece

    def getPiece(self):
    	return self.piece

   	def getIsLeft(self):
   		return self.isLeft

class Game(object):
    def __init__(self):
        self.pieceNumber = 24;
        self.gameBoard = None;
        self.whitePieceNumber = 12;
        self.blackPieceNumber = 12;
        self.isWhiteTurn = False;
        self.blackPieces = []
        self.whitePieces = []

    def getWhitePieces(self):
        return self.whitePieces

    def getBlackPieces(self):
        return self.blackPieces

    def getGameBoard(self):
        return self.gameBoard

    def getWhitePieces(self):
        return self.whitePieces

    def getBlackPieces(self):
        return self.blackPieces

    def getWhitePieceNumber(self):
        return self.whitePieceNumber

    def getBlackPieceNumber(self):
        return self.blackPieceNumber

    def countPieceNumbers(self):
        whiteCount = 0
        blackCount = 0
        for piece in self.whitePieces:
            if (not(piece.getIsDead())):
                whiteCount += 1

        for piece in self.blackPieces:
            if (not(piece.getIsDead())):
                blackCount += 1

        self.whitePieceNumber = whiteCount
        self.blackPieceNumber = blackCount

    def copyGameBoard(self, copyBoard, blackPieces, whitePieces):
        self.gameBoard = copyBoard
        self.whitePieces = whitePieces
        self.blackPieces = blackPieces
        self.countPieceNumbers()

    def generateGameBoard(self):
        self.blackPieces = []
        self.whitePieces = []
        dimension = 8
        self.gameBoard = [[None for x in range(dimension)] for y in range(dimension)]
        for y in range(0, 3):
            for x in range(dimension):
                if x % 2 == 0 and y % 2 == 0:
                    newWhitePiece = Piece("white", x, y)
                    self.whitePieces.append(newWhitePiece)
                    self.gameBoard[y][x] = newWhitePiece
                elif x % 2 == 1 and y % 2 == 1:
                    newWhitePiece = Piece("white", x, y)
                    self.whitePieces.append(newWhitePiece)
                    self.gameBoard[y][x] = newWhitePiece
                else:
                    continue

        for y in range(5, 8):
            for x in range(dimension):
                if x % 2 == 1 and y % 2 == 1:
                    newBlackPiece = Piece("black", x, y)
                    self.blackPieces.append(newBlackPiece)
                    self.gameBoard[y][x] = newBlackPiece
                elif x % 2 == 0 and y % 2 == 0:
                    newBlackPiece = Piece("black", x, y)
                    self.blackPieces.append(newBlackPiece)
                    self.gameBoard[y][x] = newBlackPiece
                else:
                    continue

        return

    def canPieceMove(self, checkPiece):
        newLeftX = 0
        newRightX = 0
        newY = 0
        newJumpLeft = 0
        newJumpRight = 0
        newJumpY = 0
        if (checkPiece.getCanGoUp()):
            newY = checkPiece.getYPos() - 1
            newJumpY = newY - 1
        else:
            newY = checkPiece.getYPos() + 1
            newJumpY = newY + 1
        
        newLeftX = checkPiece.getXPos() - 1
        newJumpLeft = newLeftX - 1
        newRightX = checkPiece.getXPos() + 1
        newJumpRight = newRightX + 1

        if newLeftX >= 0 and (newY >= 0 or newJumpY <= 7):
            newLeftValue = self.gameBoard[newY][newLeftX]
            if newLeftValue is None:
                checkPiece.setCanGoLeft(True)
            else:
                if newLeftValue.getColor() == "white":
                    checkPiece.setCanGoLeft(False)
                else:
                    if newJumpLeft >= 0 and (newJumpY >= 0 or newJumpY <= 7):
                        jumpPieceVal = self.gameBoard[newJumpY][newJumpLeft]
                        if jumpPieceVal is None:
                            checkPiece.setCanGoLeft(True)
                        else:
                            checkPiece.setCanGoLeft(False)
                    else:
                        checkPiece.setCanGoLeft(False)
        else:
            checkPiece.setCanGoLeft(False)

        if newRightX <= 7 and (newY >= 0 or newJumpY <= 7):
            newRightValue = self.gameBoard[newY][newRightX]
            if newRightValue is None:
                checkPiece.setCanGoRight(True)
            else:
                if newRightValue.getColor() == "white":
                    checkPiece.setCanGoRight(False)
                else:
                    if newJumpRight <= 7 and (newJumpY >= 0 or newJumpY <= 7):
                        jumpPieceVal = self.gameBoard[newJumpY][newJumpRight]
                        if jumpPieceVal is None:
                            checkPiece.setCanGoRight(True)
                        else:
                            checkPiece.setCanGoRight(False)
                    else:
                        checkPiece.setCanGoRight(False)
        else:
            checkPiece.setCanGoRight(False)

        return

    def drawColorStatus(self, color):
        piecesVal = []
        if (color == "white"):
            returnString = "White:\n"
            piecesVal = self.whitePieces
        else:
            returnString = "Black:\n"
            piecesVal = self.blackPieces
        count = 1
        for piece in piecesVal:
            addString = str(count) + "- ";
            if piece.getIsDead():
                addString = addString + "DEAD\n"
                returnString = returnString + addString
            else:
                addString = addString + "(" + str(piece.getXPos()) + "," + str(piece.getYPos()) + ")"
                if piece.getIsKing():
                    addString = addString + "K"
                addString = addString + "\n"
                returnString = returnString + addString
            count += 1
        return returnString

    def killPiece(self, color, xVal, yVal):
        pieceVal = []
        if (color == "white"):
            pieceVal = self.whitePieces
        else:
            pieceVal = self.blackPieces

        for piece in pieceVal:
            if (piece.getXPos() == xVal and piece.getYPos() == yVal):
                piece.becomeDead()
                self.gameBoard[yVal][xVal] = None

    def kingPiece(self, color, xVal, yVal):
        pieceVal = []
        if (color == "white"):
            pieceVal = self.whitePieces
        else:
            pieceVal = self.blackPieces

        for piece in pieceVal:
            if (piece.getXPos() == xVal and piece.getYPos() == yVal):
                piece.becomeKing()

    def drawBoard(self):
        self.countPieceNumbers()
        dimension = len(self.gameBoard[0])
        returnString = ""
        for row in range(dimension):
            for col in range(dimension):
                checkVal = self.gameBoard[row][col]
                if checkVal is None:
                    returnString = returnString + "."
                else:
                    if checkVal.getColor() == "white":
                        if checkVal.getIsKing():
                            returnString = returnString + "W"
                        else:
                            returnString = returnString + "w"
                    else:
                        if checkVal.getIsKing():
                            returnString = returnString + "B"
                        else:
                            returnString = returnString + "b"
            returnString = returnString + "\n"
        turnString = ""
        if self.isWhiteTurn:
            turnString = " T:White"
        else:
            turnString = " T:Black"

        finalLine = "Black:" + str(self.blackPieceNumber) + " White:" + str(self.whitePieceNumber) + turnString
        returnString = returnString + finalLine 
        return returnString

    def movePiece(self, piece, newX, newY):
        self.canPieceMove(piece)
        if piece.getCanGoRight() is False and piece.getCanGoLeft() is False:
            raise ValueError("Can't move piece")

        if piece.getCanGoLeft() is False and newX < piece.getXPos():
            raise ValueError("Can't move piece")

        if piece.getCanGoRight() is False and newX > piece.getXPos():
            raise ValueError("Can't move piece")

        if (piece.getCanGoUp() is True and newY > piece.getYPos()) or \
           (piece.getCanGoUp() is False and newY < piece.getYPos()) or \
           (newY == piece.getYPos()):
           raise ValueError("Can't move piece")

        if (newX != piece.getXPos() + 1) and \
           (newX != piece.getXPos() - 1) and \
           (newX != piece.getXPos() + 2) and \
           (newX != piece.getXPos() - 2):
           raise ValueError("Can't move piece")

        self.gameBoard[piece.getYPos()][piece.getXPos()] = None

        if newX == piece.getXPos() + 2:
            if piece.getCanGoUp():
                findPiece = self.gameBoard[piece.getYPos() - 1][piece.getXPos() + 1]
            else:
                findPiece = self.gameBoard[piece.getYPos() + 1][piece.getXPos() + 1] 

            self.killPiece(findPiece.getColor(), findPiece.getXPos(), findPiece.getYPos())

        if newX == piece.getXPos() - 2:
            if piece.getCanGoUp():
                findPiece = self.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1]
            else:
                findPiece = self.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1]

            self.killPiece(findPiece.getColor(), findPiece.getXPos(), findPiece.getYPos())
        

        piece.newPosition(newX, newY)
        self.gameBoard[newY][newX] = piece
        self.countPieceNumbers()

    def generateScore(self, pieceArray, enemyArray):
        scoreNumPieces = 5
        scoreNumKings = 10
        scoreNumberInvulnerable = 2
        scoreNumberPartiallyInvulnerable = 1
        yourScore = 0
        theirScore = 0
        for piece in pieceArray:
            if not piece.getIsDead() and not piece.getIsKing():
                yourScore += scoreNumPieces
            if not piece.getIsDead() and piece.getIsKing():
                yourScore += scoreNumKings
            self.canPieceMove(piece)
            if not piece.getCanGoRight() and not piece.getCanGoLeft():
                yourScore += scoreNumberInvulnerable
            if piece.getCanGoRight() or piece.getCanGoLeft():
                yourScore += scoreNumberPartiallyInvulnerable

        for piece in enemyArray:
            if not piece.getIsDead() and not piece.getIsKing():
                theirScore += scoreNumPieces
            if not piece.getIsDead() and piece.getIsKing():
                theirScore += scoreNumKings
            self.canPieceMove(piece)
            if not piece.getCanGoRight() and not piece.getCanGoLeft():
                theirScore += scoreNumberInvulnerable
            if piece.getCanGoRight() or piece.getCanGoLeft():
                theirScore += scoreNumberPartiallyInvulnerable

        finalScore = yourScore - theirScore
        return finalScore


    def pickPieceAndMove(self, startingColor):
        # Get all moveable pieces
        piecesArray = []
        iterateArray = []
        if startingColor == "white":
            iterateArray = self.getWhitePieces()
        else:
            iterateArray = self.getBlackPieces()

        for piece in iterateArray:
            self.canPieceMove(piece)
            if piece.getCanGoRight() or piece.getCanGoLeft():
                piecesArray.append(piece)

        heuristicArray = []
        # For each of the movable pieces
        for piece in piecesArray:
            heuristic = HeuristicTree()
            # Layer 1
            # Layer 2 - Enemies
            # Layer 3 - Theoretical Second Move
            if piece.getCanGoLeft():
                theoreticalGameNode1 = Game()
                theoreticalGameNode1.copyGameBoard(self.gameBoard)
                enemyArray = []
                yourPieceArray = []
                if piece.getCanGoUp():
                    if self.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                        theoreticalGameNode1.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                    else:
                        theoreticalGameNode1.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                else:
                    if self.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                        theoreticalGameNode1.movePiece(piece, piece.getYPos() + 1, piece.getXPos() - 1)
                    else:
                        theoreticalGameNode1.movePiece(piece, piece.getYPos() + 2, piece.getXPos() - 2)

                if startingColor == "white":
                    yourPieceArray = theoreticalGameNode1.getWhitePieces()
                    enemyArray = theoreticalGameNode1.getBlackPieces()
                else:
                    yourPieceArray = theoreticalGameNode1.getBlackPieces()
                    enemyArray = theoreticalGameNode1.getWhitePieces() 

                score = self.generateScore(yourPieceArray, enemyArray)
                heuristic.insert(score, 1)
                availableEnemyPieces = []
                for piece in enemyArray:
                    theoreticalGameNode1.canPieceMove(piece)
                    if piece.getCanGoRight() or piece.getCanGoLeft() and not piece.getIsDead():
                        availableEnemyPieces.append(piece)

                theoreticalGameNode3 = Game()
                theoreticalGameNode3.copyGameBoard(theoreticalGameNode1.getGameBoard())
                theoreticalGameNode4 = Game()
                theoreticalGameNode4.copyGameBoard(theoreticalGameNode1.getGameBoard())

                if len(availableEnemyPieces) >= 1:
                    if len(availableEnemyPieces) == 1:
                        pieceForNodeThree = availableEnemyPieces[0]
                        pieceForNodeFour = availableEnemyPieces[0]
                    else:
                        pieceForNodeThree = availableEnemyPieces.pop()
                        pieceForNodeFour = availableEnemyPieces.pop()

                    # For node 3
                    if pieceForNodeThree.getCanGoLeft():
                        enemyArray = []
                        yourPieceArray = []
                        if piece.getCanGoUp():
                            if theoreticalGameNode3.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                        else:
                            if theoreticalGameNode3.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() + 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() + 2, piece.getXPos() - 2)

                        if startingColor == "white":
                            yourPieceArray = theoreticalGameNode3.getWhitePieces()
                            enemyArray = theoreticalGameNode3.getBlackPieces()
                        else:
                            yourPieceArray = theoreticalGameNode3.getBlackPieces()
                            enemyArray = theoreticalGameNode3.getWhitePieces() 

                        score = self.generateScore(yourPieceArray, enemyArray)
                        heuristic.insert(score, 3)
                    else:
                        enemyArray = []
                        yourPieceArray = []
                        if piece.getCanGoUp():
                            if theoreticalGameNode3.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                        else:
                            if theoreticalGameNode3.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() + 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() + 2, piece.getXPos() - 2)

                        if startingColor == "white":
                            yourPieceArray = theoreticalGameNode3.getWhitePieces()
                            enemyArray = theoreticalGameNode3.getBlackPieces()
                        else:
                            yourPieceArray = theoreticalGameNode3.getBlackPieces()
                            enemyArray = theoreticalGameNode3.getWhitePieces() 

                        score = self.generateScore(yourPieceArray, enemyArray)
                        heuristic.insert(score, 3)

                        # Now get the stuff for nodes 7 and 8
                        availableYourPieces = []
                        for piece in yourPieceArray:
                            theoreticalGameNode3.canPieceMove(piece)
                            if piece.getCanGoRight() or piece.getCanGoLeft() and not piece.getIsDead():
                                availableEnemyPieces.append(piece)

                        theoreticalGameNode7 = Game()
                        theoreticalGameNode7.copyGameBoard(theoreticalGameNode3.getGameBoard())
                        theoreticalGameNode8 = Game()
                        theoreticalGameNode8.copyGameBoard(theoreticalGameNode3.getGameBoard())

                        if len(availableEnemyPieces) >= 1:
                            if len(availableEnemyPieces) == 1:
                                pieceForNodeSeven = availableEnemyPieces[0]
                                pieceForNodeEight = availableEnemyPieces[0]
                            else:
                                pieceForNodeSeven = availableEnemyPieces.pop()
                                pieceForNodeEight = availableEnemyPieces.pop()

                            if pieceForNodeSeven.getCanGoLeft():
                                enemyArray = []
                                yourPieceArray = []
                                if pieceForNodeSeven.getCanGoUp():
                                    if theoreticalGameNode7.gameBoard[pieceForNodeSeven.getYPos() - 1][pieceForNodeSeven.getXPos() - 1] is None:
                                        theoreticalGameNode7.movePiece(pieceForNodeSeven, pieceForNodeSeven.getYPos() - 1, pieceForNodeSeven.getXPos() - 1)
                                    else:
                                        theoreticalGameNode7.movePiece(pieceForNodeSeven, pieceForNodeSeven.getYPos() - 2, pieceForNodeSeven.getXPos() - 2)
                                else:
                                    if theoreticalGameNode7.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode7.movePiece(pieceForNodeSeven, pieceForNodeSeven.getYPos() + 1, pieceForNodeSeven.getXPos() - 1)
                                    else:
                                        theoreticalGameNode7.movePiece(pieceForNodeSeven, pieceForNodeSeven.getYPos() + 2, pieceForNodeSeven.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode7.getWhitePieces()
                                    enemyArray = theoreticalGameNode7.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode7.getBlackPieces()
                                    enemyArray = theoreticalGameNode7.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 7)
                            else:
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode7.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode7.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                                    else:
                                        theoreticalGameNode7.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                                else:
                                    if theoreticalGameNode7.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode7.movePiece(piece, piece.getYPos() + 1, piece.getXPos() - 1)
                                    else:
                                        theoreticalGameNode7.movePiece(piece, piece.getYPos() + 2, piece.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode7.getWhitePieces()
                                    enemyArray = theoreticalGameNode7.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode7.getBlackPieces()
                                    enemyArray = theoreticalGameNode7.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 7)

                            # For node 8
                            if pieceForNodeEight.getCanGoLeft():
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode8.gameBoard[pieceForNodeEight.getYPos() - 1][pieceForNodeEight.getXPos() - 1] is None:
                                        theoreticalGameNode8.movePiece(pieceForNodeEight, piece.getYPos() - 1, pieceForNodeEight.getXPos() - 1)
                                    else:
                                        theoreticalGameNode8.movePiece(pieceForNodeEight, pieceForNodeEight.getYPos() - 2, pieceForNodeEight.getXPos() - 2)
                                else:
                                    if theoreticalGameNode8.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode8.movePiece(pieceForNodeEight, pieceForNodeEight.getYPos() + 1, pieceForNodeEight.getXPos() - 1)
                                    else:
                                        theoreticalGameNode8.movePiece(pieceForNodeEight, pieceForNodeEight.getYPos() + 2, pieceForNodeEight.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode8.getWhitePieces()
                                    enemyArray = theoreticalGameNode8.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode8.getBlackPieces()
                                    enemyArray = theoreticalGameNode8.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 8)
                            else:
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode8.gameBoard[pieceForNodeEight.getYPos() - 1][pieceForNodeEight.getXPos() - 1] is None:
                                        theoreticalGameNode8.movePiece(pieceForNodeEight, pieceForNodeEight.getYPos() - 1, pieceForNodeEight.getXPos() - 1)
                                    else:
                                        theoreticalGameNode8.movePiece(pieceForNodeEight, pieceForNodeEight.getYPos() - 2, pieceForNodeEight.getXPos() - 2)
                                else:
                                    if theoreticalGameNode8.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode8.movePiece(pieceForNodeEight, pieceForNodeEight.getYPos() + 1, pieceForNodeEight.getXPos() - 1)
                                    else:
                                        theoreticalGameNode8.movePiece(pieceForNodeEight, pieceForNodeEight.getYPos() + 2, pieceForNodeEight.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode8.getWhitePieces()
                                    enemyArray = theoreticalGameNode8.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode8.getBlackPieces()
                                    enemyArray = theoreticalGameNode8.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 8)




                    # For node 4
                    if pieceForNodeFour.getCanGoLeft():
                        enemyArray = []
                        yourPieceArray = []
                        if piece.getCanGoUp():
                            if self.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode4.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode4.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                        else:
                            if self.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode4.movePiece(piece, piece.getYPos() + 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode4.movePiece(piece, piece.getYPos() + 2, piece.getXPos() - 2)

                        if startingColor == "white":
                            yourPieceArray = theoreticalGameNode4.getWhitePieces()
                            enemyArray = theoreticalGameNode4.getBlackPieces()
                        else:
                            yourPieceArray = theoreticalGameNode4.getBlackPieces()
                            enemyArray = theoreticalGameNode4.getWhitePieces() 

                        score = self.generateScore(yourPieceArray, enemyArray)
                        heuristic.insert(score, 4)
                    else:
                        enemyArray = []
                        yourPieceArray = []
                        if piece.getCanGoUp():
                            if self.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode4.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode4.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                        else:
                            if self.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode4.movePiece(piece, piece.getYPos() + 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode4.movePiece(piece, piece.getYPos() + 2, piece.getXPos() - 2)

                        if startingColor == "white":
                            yourPieceArray = theoreticalGameNode4.getWhitePieces()
                            enemyArray = theoreticalGameNode4.getBlackPieces()
                        else:
                            yourPieceArray = theoreticalGameNode4.getBlackPieces()
                            enemyArray = theoreticalGameNode4.getWhitePieces() 

                        score = self.generateScore(yourPieceArray, enemyArray)
                        heuristic.insert(score, 4)

                        # Now get the stuff for nodes 9 and 10
                        availableYourPieces = []
                        for piece in yourPieceArray:
                            theoreticalGameNode4.canPieceMove(piece)
                            if piece.getCanGoRight() or piece.getCanGoLeft() and not piece.getIsDead():
                                availableEnemyPieces.append(piece)

                        theoreticalGameNode9 = Game()
                        theoreticalGameNode9.copyGameBoard(theoreticalGameNode3.getGameBoard())
                        theoreticalGameNode10 = Game()
                        theoreticalGameNode10.copyGameBoard(theoreticalGameNode3.getGameBoard())

                        if len(availableEnemyPieces) >= 1:
                            if len(availableEnemyPieces) == 1:
                                pieceForNodeNine = availableEnemyPieces[0]
                                pieceForNodeTen = availableEnemyPieces[0]
                            else:
                                pieceForNodeNine = availableEnemyPieces.pop()
                                pieceForNodeTen = availableEnemyPieces.pop()

                            if pieceForNodeNine.getCanGoLeft():
                                enemyArray = []
                                yourPieceArray = []
                                if pieceForNodeNine.getCanGoUp():
                                    if theoreticalGameNode9.gameBoard[pieceForNodeNine.getYPos() - 1][pieceForNodeNine.getXPos() - 1] is None:
                                        theoreticalGameNode9.movePiece(pieceForNodeNine, pieceForNodeNine.getYPos() - 1, pieceForNodeNine.getXPos() - 1)
                                    else:
                                        theoreticalGameNode9.movePiece(pieceForNodeNine, pieceForNodeNine.getYPos() - 2, pieceForNodeNine.getXPos() - 2)
                                else:
                                    if theoreticalGameNode9.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode9.movePiece(pieceForNodeNine, pieceForNodeNine.getYPos() + 1, pieceForNodeNine.getXPos() - 1)
                                    else:
                                        theoreticalGameNode9.movePiece(pieceForNodeNine, pieceForNodeNine.getYPos() + 2, pieceForNodeNine.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode9.getWhitePieces()
                                    enemyArray = theoreticalGameNode9.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode9.getBlackPieces()
                                    enemyArray = theoreticalGameNode9.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 9)
                            else:
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode9.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode9.movePiece(pieceForNodeNine, pieceForNodeNine.getYPos() - 1, pieceForNodeNine.getXPos() - 1)
                                    else:
                                        theoreticalGameNode9.movePiece(pieceForNodeNine, pieceForNodeNine.getYPos() - 2, pieceForNodeNine.getXPos() - 2)
                                else:
                                    if theoreticalGameNode9.gameBoard[pieceForNodeNine.getYPos() + 1][pieceForNodeNine.getXPos() - 1] is None:
                                        theoreticalGameNode9.movePiece(pieceForNodeNine, pieceForNodeNine.getYPos() + 1, pieceForNodeNine.getXPos() - 1)
                                    else:
                                        theoreticalGameNode9.movePiece(pieceForNodeNine, pieceForNodeNine.getYPos() + 2, pieceForNodeNine.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode9.getWhitePieces()
                                    enemyArray = theoreticalGameNode9.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode9.getBlackPieces()
                                    enemyArray = theoreticalGameNode9.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 9)

                            # For node 10
                            if pieceForNodeTen.getCanGoLeft():
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode10.gameBoard[pieceForNodeTen.getYPos() - 1][pieceForNodeTen.getXPos() - 1] is None:
                                        theoreticalGameNode10.movePiece(pieceForNodeTen, piece.getYPos() - 1, pieceForNodeTen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode10.movePiece(pieceForNodeTen, pieceForNodeTen.getYPos() - 2, pieceForNodeTen.getXPos() - 2)
                                else:
                                    if theoreticalGameNode10.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode10.movePiece(pieceForNodeTen, pieceForNodeTen.getYPos() + 1, pieceForNodeTen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode10.movePiece(pieceForNodeTen, pieceForNodeTen.getYPos() + 2, pieceForNodeTen.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode10.getWhitePieces()
                                    enemyArray = theoreticalGameNode10.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode10.getBlackPieces()
                                    enemyArray = theoreticalGameNode10.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 10)
                            else:
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode10.gameBoard[pieceForNodeTen.getYPos() - 1][pieceForNodeTen.getXPos() - 1] is None:
                                        theoreticalGameNode10.movePiece(pieceForNodeTen, pieceForNodeTen.getYPos() - 1, pieceForNodeTen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode10.movePiece(pieceForNodeTen, pieceForNodeTen.getYPos() - 2, pieceForNodeTen.getXPos() - 2)
                                else:
                                    if theoreticalGameNode10.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode10.movePiece(pieceForNodeTen, pieceForNodeTen.getYPos() + 1, pieceForNodeTen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode10.movePiece(pieceForNodeTen, pieceForNodeTen.getYPos() + 2, pieceForNodeTen.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode10.getWhitePieces()
                                    enemyArray = theoreticalGameNode10.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode10.getBlackPieces()
                                    enemyArray = theoreticalGameNode10.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 10)
                else:
                    pass


            if piece.getCanGoRight():
                theoreticalGameNode2 = Game()
                theoreticalGameNode2.copyGameBoard(self.gameBoard)
                if piece.getCanGoUp():
                    if self.gameBoard[piece.getYPos() - 1][piece.getXPos() + 1] is None:
                        theoreticalGameNode2.movePiece(piece, piece.getYPos() - 1, piece.getXPos() + 1)
                    else:
                        theoreticalGameNode2.movePiece(piece, piece.getYPos() - 2, piece.getXPos() + 2)
                else:
                    if self.gameBoard[piece.getYPos() + 1][piece.getXPos() + 1] is None:
                        theoreticalGameNode2.movePiece(piece, piece.getYPos() + 1, piece.getXPos() + 1)
                    else:
                        theoreticalGameNode2.movePiece(piece, piece.getYPos() + 2, piece.getXPos() + 2)

                if startingColor == "white":
                    yourPieceArray = theoreticalGameNode2.getWhitePieces()
                    enemyArray = theoreticalGameNode2.getBlackPieces()
                else:
                    yourPieceArray = theoreticalGameNode2.getBlackPieces()
                    enemyArray = theoreticalGameNode2.getWhitePieces() 

                score = self.generateScore(yourPieceArray, enemyArray)
                heuristic.insert(score, 2)
                availableEnemyPieces = []
                for piece in enemyArray:
                    theoreticalGameNode2.canPieceMove(piece)
                    if piece.getCanGoRight() or piece.getCanGoLeft() and not piece.getIsDead():
                        availableEnemyPieces.append(piece)

                theoreticalGameNode5 = Game()
                theoreticalGameNode5.copyGameBoard(theoreticalGameNode2.getGameBoard())
                theoreticalGameNode6 = Game()
                theoreticalGameNode6.copyGameBoard(theoreticalGameNode2.getGameBoard())

                if len(availableEnemyPieces) >= 1:
                    if len(availableEnemyPieces) == 1:
                        pieceForNodeFive = availableEnemyPieces[0]
                        pieceForNodeSix = availableEnemyPieces[0]
                    else:
                        pieceForNodeFive = availableEnemyPieces.pop()
                        pieceForNodeSix = availableEnemyPieces.pop()

                    # For node 5
                    if pieceForNodeFive.getCanGoLeft():
                        enemyArray = []
                        yourPieceArray = []
                        if piece.getCanGoUp():
                            if theoreticalGameNode5.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode5.movePiece(pieceForNodeFive, pieceForNodeFive.getYPos() - 1, pieceForNodeFive.getXPos() - 1)
                            else:
                                theoreticalGameNode5.movePiece(pieceForNodeFive, pieceForNodeFive.getYPos() - 2, pieceForNodeFive.getXPos() - 2)
                        else:
                            if theoreticalGameNode5.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode5.movePiece(pieceForNodeFive, pieceForNodeFive.getYPos() + 1, pieceForNodeFive.getXPos() - 1)
                            else:
                                theoreticalGameNode5.movePiece(pieceForNodeFive, pieceForNodeFive.getYPos() + 2, pieceForNodeFive.getXPos() - 2)

                        if startingColor == "white":
                            yourPieceArray = theoreticalGameNode5.getWhitePieces()
                            enemyArray = theoreticalGameNode5.getBlackPieces()
                        else:
                            yourPieceArray = theoreticalGameNode5.getBlackPieces()
                            enemyArray = theoreticalGameNode5.getWhitePieces() 

                        score = self.generateScore(yourPieceArray, enemyArray)
                        heuristic.insert(score, 5)
                    else:
                        enemyArray = []
                        yourPieceArray = []
                        if piece.getCanGoUp():
                            if theoreticalGameNode5.gameBoard[pieceForNodeFive.getYPos() - 1][pieceForNodeFive.getXPos() - 1] is None:
                                theoreticalGameNode5.movePiece(pieceForNodeFive, pieceForNodeFive.getYPos() - 1, pieceForNodeFive.getXPos() - 1)
                            else:
                                theoreticalGameNode5.movePiece(pieceForNodeFive, pieceForNodeFive.getYPos() - 2, pieceForNodeFive.getXPos() - 2)
                        else:
                            if theoreticalGameNode5.gameBoard[pieceForNodeFive.getYPos() + 1][pieceForNodeFive.getXPos() - 1] is None:
                                theoreticalGameNode5.movePiece(pieceForNodeFive, pieceForNodeFive.getYPos() + 1, pieceForNodeFive.getXPos() - 1)
                            else:
                                theoreticalGameNode5.movePiece(pieceForNodeFive, pieceForNodeFive.getYPos() + 2, pieceForNodeFive.getXPos() - 2)

                        if startingColor == "white":
                            yourPieceArray = theoreticalGameNode5.getWhitePieces()
                            enemyArray = theoreticalGameNode5.getBlackPieces()
                        else:
                            yourPieceArray = theoreticalGameNode5.getBlackPieces()
                            enemyArray = theoreticalGameNode5.getWhitePieces() 

                        score = self.generateScore(yourPieceArray, enemyArray)
                        heuristic.insert(score, 5)

                        # Now get the stuff for nodes 11 and 12
                        availableYourPieces = []
                        for piece in yourPieceArray:
                            theoreticalGameNode5.canPieceMove(piece)
                            if piece.getCanGoRight() or piece.getCanGoLeft() and not piece.getIsDead():
                                availableEnemyPieces.append(piece)

                        theoreticalGameNode11 = Game()
                        theoreticalGameNode11.copyGameBoard(theoreticalGameNode3.getGameBoard())
                        theoreticalGameNode12 = Game()
                        theoreticalGameNode12.copyGameBoard(theoreticalGameNode3.getGameBoard())

                        if len(availableEnemyPieces) >= 1:
                            if len(availableEnemyPieces) == 1:
                                pieceForNodeEleven = availableEnemyPieces[0]
                                pieceForNodeTwelve = availableEnemyPieces[0]
                            else:
                                pieceForNodeEleven = availableEnemyPieces.pop()
                                pieceForNodeTwelve = availableEnemyPieces.pop()

                            if pieceForNodeEleven.getCanGoLeft():
                                enemyArray = []
                                yourPieceArray = []
                                if pieceForNodeEleven.getCanGoUp():
                                    if theoreticalGameNode11.gameBoard[pieceForNodeEleven.getYPos() - 1][pieceForNodeEleven.getXPos() - 1] is None:
                                        theoreticalGameNode11.movePiece(pieceForNodeEleven, pieceForNodeEleven.getYPos() - 1, pieceForNodeEleven.getXPos() - 1)
                                    else:
                                        theoreticalGameNode11.movePiece(pieceForNodeEleven, pieceForNodeEleven.getYPos() - 2, pieceForNodeEleven.getXPos() - 2)
                                else:
                                    if theoreticalGameNode11.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode11.movePiece(pieceForNodeEleven, pieceForNodeEleven.getYPos() + 1, pieceForNodeEleven.getXPos() - 1)
                                    else:
                                        theoreticalGameNode11.movePiece(pieceForNodeEleven, pieceForNodeEleven.getYPos() + 2, pieceForNodeEleven.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode11.getWhitePieces()
                                    enemyArray = theoreticalGameNode11.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode11.getBlackPieces()
                                    enemyArray = theoreticalGameNode11.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 11)
                            else:
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode11.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode11.movePiece(pieceForNodeEleven, pieceForNodeEleven.getYPos() - 1, pieceForNodeEleven.getXPos() - 1)
                                    else:
                                        theoreticalGameNode11.movePiece(pieceForNodeEleven, pieceForNodeEleven.getYPos() - 2, pieceForNodeEleven.getXPos() - 2)
                                else:
                                    if theoreticalGameNode11.gameBoard[pieceForNodeEleven.getYPos() + 1][pieceForNodeEleven.getXPos() - 1] is None:
                                        theoreticalGameNode11.movePiece(pieceForNodeEleven, pieceForNodeEleven.getYPos() + 1, pieceForNodeEleven.getXPos() - 1)
                                    else:
                                        theoreticalGameNode11.movePiece(pieceForNodeEleven, pieceForNodeEleven.getYPos() + 2, pieceForNodeEleven.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode11.getWhitePieces()
                                    enemyArray = theoreticalGameNode11.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode11.getBlackPieces()
                                    enemyArray = theoreticalGameNode11.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 11)

                            # For node 12
                            if pieceForNodeTwelve.getCanGoLeft():
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode12.gameBoard[pieceForNodeTwelve.getYPos() - 1][pieceForNodeTwelve.getXPos() - 1] is None:
                                        theoreticalGameNode12.movePiece(pieceForNodeTwelve, piece.getYPos() - 1, pieceForNodeTwelve.getXPos() - 1)
                                    else:
                                        theoreticalGameNode12.movePiece(pieceForNodeTwelve, pieceForNodeTwelve.getYPos() - 2, pieceForNodeTwelve.getXPos() - 2)
                                else:
                                    if theoreticalGameNode12.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode12.movePiece(pieceForNodeTwelve, pieceForNodeTwelve.getYPos() + 1, pieceForNodeTwelve.getXPos() - 1)
                                    else:
                                        theoreticalGameNode12.movePiece(pieceForNodeTwelve, pieceForNodeTwelve.getYPos() + 2, pieceForNodeTwelve.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode12.getWhitePieces()
                                    enemyArray = theoreticalGameNode12.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode12.getBlackPieces()
                                    enemyArray = theoreticalGameNode12.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 12)
                            else:
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode12.gameBoard[pieceForNodeTwelve.getYPos() - 1][pieceForNodeTwelve.getXPos() - 1] is None:
                                        theoreticalGameNode12.movePiece(pieceForNodeTwelve, pieceForNodeTwelve.getYPos() - 1, pieceForNodeTwelve.getXPos() - 1)
                                    else:
                                        theoreticalGameNode12.movePiece(pieceForNodeTwelve, pieceForNodeTwelve.getYPos() - 2, pieceForNodeTwelve.getXPos() - 2)
                                else:
                                    if theoreticalGameNode12.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode12.movePiece(pieceForNodeTwelve, pieceForNodeTwelve.getYPos() + 1, pieceForNodeTwelve.getXPos() - 1)
                                    else:
                                        theoreticalGameNode12.movePiece(pieceForNodeTwelve, pieceForNodeTwelve.getYPos() + 2, pieceForNodeTwelve.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode12.getWhitePieces()
                                    enemyArray = theoreticalGameNode12.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode12.getBlackPieces()
                                    enemyArray = theoreticalGameNode12.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 12)


                    # For node 6
                    if pieceForNodeSix.getCanGoLeft():
                        enemyArray = []
                        yourPieceArray = []
                        if piece.getCanGoUp():
                            if theoreticalGameNode6.gameBoard[pieceForNodeSix.getYPos() - 1][pieceForNodeSix.getXPos() - 1] is None:
                                theoreticalGameNode6.movePiece(pieceForNodeSix, pieceForNodeSix.getYPos() - 1, pieceForNodeSix.getXPos() - 1)
                            else:
                                theoreticalGameNode6.movePiece(pieceForNodeSix, pieceForNodeSix.getYPos() - 2, pieceForNodeSix.getXPos() - 2)
                        else:
                            if theoreticalGameNode6.gameBoard[pieceForNodeSix.getYPos() + 1][pieceForNodeSix.getXPos() - 1] is None:
                                theoreticalGameNode6.movePiece(pieceForNodeSix, pieceForNodeSix.getYPos() + 1, pieceForNodeSix.getXPos() - 1)
                            else:
                                theoreticalGameNode6.movePiece(pieceForNodeSix, pieceForNodeSix.getYPos() + 2, pieceForNodeSix.getXPos() - 2)

                        if startingColor == "white":
                            yourPieceArray = theoreticalGameNode6.getWhitePieces()
                            enemyArray = theoreticalGameNode6.getBlackPieces()
                        else:
                            yourPieceArray = theoreticalGameNode6.getBlackPieces()
                            enemyArray = theoreticalGameNode6.getWhitePieces() 

                        score = self.generateScore(yourPieceArray, enemyArray)
                        heuristic.insert(score, 6)
                    else:
                        enemyArray = []
                        yourPieceArray = []
                        if piece.getCanGoUp():
                            if theoreticalGameNode6.gameBoard[pieceForNodeSix.getYPos() - 1][pieceForNodeSix.getXPos() - 1] is None:
                                theoreticalGameNode6.movePiece(pieceForNodeSix, pieceForNodeSix.getYPos() - 1, pieceForNodeSix.getXPos() - 1)
                            else:
                                theoreticalGameNode6.movePiece(pieceForNodeSix, pieceForNodeSix.getYPos() - 2, pieceForNodeSix.getXPos() - 2)
                        else:
                            if theoreticalGameNode6.gameBoard[pieceForNodeSix.getYPos() + 1][pieceForNodeSix.getXPos() - 1] is None:
                                theoreticalGameNode6.movePiece(pieceForNodeSix, pieceForNodeSix.getYPos() + 1, pieceForNodeSix.getXPos() - 1)
                            else:
                                theoreticalGameNode6.movePiece(pieceForNodeSix, pieceForNodeSix.getYPos() + 2, pieceForNodeSix.getXPos() - 2)

                        if startingColor == "white":
                            yourPieceArray = theoreticalGameNode6.getWhitePieces()
                            enemyArray = theoreticalGameNode6.getBlackPieces()
                        else:
                            yourPieceArray = theoreticalGameNode6.getBlackPieces()
                            enemyArray = theoreticalGameNode6.getWhitePieces() 

                        score = self.generateScore(yourPieceArray, enemyArray)
                        heuristic.insert(score, 6)

                        # Now get the stuff for nodes 13 and 14
                        availableYourPieces = []
                        for piece in yourPieceArray:
                            theoreticalGameNode6.canPieceMove(piece)
                            if piece.getCanGoRight() or piece.getCanGoLeft() and not piece.getIsDead():
                                availableEnemyPieces.append(piece)

                        theoreticalGameNode13 = Game()
                        theoreticalGameNode13.copyGameBoard(theoreticalGameNode3.getGameBoard())
                        theoreticalGameNode14 = Game()
                        theoreticalGameNode14.copyGameBoard(theoreticalGameNode3.getGameBoard())

                        if len(availableEnemyPieces) >= 1:
                            if len(availableEnemyPieces) == 1:
                                pieceForNodeThirteen = availableEnemyPieces[0]
                                pieceForNodeFourteen = availableEnemyPieces[0]
                            else:
                                pieceForNodeThirteen = availableEnemyPieces.pop()
                                pieceForNodeFourteen = availableEnemyPieces.pop()

                            if pieceForNodeThirteen.getCanGoLeft():
                                enemyArray = []
                                yourPieceArray = []
                                if pieceForNodeThirteen.getCanGoUp():
                                    if theoreticalGameNode13.gameBoard[pieceForNodeThirteen.getYPos() - 1][pieceForNodeThirteen.getXPos() - 1] is None:
                                        theoreticalGameNode13.movePiece(pieceForNodeThirteen, pieceForNodeThirteen.getYPos() - 1, pieceForNodeThirteen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode13.movePiece(pieceForNodeThirteen, pieceForNodeThirteen.getYPos() - 2, pieceForNodeThirteen.getXPos() - 2)
                                else:
                                    if theoreticalGameNode13.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode13.movePiece(pieceForNodeThirteen, pieceForNodeThirteen.getYPos() + 1, pieceForNodeThirteen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode13.movePiece(pieceForNodeThirteen, pieceForNodeThirteen.getYPos() + 2, pieceForNodeThirteen.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode13.getWhitePieces()
                                    enemyArray = theoreticalGameNode13.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode13.getBlackPieces()
                                    enemyArray = theoreticalGameNode13.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 13)
                            else:
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode13.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode13.movePiece(pieceForNodeThirteen, pieceForNodeThirteen.getYPos() - 1, pieceForNodeThirteen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode13.movePiece(pieceForNodeThirteen, pieceForNodeThirteen.getYPos() - 2, pieceForNodeThirteen.getXPos() - 2)
                                else:
                                    if theoreticalGameNode13.gameBoard[pieceForNodeThirteen.getYPos() + 1][pieceForNodeThirteen.getXPos() - 1] is None:
                                        theoreticalGameNode13.movePiece(pieceForNodeThirteen, pieceForNodeThirteen.getYPos() + 1, pieceForNodeThirteen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode13.movePiece(pieceForNodeThirteen, pieceForNodeThirteen.getYPos() + 2, pieceForNodeThirteen.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode13.getWhitePieces()
                                    enemyArray = theoreticalGameNode13.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode13.getBlackPieces()
                                    enemyArray = theoreticalGameNode13.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 13)

                            # For node 14
                            if pieceForNodeFourteen.getCanGoLeft():
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode14.gameBoard[pieceForNodeFourteen.getYPos() - 1][pieceForNodeFourteen.getXPos() - 1] is None:
                                        theoreticalGameNode14.movePiece(pieceForNodeFourteen, piece.getYPos() - 1, pieceForNodeFourteen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode14.movePiece(pieceForNodeFourteen, pieceForNodeFourteen.getYPos() - 2, pieceForNodeFourteen.getXPos() - 2)
                                else:
                                    if theoreticalGameNode14.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode14.movePiece(pieceForNodeFourteen, pieceForNodeFourteen.getYPos() + 1, pieceForNodeFourteen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode14.movePiece(pieceForNodeFourteen, pieceForNodeFourteen.getYPos() + 2, pieceForNodeFourteen.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode14.getWhitePieces()
                                    enemyArray = theoreticalGameNode14.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode14.getBlackPieces()
                                    enemyArray = theoreticalGameNode14.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 14)
                            else:
                                enemyArray = []
                                yourPieceArray = []
                                if piece.getCanGoUp():
                                    if theoreticalGameNode14.gameBoard[pieceForNodeFourteen.getYPos() - 1][pieceForNodeFourteen.getXPos() - 1] is None:
                                        theoreticalGameNode14.movePiece(pieceForNodeFourteen, pieceForNodeFourteen.getYPos() - 1, pieceForNodeFourteen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode14.movePiece(pieceForNodeFourteen, pieceForNodeFourteen.getYPos() - 2, pieceForNodeFourteen.getXPos() - 2)
                                else:
                                    if theoreticalGameNode14.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                        theoreticalGameNode14.movePiece(pieceForNodeFourteen, pieceForNodeFourteen.getYPos() + 1, pieceForNodeFourteen.getXPos() - 1)
                                    else:
                                        theoreticalGameNode14.movePiece(pieceForNodeFourteen, pieceForNodeFourteen.getYPos() + 2, pieceForNodeFourteen.getXPos() - 2)

                                if startingColor == "white":
                                    yourPieceArray = theoreticalGameNode14.getWhitePieces()
                                    enemyArray = theoreticalGameNode14.getBlackPieces()
                                else:
                                    yourPieceArray = theoreticalGameNode14.getBlackPieces()
                                    enemyArray = theoreticalGameNode14.getWhitePieces() 

                                score = self.generateScore(yourPieceArray, enemyArray)
                                heuristic.insert(score, 14)
                else:
                    pass
            heuristicWrapper = MinimaxWrapper(piece, piece.getColor(), heuristic.canGoLeft(), heuristic.miniMax())
            heuristicArray.append(heuristicWrapper)


        heuristicArray.sort(key=lambda x: x.minimaxScore, reverse=True)
        wrapperToUse = heuristicArray[0]
        pieceToUse = wrapperToUse.getPiece()
        goLeft = wrapperToUse.getIsLeft()
        if goLeft:
        	if self.gameBoard[pieceToUse.getYPos() - 1][pieceToUse.getXPos() - 1] is None:
   	           	self.movePiece(pieceToUse, piece.getYPos() - 1, pieceToUse.getXPos() - 1)
 			else:
             	self.movePiece(pieceToUse, pieceToUse.getYPos() - 2, pieceToUse.getXPos() - 2)
       	else:
           	if self.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
            	self.movePiece(pieceToUse, pieceToUse.getYPos() + 1, pieceToUse.getXPos() - 1)
           	else:
          		self.movePiece(pieceToUse, pieceToUse.getYPos() + 2, pieceToUse.getXPos() - 2)
