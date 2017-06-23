class MinimaxWrapper(object):
    def __init__(self, color, isLeft, minimaxScore):
        self.color = color
        self.isLeft = isLeft
        self.minimaxScore = minimaxScore

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

class HeuristicTree(object):
    '''
    Edit - Been thinking about how minimax would
    work. I'll have to edit the structure of the tree
    so it's behaves better with the move-based layering
    of the tree. So, no BST :(

    Also, I'd like to eventually make every other layer a variable-sized array of nodes, so
    that I can account for all moves by all available enemy pieces (right now, I'll just take)
    '''
    def __init__(self):
        self.root = Node(0)
        self.size = 0
        self.left = None
        self.right = None

    def __str__(self):
        ''' Return a representation of the tree as (left, elem, right)
        '''
        return self.root.toString()

    def __len__(self):
        ''' Returns the number of nodes in the tree.'''
        return self.root.length()

    def __contains__(self, element):
        ''' Finds whether a given element is in the tree.
        Returns True if the element is found, else returns False.
        '''
        return self.root.find(element)

    ''' 
        Insert a given value into the tree.
        Left subtree should contain left moves.
        Right subtree will contain all right moves.
        To make things easier on me, and since I only
        want the AI to be at most 3 steps ahead, I'll
        stop after three layers
    '''
    '''
    Tree Numbering:
    0                       0
    1               1               2      
    2          3        4      5         6
    3       7     8   9   10 11 12     13  14
    '''
    def insert(self, element, moveNumber):
    
        self.root.insert(element, moveNumber)

    def elements(self):
        ''' Return a list of the elements visited in a level order traversal:
        '''
        return self.root.elements()

    def miniMax(self):
        '''Determine the minimax score for an available checkers piece'''
        return self.root.miniMax(0)


