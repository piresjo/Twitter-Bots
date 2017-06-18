class Piece(object):
	def __init__(self, color, xPos, yPos):
      self.color = color
      self.xPos = xPos
      self.yPos = yPos
      self.isKing = False
      self.isDead = False

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

class HeuristicTree(object):
    ''' Tree of all possible moves. For ease, 
    	this will be done like a BST (that way,
    	for minimax, I can go right on the max move
    	and left on the min move)
    	BST generation is n*lg(n)
    	But we are generating this frequently
    	But since there will at most 50 moves
    	(Checkers draws after 50 moves),
    	and since we'll need at most 12 trees per
    	turn (if even that),
    	Big O effeciciency won't matter much
    '''
    def __init__(self):
        self.root = None
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
        nodeA = self.root
        while nodeA is not None:
            if element == nodeA.val:
                return True
            elif element < nodeA.val:
                nodeA = nodeA.left
            else:
                nodeA = nodeA.right
        return False

    def insert(self, element):
        ''' 
        	Insert a given value into the tree.
        	Left subtree should contain all elements <= to the current element.
        	Right subtree will contain all elements > the current element.
        '''
        self.size += 1
        newNode = Node(element)
        if self.root is None:
            self.root = newNode
        else:
            nodeA = self.root
            while True:
                if element <= nodeA.val:
                    if nodeA.left is None:
                        nodeA.left = newNode
                        self.left = newNode
                        newNode.parent = nodeA
                        break
                    nodeA = nodeA.left
                else:
                    if nodeA.right is None:
                        nodeA.right = newNode
                        self.right = newNode
                        newNode.parent = nodeA
                        break
                    nodeA = nodeA.right
        return newNode

    def elements(self):
        ''' Return a list of the elements visited in an inorder traversal:
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

    def elements(self):
        if self is None:
            return []
        if self.left is not None and self.right is not None:
            return self.left.elements() + [self.val] + self.right.elements()
        if self.left is None and self.right is not None:
            return [self.val] + self.right.elements()
        if self.left is not None and self.right is None:
            return self.left.elements() + [self.val]
        if self.left is None and self.right is None:
            return [self.val]

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
            return self.left.toString() + str(self.val)
        if self.left is None and self.right is None:
            return '(_ ' + str(self.val) + ' _)'

    def miniMax(self, layerOn):
    	if self is None:
    		return 0
    	if self.left is None and self.right is not None:
    		return self.val + miniMax(self.right, layerOn + 1)
    	if self.left is not None and self.right is None:
    		return self.val + miniMax(self.left, layerOn + 1)
    	if self.left is not None and self.right is not None:
    		if (layerOn % 2 == 0):
    			return self.val + miniMax(self.right, layerOn + 1)
    		else:
    			return self.val + miniMax(self.left, layerOn + 1)
    	if self.left is None and self.right is None:
    		return self.val


   