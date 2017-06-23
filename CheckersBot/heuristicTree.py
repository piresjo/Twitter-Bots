from checkerGame import *
from piece import *

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

    def canGoLeft(self):
        return self.root.canGoLeft()


class Node(object):
    ''' A Node of the HeuristicTree.
    '''
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def canGoLeft(self):
        if self is None:
            return False
        if self.left is not None and self.right is None:
            return True
        if self.left is None and self.right is not None:
            return False
        if self.left is not None and self.right is not None:
            return False
        if self.left.val >= self.right.val:
            return True
        return False

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