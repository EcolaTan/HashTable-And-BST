from nodeClass import node

# create a subclass of node with additional properties for a bst node
class Node(node):
    def __init__(self,kmer,frequency = 1):
        # call parent class constructor to inherit attributes
        super().__init__(kmer,frequency)
        self.left = None
        self.right = None
        self.height = 1

# avl tree class
class AVL():
    # the root start as none since tree will be empty when constructed
    def __init__(self):
        self.__root = None

    # the search is based on the string
    def search(self, root, kmer):
        # if it is found or none stop the search
        if (root is None or root.kmer == kmer):
            return root
        # if kmer string is less check left else right
        if (kmer < root.kmer):
            return self.search(root.left, kmer)
        return self.search(root.right, kmer)
    
    # a function to call search and print its output
    def printSearchResult(self, root, kmer):
        result = self.search(root,kmer)
        if(result != None):
            print("Found " + result.kmer + " it has a frequency of " + str(result.frequency))
        else:
            print(kmer + " is not found in the tree")

    # delete all the nodes in the tree
    def deleteNodes(self, root):
        if root is not None:
            self.deleteNodes(root.left)
            self.deleteNodes(root.right)
            root.left = None
            root.right = None

    # delete all nodes then set root to none to clear the tree
    def deleteTree(self,root):
        self.deleteNodes(root)
        self.__root = None

    # calculate the individual height of the tree
    def nodeHeight(self, root):
        if not root:
            return 0
        return root.height

    # compute if the tree is balance or side heavy
    def getThreshHold(self, root):
        if not root:
            return 0
        return self.nodeHeight(root.left) - self.nodeHeight(root.right)


    # rotates imbalance nodes 
    def leftRotate(self, node):
        
        rightChild = node.right
        leftGrandChild = rightChild.left
        
        rightChild.left = node
        node.right = leftGrandChild

        node.height = 1 + max(self.nodeHeight(node.left),self.nodeHeight(node.right))
        rightChild.height = 1 + max(self.nodeHeight(rightChild.left),self.nodeHeight(rightChild.right))
 
        return rightChild
 
    def rightRotate(self, node):
 
        leftChild = node.left
        rightGrandChild = leftChild.right
 
        leftChild.right = node
        node.left = rightGrandChild

        node.height = 1 + max(self.nodeHeight(node.left),self.nodeHeight(node.right))
        leftChild.height = 1 + max(self.nodeHeight(leftChild.left),self.nodeHeight(leftChild.right))
 
        return leftChild

    # insert node which upholds an avl tree
    def balancedInsertion(self, root, node):

        # normal bst insertion
        if not root:
            return node
        elif node.kmer < root.kmer:
            root.left = self.balancedInsertion(root.left, node)
        else:
            root.right = self.balancedInsertion(root.right, node)

        # update height of the node 
        root.height = 1 + max(self.nodeHeight(root.left),self.nodeHeight(root.right))

        # compute threshold
        threshold = self.getThreshHold(root)

        # left heavy
        #  left child has a left child
        if threshold > 1 and node.kmer < root.left.kmer:
            return self.rightRotate(root)
    
        # left child has a right child
        if threshold < -1 and node.kmer > root.right.kmer:
            return self.leftRotate(root)
 
        # right heavy
        # right child has a right child
        if threshold > 1 and node.kmer > root.left.kmer:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        # right child has a left child
        if threshold < -1 and node.kmer < root.right.kmer:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    # update root node with insertion 
    def insert(self,root,node):
        searchedNode = self.search(root, node.kmer)
        if(searchedNode != None):
            searchedNode.frequency += 1
        else:
            self.__root = self.balancedInsertion(root,node)
        
    # getter for root
    def getRoot(self):
        return self.__root

    # print tree inorder travesal
    def printInorder(self,root):
        if(root):
            self.printInorder(root.left)
            print(root.kmer,root.frequency)
            self.printInorder(root.right)
