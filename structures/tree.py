from struct import pack, unpack

def nlr(node):
    """Iteratively visit tree in pre-order starting from `node`."""
    if (not node):
        return
    hist = [node]
    while (hist):
        node = hist.pop()
        yield node
        if (node.right):
            hist.append(node.right)
        if (node.left):
            hist.append(node.left)
            
def nrl(node):
    """Iteratively visit tree in reversed pre-order starting from `node`."""
    if (not node):
        return
    hist = [node]
    while (hist):
        node = hist.pop()
        yield node
        if (node.left):
            hist.append(node.left)
        if (node.right):
            hist.append(node.right)
            
def lnr(node):
    """Iteratively visit tree in in-order starting from `node`."""
    hist = []
    while (hist or node):
        if (node):
            hist.append(node)
            node = node.left
        else:
            node = hist.pop()
            yield node
            node = node.right
            
def rnl(node):
    """Iteratively visit tree in reverse in-order starting from `node`."""
    hist = []
    while (hist or node):
        if (node):
            hist.append(node)
            node = node.right
        else:
            node = hist.pop()
            yield node
            node = node.left

def lrn(node):
    """Iteratively visit tree in post-order starting from `node`."""
    hist = []
    last_node = None
    while (hist or node):
        if (node):
            hist.append(node)
            node = node.left
        else:
            peek_node = hist[-1]
            if (peek_node.right and last_node != peek_node.right):
                node = peek_node.right
            else:
                yield peek_node
                last_node = hist.pop()
                
def rln(node):
    """Iteratively visit tree in reversed post-order starting from `node`."""
    hist = []
    last_node = None
    while (hist or node):
        if (node):
            hist.append(node)
            node = node.right
        else:
            peek_node = hist[-1]
            if (peek_node.left and last_node != peek_node.left):
                node = peek_node.left
            else:
                yield peek_node
                last_node = hist.pop()
                
def in_depth(node):
    """Iteratively visit tree in level-order starting from `node`."""
    queue = [node]
    while queue:
        node = queue.pop(0)
        yield node
        if (node.left):
            queue.append(node.left)
        if (node.right):
            queue.append(node.right)        

class BinNode():
    """Binary tree node."""
    def __init__(self, data, left=None, right=None, parent=None):
        """Create a new BinNode object.
        data - data stored in this node,
        [left] - left child of this node,
        [right] - right child of this node,
        [parent] - parent of this node."""
        self.data = data
        if (left and not issubclass(type(left), BinNode)):
            raise TypeError("`left` must be a BinNode derived object!")
        if (right and not issubclass(type(right), BinNode)):
            raise TypeError("`right` must be a BinNode derived object!")
        if (parent and not issubclass(type(parent), BinNode)):
            raise TypeError("`parent` must be a BinNode derived object!")        
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
    
    def copy(self):
        """Create and return a copy of this node."""
        return self.__class__(self.data, self.left, self.right, self.parent)
    
class BinTree():
    """Binary tree."""
    def __init__(self, root=None):
        """Create a new BinTree object.
        [root] - a BinNode which will be root of this tree."""
        if (root and not issubclass(root, BinNode)):
            raise ValueError("Only node can be root of tree!")
        self._root = root
        self._size = 0
            
    def __contains__(self, value):
        for n in lnr(self.root):
            if (n.data == value):
                return True
        return False
    
    def __len__(self):
        return self._size
        
    def _count_depth(self, node):
        """|INTERNAL| recursevly counts depth
        node - node to count from."""
        if (not node):
            depth = -1
        else:
            depth_left = self._count_depth(node.left)
            depth_right = self._count_depth(node.right)
            depth = 1 + (max(depth_left, depth_right))
        return depth
    
    def _write_element(self, file, element):
        """|INTERNAL| write `element` to opened `file`."""
        data_type = type(element)
        if (data_type in (int, float)):
            file.write(pack(str(data_type)[8], element))    # if int or float - just write element
        elif (data_type in (str, bytes)):
            file.write(pack("i", len(element)))             # if str or bytes - write length and then element itself
            if (data_type == str):
                file.write(element.encode())
            else:
                file.write(element)
        else:
            file.write(pack("i", len(element)))             # if list or tuple - write it's length and recursevly write it's contents
            for e in element:
                file.write(str(type(e))[8].encode("ascii")) # write contents data type
                self._write_element(file, e)
                
    def _read_element(self, file, datatype):
        """|INTERNAL| read element with given `datatype` from opened `file`."""
        if (datatype in ("i", "f")):
            return unpack(datatype, file.read(4))[0]
        elif (datatype in ("s", "b")):
            length = unpack("i", file.read(4))[0]
            if (datatype == "s"):
                return unpack("%ds" % length, file.read(length))[0].decode()
            else:
                return file.read(length)
        else:
            length = unpack("i", file.read(4))[0]
            data = []
            for i in range(length):
                elem_type = unpack("s", file.read(1))[0].decode("ascii")
                data.append( self._read_element(file, elem_type) )
            if (datatype == "t"):
                data = tuple(data)
            return data
        
    @property
    def root(self):
        """Get root of this tree."""
        return self._root
    
    @property
    def size(self):
        """Get size (node count) of this tree."""
        return self._size
    
    @staticmethod
    def create_tree(values: iter):
        """Create and return a new tree from given values.
        `values` must be iterable."""
        tree = BinTree()
        for v in values:
            tree.insert(v)
        return tree
    
    def is_empty(self) -> bool: 
        """Whether this tree empty or not."""
        return self._size == 0
    
    def find(self, key):
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
        new_node = BinNode(value)
        while (curr):
            new_node._parent = curr
            if (value < curr.data):
                curr = curr.left
            else:
                curr = curr.right  
        if (not new_node.parent):
            self._root = new_node
        elif (value < new_node.parent.data):
            new_node.parent._left = new_node
        else:
            new_node.parent._right = new_node
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
        return self._count_depth(self._root)
    
    def write(self, filepath, writefunc=None):
        """Write tree data to binary file at `filepath`.
        If `writefunc` given - writes data using this function, otherwise writes itself if tree data type is standart (int, float, str, bytes, list, tuple).
        `writefunc` takes opened file and node data as args."""
        with open(filepath, "wb") as file:
            if (not writefunc):
                data_type = None
                for n in nlr(self.root):
                    if (not data_type):
                        data_type = type(n.data)
                        if (data_type not in (int, float, str, list, tuple, bytes)):
                            raise RuntimeError("To write non-standart data types pass `writefunc`.")
                    elif (type(n.data) != data_type):
                        raise RuntimeError("To write tree all nodes must have same data type.")
                file.write(str(data_type)[8].encode("ascii"))
            for n in nlr(self.root):
                if (writefunc):
                    writefunc(file, n.data)
                else:
                    self._write_element(file, n.data)
                    
    def read(self, filepath, readfunc=None):
        """Read tree data from binary file at `filepath`.
        If `readfunc` given - reads data using this function, otherwise reads itself if saved data type is standart (int, float, str, bytes, list, tuple).
        `readfunc` takes opened file as arg."""
        self.clear()
        with open(filepath, "rb") as file:
            if (not readfunc):
                raw = file.read(1)
                if (not raw.isalpha()):
                    raise ValueError("File '%s': readfunc required or invalid tree data file." % filepath)
                data_type = unpack("s", raw)[0].decode("ascii")
            while (True):
                pos = file.tell()
                peek = file.read(1)
                if (not peek):
                    break
                file.seek(pos)
                if (readfunc):
                    self.insert(readfunc(file))
                else:
                    self.insert(self._read_element(file, data_type))
                    