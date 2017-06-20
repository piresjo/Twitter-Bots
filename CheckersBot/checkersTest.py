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

    # This is all for a BST
    # I'll need to change these test cases
    def testTree(self):
        tree = HeuristicTree()
        tree.insert(11, 1)
        self.assertEqual(str(tree), '((_ 11 _) 0 _)')
        tree.insert(7, 3)
        tree.insert(12, 8)
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

    def testGame(self):
        testGame = Game()
        testGame.generateGameBoard()
        testString = "w.w.w.w.\n.w.w.w.w\nw.w.w.w.\n........\n........\nb.b.b.b.\n.b.b.b.b\nb.b.b.b."
        self.assertEqual(testString, testGame.draw())

def main():
    unittest.main()

if __name__ == '__main__':
    main()