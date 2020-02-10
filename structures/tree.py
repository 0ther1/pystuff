class BinNode():
    """Binary tree node."""
    def __init__(self, data, left: BinNode=None, right: BinNode=None, parent: BinNode=None):
        """Create a new BinNode object.
        data - data stored in this node,
        [left] - left child of this node,
        [right] - right child of this node,
        [parent] - parent of this node."""
        self.data = data
        if (left and not isinstance(left, BinNode)):
            raise TypeError("`left` must be a BinNode object!")
        if (right and not isinstance(right, BinNode)):
            raise TypeError("`right` must be a BinNode object!")
        if (parent and not isinstance(parent, BinNode)):
            raise TypeError("`parent` must be a BinNode object!")        
        self._left = left
        self._right = right
        self._parent = parent
        
    @property
    def left(self):
        """Get left child node."""
        return self._left
    
    @property
    def right(self):
        """Get right child node."""
        return self._right
    
    @property
    def parent(self):
        """Get parent node."""
        return self._parent
    
    def copy(self) -> BinNode:
        """Create and return a copy of this node."""
        return BinNode(self.data, self.left, self.right, self.parent)
    
class BinTree():
    """Binary tree."""
    def __init__(self, root: BinNode=None):
        """Create a new BinTree object.
        [root] - a BinNode which will be root of this tree."""
        if (root and not issubclass(root, BinNode)):
            raise ValueError("Only node can be root of tree!")
        self._root = root
        self._size = 0
        
    def __iter__(self):
        iterlist = []
        current = self._getLastLeft(self.root, iterlist)
        yield current
        while (True):
            if (current.right):
                current = self._getLastLeft(current.right, iterlist)
            elif (len(iterlist) > 0):
                current = iterlist.pop()
            else:
                break
            yield current
            
    def __contains__(self, value):
        for n in self:
            if (n.data == value):
                return True
        return False
    
    def __len__(self):
        return self._size
    
    def _getLastLeft(self, node, lst):
        """|INTERNAL| get last left node for this node, remembering path to it.
        Used in iterator."""
        if (not node):
            return None
        current = node
        while (current.left):
            lst.append(current)
            current = current.left
        return current
        
    def _countDepth(self, node):
        """|INTERNAL| recursevly counts depth
        node - node to count from."""
        if (not node):
            depth = -1
        else:
            depthLeft = self._countDepth(node.left)
            depthRight = self._countDepth(node.right)
            depth = 1 + (max(depthLeft, depthRight))
        return depth      
        
    @property
    def root(self):
        """Get root of this tree."""
        return self._root
    
    @property
    def size(self):
        """Get size (node count) of this tree."""
        return self._size
    
    @staticmethod
    def createTree(values: iter) -> BinTree:
        """Create and return a new tree from given values.
        `values` must be iterable."""
        tree = BinTree()
        datatype = None
        for v in values:
            if (not datatype):
                datatype = type(v)
            else:
                if (type(v) != datatype):
                    raise ValueError("Elements in `values` are have different types!")
            tree.insert(v)
        return tree    
    
    def isEmpty(self) -> bool: 
        """Whether this tree empty or not."""
        return self._size == 0
    
    def find(self, key) -> BinNode:
        """Find a node with given key in this tree. Returns None if node is not found."""
        curr = self.root
        while (curr):
            if (curr.data == key):
                return curr
            if (key < curr.data):
                curr = curr.left
            else:
                curr = curr.right
        return None
    
    def insert(self, value):
        """Create a new node with given value and insert it in this tree."""
        curr = self.root
        newNode = BinNode(value)
        while (curr):
            newNode._parent = curr
            if (value < curr.data):
                curr = curr.left
            else:
                curr = curr.right  
        if (not newNode.parent):
            self._root = newNode
        elif (value < newNode.parent.data):
            newNode.parent._left = newNode
        else:
            newNode.parent._right = newNode
        self._size += 1
        
    def remove(self, key):
        """Remove node with given key from this tree."""
        node = self.find(key)
        if (not node):
            raise ValueError("Node with given key is not found in this tree!")
        if (not node.left and not node.right):
            if (node.data < node.parent.data):
                node.parent._left = None
            else:
                node.parent._right = None
        elif (node.left and node.right):
            replace = node.left
            while (replace.right):
                replace = replace.right
            if (replace.data < replace.parent.data):
                replace.parent._left = None
            else:
                replace.parent._right = None
            replace._right = node.right
            replace._left = node.left if node.left != replace else None
            replace._parent = node._parent
            if (node.data < node.parent.data):
                node.parent._left = replace
            else:
                node.parent._right = replace 
        else:
            replace = node.left if node.left else node.right
            replace._parent = node._parent
            if (node.data < node.parent.data):
                node.parent._left = replace
            else:
                node.parent._right = replace  
        self._size -= 1
                
    def clear(self):
        """Clear this tree (remove all nodes)."""
        self._root = None
        self._size = 0
        
    def depth(self) -> int:
        """Get depth of this tree."""
        return self._countDepth(self._root)