class Node(object):
    ''' A Node of the HeuristicTree.
    '''
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def insert(self, element, moveNumber):
        '''
        Given the nature of the tree, we're doing this linearly...
        eww...there has to be a better way to do this
        '''
        '''
        Tree Numbering:
        0                       0
        1               1               2      
        2          3        4      5         6
        3       7     8   9   10 11 12     13  14
        '''
        if moveNumber > 14:
            raise ValueError("Value Too Big")

        if moveNumber == 0:
            raise ValueError("Heuristic Trees Always Have A Root Of 0")

        addNode = Node(element)
        if moveNumber == 1:
            if self.left is not None:
                raise ValueError("Position Already Filled")
            else:
                self.left = addNode
                return

        if moveNumber == 2:
            if self.right is not None:
                raise ValueError("Position Already Filled")
            else:
                self.right = addNode
                return

        if moveNumber == 3 or \
        moveNumber == 4 or \
        moveNumber == 7 or \
        moveNumber == 8 or \
        moveNumber == 9 or \
        moveNumber == 10:
            nextNode = self.left
        else:
            nextNode = self.right

        if nextNode is None:
            raise ValueError("Need a prior node")

        if moveNumber == 3 or moveNumber == 5:
            if nextNode.left is not None:
                raise ValueError("Position Already Filled")
            else:
                nextNode.left = addNode
                return

        if moveNumber == 4 or moveNumber == 6:
            if nextNode.right is not None:
                raise ValueError("Position Already Filled")
            else:
                nextNode.right = addNode
                return

        if moveNumber == 3 or \
        moveNumber == 7 or \
        moveNumber == 8 or \
        moveNumber == 5 or \
        moveNumber == 11 or \
        moveNumber == 12:
            nextNode = nextNode.left
        else:
            nextNode = nextNode.right

        if nextNode is None:
            raise ValueError("Need a prior node")

        if moveNumber == 7 or moveNumber == 9 or moveNumber == 11 or moveNumber == 13:
            if nextNode.left is not None:
                raise ValueError("Position Already Filled")
            else:
                nextNode.left = addNode
                return

        if moveNumber == 8 or moveNumber == 10 or moveNumber == 12 or moveNumber == 14:
            if nextNode.right is not None:
                raise ValueError("Position Already Filled")
            else:
                nextNode.right = addNode
                return

    def find(self, valToFind):
        if self is None:
            return False
        if self.left is not None and self.right is not None:
            return (self.val == valToFind) or self.left.find(valToFind) or self.right.find(valToFind)
        if self.left is None and self.right is not None:
            return (self.val == valToFind) or self.right.find(valToFind)
        if self.left is not None and self.right is None:
            return (self.val == valToFind) or self.left.find(valToFind)
        if self.left is None and self.right is None:
            return (self.val == valToFind)


    def elements(self):
        if self is None:
            return []

        returnVal = []
        queue = []
        queue.append(self)
        while len(queue) > 0:
            returnVal.append(queue[0].val)
            node = queue.pop(0)

            #Enqueue left child
            if node.left is not None:
                queue.append(node.left)
 
            # Enqueue right child
            if node.right is not None:
                queue.append(node.right)
        return returnVal

    def length(self):
        if self is None:
            return 0
        if self.left is not None and self.right is not None:
            return self.left.length() + 1 + self.right.length()
        if self.left is None and self.right is not None:
            return 1 + self.right.length()
        if self.left is not None and self.right is None:
            return self.left.length() + 1
        if self.left is None and self.right is None:
            return 1

    def toString(self):
        if self.left is not None and self.right is not None:
            return "(" + self.left.toString() + " " + str(self.val) + " " + self.right.toString() + ")"
        if self.left is None and self.right is not None:
            return "(_ " + str(self.val) + " " + self.right.toString() + ")"
        if self.left is not None and self.right is None:
            return "(" + self.left.toString() + " " + str(self.val) + " _)"
        if self.left is None and self.right is None:
            return '(_ ' + str(self.val) + ' _)'

    def miniMax(self, layerOn):
        if self is None:
            return 0
        if self.left is None and self.right is not None:
            return self.val + self.right.miniMax(layerOn + 1)
        if self.left is not None and self.right is None:
            return self.val + self.left.miniMax(layerOn + 1)
        if self.left is not None and self.right is not None:
            if (layerOn % 2 == 0):
                leftVal = self.left.val
                rightVal = self.right.val
                if (leftVal >= rightVal):
                    return self.val + self.left.miniMax(layerOn + 1)
                else:
                    return self.val + self.right.miniMax(layerOn + 1)
            else:
                leftVal = self.left.val
                rightVal = self.right.val
                if (leftVal < rightVal):
                    return self.val + self.left.miniMax(layerOn + 1)
                else:
                    return self.val + self.right.miniMax(layerOn + 1)
        if self.left is None and self.right is None:
            return self.val

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
                    if piece.getCanGoLeft():
                        enemyArray = []
                        yourPieceArray = []
                        if piece.getCanGoUp():
                            if self.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                        else:
                            if self.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
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
                            if self.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode3.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                        else:
                            if self.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
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


                    # For node 4
                    if piece.getCanGoLeft():
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
                    if piece.getCanGoLeft():
                        enemyArray = []
                        yourPieceArray = []
                        if piece.getCanGoUp():
                            if self.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode5.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode5.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                        else:
                            if self.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode5.movePiece(piece, piece.getYPos() + 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode5.movePiece(piece, piece.getYPos() + 2, piece.getXPos() - 2)

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
                            if self.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode5.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode5.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                        else:
                            if self.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode5.movePiece(piece, piece.getYPos() + 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode5.movePiece(piece, piece.getYPos() + 2, piece.getXPos() - 2)

                        if startingColor == "white":
                            yourPieceArray = theoreticalGameNode5.getWhitePieces()
                            enemyArray = theoreticalGameNode5.getBlackPieces()
                        else:
                            yourPieceArray = theoreticalGameNode5.getBlackPieces()
                            enemyArray = theoreticalGameNode5.getWhitePieces() 

                        score = self.generateScore(yourPieceArray, enemyArray)
                        heuristic.insert(score, 5)


                    # For node 6
                    if piece.getCanGoLeft():
                        enemyArray = []
                        yourPieceArray = []
                        if piece.getCanGoUp():
                            if self.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode6.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode6.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                        else:
                            if self.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode6.movePiece(piece, piece.getYPos() + 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode6.movePiece(piece, piece.getYPos() + 2, piece.getXPos() - 2)

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
                            if self.gameBoard[piece.getYPos() - 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode6.movePiece(piece, piece.getYPos() - 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode6.movePiece(piece, piece.getYPos() - 2, piece.getXPos() - 2)
                        else:
                            if self.gameBoard[piece.getYPos() + 1][piece.getXPos() - 1] is None:
                                theoreticalGameNode6.movePiece(piece, piece.getYPos() + 1, piece.getXPos() - 1)
                            else:
                                theoreticalGameNode6.movePiece(piece, piece.getYPos() + 2, piece.getXPos() - 2)

                        if startingColor == "white":
                            yourPieceArray = theoreticalGameNode6.getWhitePieces()
                            enemyArray = theoreticalGameNode6.getBlackPieces()
                        else:
                            yourPieceArray = theoreticalGameNode6.getBlackPieces()
                            enemyArray = theoreticalGameNode6.getWhitePieces() 

                        score = self.generateScore(yourPieceArray, enemyArray)
                        heuristic.insert(score, 6)
                else:
                    pass


        heuristicArray.sort(key=lambda x: x.minimaxScore, reverse=True)




    


