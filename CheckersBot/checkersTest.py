import unittest
from checkers import *


class TestCheckers(unittest.TestCase):

    def setUp(self):
        pass

    def testPieces(self):
        blackPiece = Piece("black", 6, 6)
        whitePiece = Piece("white", 6, 6)
        self.assertEqual("black", blackPiece.getColor())
        self.assertEqual("white", whitePiece.getColor())
        self.assertEqual(6, blackPiece.getXPos())
        self.assertEqual(6, blackPiece.getYPos())
        self.assertEqual(False, blackPiece.getIsKing())
        self.assertEqual(False, blackPiece.getIsDead())
        whitePiece.newPosition(2, 2)
        self.assertEqual(2, whitePiece.getXPos())
        self.assertEqual(2, whitePiece.getYPos())
        blackPiece.becomeKing()
        blackPiece.becomeDead()
        self.assertEqual(True, blackPiece.getIsKing())
        self.assertEqual(True, blackPiece.getIsDead())
        self.assertEqual(True, blackPiece.getCanGoUp())
        self.assertEqual(False, whitePiece.getCanGoUp())
        whitePiece.setCanGoUp()
        self.assertEqual(True, whitePiece.getCanGoUp())
        self.assertEqual(False, blackPiece.getCanGoLeft())
        self.assertEqual(False, blackPiece.getCanGoRight())
        blackPiece.setCanGoRight(True)
        blackPiece.setCanGoLeft(True)
        self.assertEqual(True, blackPiece.getCanGoRight())
        self.assertEqual(True, blackPiece.getCanGoLeft())


    def testTree(self):
        tree = HeuristicTree()
        self.assertEqual(tree.miniMax(), 0)
        tree.insert(11, 1)
        self.assertEqual(tree.miniMax(), 11)
        self.assertEqual(str(tree), '((_ 11 _) 0 _)')
        tree.insert(7, 3)
        tree.insert(12, 8)
        self.assertEqual(tree.miniMax(), 30)
        self.assertEqual(str(tree), '(((_ 7 (_ 12 _)) 11 _) 0 _)')
        self.assertEqual(tree.elements(), [0, 11, 7, 12])
        tree.insert(16, 2)
        tree.insert(9, 5)
        tree.insert(10, 6)
        self.assertEqual(str(tree), '(((_ 7 (_ 12 _)) 11 _) 0 ((_ 9 _) 16 (_ 10 _)))')
        self.assertEqual(tree.elements(), [0, 11, 16, 7, 9, 10, 12])
        self.assertEqual(1 in tree, False)
        self.assertEqual(9 in tree, True)
        self.assertEqual(len(tree), 7)
        self.assertEqual(tree.miniMax(), 25)

    def testGame(self):
        testGame = Game()
        testGame.generateGameBoard()
        testString = "w.w.w.w.\n.w.w.w.w\nw.w.w.w.\n........\n........\nb.b.b.b.\n.b.b.b.b\nb.b.b.b.\nBlack:12 White:12 T:Black"
        self.assertEqual(testString, testGame.drawBoard())
        testStringWhiteStatus = "White:\n1- (0,0)\n2- (2,0)\n3- (4,0)\n4- (6,0)\n5- (1,1)\n6- (3,1)\n7- (5,1)\n8- (7,1)\n9- (0,2)\n10- (2,2)\n11- (4,2)\n12- (6,2)\n";
        testStringBlackStatus = "Black:\n1- (0,5)\n2- (2,5)\n3- (4,5)\n4- (6,5)\n5- (1,6)\n6- (3,6)\n7- (5,6)\n8- (7,6)\n9- (0,7)\n10- (2,7)\n11- (4,7)\n12- (6,7)\n";
        self.assertEqual(testGame.drawColorStatus("black"), testStringBlackStatus)
        self.assertEqual(testGame.drawColorStatus("white"), testStringWhiteStatus)
        testGame.kingPiece("black", 0, 5)
        testStringBlackKing = "Black:\n1- (0,5)K\n2- (2,5)\n3- (4,5)\n4- (6,5)\n5- (1,6)\n6- (3,6)\n7- (5,6)\n8- (7,6)\n9- (0,7)\n10- (2,7)\n11- (4,7)\n12- (6,7)\n";
        self.assertEqual(testGame.drawColorStatus("black"), testStringBlackKing)
        testStringKing = "w.w.w.w.\n.w.w.w.w\nw.w.w.w.\n........\n........\nB.b.b.b.\n.b.b.b.b\nb.b.b.b.\nBlack:12 White:12 T:Black"
        self.assertEqual(testGame.drawBoard(), testStringKing)
        testGame.killPiece("black", 0, 5)
        testStringBlackDead = "Black:\n1- DEAD\n2- (2,5)\n3- (4,5)\n4- (6,5)\n5- (1,6)\n6- (3,6)\n7- (5,6)\n8- (7,6)\n9- (0,7)\n10- (2,7)\n11- (4,7)\n12- (6,7)\n";
        self.assertEqual(testGame.drawColorStatus("black"), testStringBlackDead)
        testStringDead = "w.w.w.w.\n.w.w.w.w\nw.w.w.w.\n........\n........\n..b.b.b.\n.b.b.b.b\nb.b.b.b.\nBlack:11 White:12 T:Black"
        self.assertEqual(testGame.drawBoard(), testStringDead)

        testGame = Game()
        testGame.generateGameBoard()
        whitePieceArray = testGame.getWhitePieces()
        blackPieceArray = testGame.getBlackPieces()
        for piece in whitePieceArray:
            testGame.canPieceMove(piece)

        for piece in blackPieceArray:
            testGame.canPieceMove(piece)

        # The last four in the whites can move
        testWhiteA = whitePieceArray[8]
        testWhiteB = whitePieceArray[9]
        testWhiteC = whitePieceArray[10]
        testWhiteD = whitePieceArray[11]
        self.assertEqual(False, testWhiteA.getCanGoLeft())
        self.assertEqual(True, testWhiteA.getCanGoRight())
        self.assertEqual(True, testWhiteB.getCanGoLeft())
        self.assertEqual(True, testWhiteB.getCanGoRight())
        self.assertEqual(True, testWhiteC.getCanGoLeft())
        self.assertEqual(True, testWhiteC.getCanGoRight())
        self.assertEqual(True, testWhiteD.getCanGoLeft())
        self.assertEqual(True, testWhiteD.getCanGoRight())


        # The first four in the blacks can move
        testBlackA = blackPieceArray[0]
        testBlackB = blackPieceArray[1]
        testBlackC = blackPieceArray[2]
        testBlackD = blackPieceArray[3]
        self.assertEqual(False, testBlackA.getCanGoLeft())
        self.assertEqual(True, testBlackA.getCanGoRight())
        self.assertEqual(True, testBlackB.getCanGoLeft())
        self.assertEqual(True, testBlackB.getCanGoRight())
        self.assertEqual(True, testBlackC.getCanGoLeft())
        self.assertEqual(True, testBlackC.getCanGoRight())
        self.assertEqual(True, testBlackD.getCanGoLeft())
        self.assertEqual(True, testBlackD.getCanGoRight())

    def testMovePieces(self):
        testGame = Game()
        testGame.generateGameBoard()
        pieceVal = testGame.getWhitePieces()[9]
        testGame.movePiece(testGame.getWhitePieces()[9], 3, 3)
        whitePieceArray = testGame.getWhitePieces()
        self.assertEqual(0, whitePieceArray[0].getXPos())
        self.assertEqual(0, whitePieceArray[0].getYPos())
        self.assertEqual(2, whitePieceArray[1].getXPos())
        self.assertEqual(0, whitePieceArray[1].getYPos())
        self.assertEqual(4, whitePieceArray[2].getXPos())
        self.assertEqual(0, whitePieceArray[2].getYPos())
        self.assertEqual(6, whitePieceArray[3].getXPos())
        self.assertEqual(0, whitePieceArray[3].getYPos())
        self.assertEqual(1, whitePieceArray[4].getXPos())
        self.assertEqual(1, whitePieceArray[4].getYPos())
        self.assertEqual(3, whitePieceArray[5].getXPos())
        self.assertEqual(1, whitePieceArray[5].getYPos())
        self.assertEqual(5, whitePieceArray[6].getXPos())
        self.assertEqual(1, whitePieceArray[6].getYPos())
        self.assertEqual(7, whitePieceArray[7].getXPos())
        self.assertEqual(1, whitePieceArray[7].getYPos())
        self.assertEqual(0, whitePieceArray[8].getXPos())
        self.assertEqual(2, whitePieceArray[8].getYPos())
        self.assertEqual(3, whitePieceArray[9].getXPos())
        self.assertEqual(3, whitePieceArray[9].getYPos())
        self.assertEqual(4, whitePieceArray[10].getXPos())
        self.assertEqual(2, whitePieceArray[10].getYPos())
        self.assertEqual(6, whitePieceArray[11].getXPos())
        self.assertEqual(2, whitePieceArray[11].getYPos())
        testStringMove = "w.w.w.w.\n.w.w.w.w\nw...w.w.\n...w....\n........\nb.b.b.b.\n.b.b.b.b\nb.b.b.b.\nBlack:12 White:12 T:Black"
        self.assertEqual(testStringMove, testGame.drawBoard())

def main():
    unittest.main()

if __name__ == '__main__':
    main()
