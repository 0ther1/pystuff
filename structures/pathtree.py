from path import Path
import os

class PathTreeNode():
    """Tree node of path tree.
    `data`    : str          - part of path (folder or filename)
    `children`: list         - list of all children of this node (files and folders in this directory), sorted in alphabetic order
    `parent`  : PathTreeNode - node witch is parent to this one (parent folder)."""
    def __init__(self, data: str, parent: PathTreeNode=None):
        """Create a new PathTreeNode object.
        `data`   - part of path (folder or filename)
        [parent] - node witch is parent to this one (parent folder)."""
        self.data = data
        self._children = []
        self._parent = parent
        
    @property
    def parent(self):
        """Get a parent of this node."""
        return self._parent
        
    def __iter__(self):
        """Iterate through node's children."""
        for c in self._children:
            yield c
            
    def __getitem__(self, key):
        """Get child with key."""
        return self._children[key]
    
    def appendChild(self, node: PathTreeNode):
        """Add a new child. Inserts in proper position.
        `node` - node to insert."""
        if (not isinstance(node, PathTreeNode)):
            raise TypeError("Only PathTreeNode object can be appended!")
        if (len(self._children) == 0):
            self._children.append(node)
        else:
            start = 0
            end = len(self._children)        
            if (len(self._children) > 2):
                while (True):
                    mid = start + ((end - start) // 2)
                    split = self._children[mid]
                    if (split.data.casefold() == node.data.casefold()):
                        return split
                    elif (split.data.casefold() < node.data.casefold()):
                        start = mid
                    else:
                        end = mid
                    if (end - start < 3):
                        break            
            for i in range(start, end):
                if (self._children[i].data.casefold() > node.data.casefold()):
                    self._children.insert(i, node)
                    break
            else:
                self._children.append(node)
        node._parent = self
                
    def removeChild(self, node: PathTreeNode):
        """Remove given node from children. Rasies ValueError if node is not in children list."""
        self._children.remove(node)
        
    def findInChildren(self, key: str):
        """Get node in children by given key. Returns None if not found.
        `key` - path to find."""
        start = 0
        end = len(self._children)        
        if (len(self._children) > 2):
            while (True):
                mid = start + ((end - start) // 2)
                split = self._children[mid]
                if (split.data.casefold() == key.casefold()):
                    return split
                elif (split.data.casefold() < key.casefold()):
                    start = mid
                else:
                    end = mid
                if (end - start < 3):
                    break            
        for i in range(start, end):
            if (self._children[i].data.casefold() == key.casefold()):
                return self._children[i]
        return None
        
class PathTree():
    """A tree of paths (file catalog)."""
    def __init__(self, root: PathTreeNode=None):
        """Create a new tree.
        [root] - node which will be root of this tree."""
        self._root = None
        if (root and isinstance(root, PathTreeNode)):
            self._root = root
        
    def __contains__(self, path):
        """Is given path presents in tree."""
        return self.find(path) != None
    
    @property
    def root(self):
        """Get root of this tree."""
        return self._root
                    
    @staticmethod
    def fromPath(path) -> PathTree:
        """Create PathTree from given path (up to end of given path)."""
        if (isinstance(path, str)):
            path = Path(path)
        if (isinstance(path, Path)):
            tree = PathTree()
            tree.insert(path)
            return tree
        else:
            raise TypeError("`path` must be either string or Path object!")
        
    @staticmethod
    def fromCatalog(path, maxdepth: int=-1, absolute: bool=True, depth=0, tree=None) -> PathTree:
        """Create PathTree from given catalog (scans files within and appends them to tree).
        [maxdepth] - maximum depth of recursive scanning, if reched stops scanning any deeper
        [absoulte] - make tree with absolute path or relative (e.g. absolute: C:\\Program Files\\Python\\... etc; relative: Python\\... etc)
        [depth]    - !INTERNAL DO NOT USE! current depth of recursion, used inside when calling itself
        [tree]     - !INTERNAL DO NOT USE! tree to append to, on first call is being created and passed further."""
        if (maxdepth > 0 and depth > maxdepth):
            return
        if (isinstance(path, str)):
            path = Path(path)
        if (isinstance(path, Path)):
            if (path.exists() or not absolute):
                if (path.isDir()):
                    if (not tree):
                        tree = PathTree.fromPath(path if absolute else path[-1])
                    if (not absolute):
                        os.chdir(path.path)
                        path = Path(os.curdir)                    
                    for f in os.listdir(path.path):
                        subp = Path(os.path.abspath(path.path) + "\\" + f)
                        if (not absolute):
                            subp = Path(subp.path[subp.path.index(tree.root.data):])
                        tree.insert(subp)
                        if (not absolute):                        
                            subp = Path(os.path.abspath(path.path) + "\\" + f)
                        if (subp.isDir()):
                            PathTree.fromCatalog(subp, maxdepth, absolute, depth + 1, tree)                        
                else:
                    raise ValueError("Path '{0}' must be a directory!".format(path))
            else:
                raise ValueError("Path '{0}' is not exists!".format(path))
        else:
            raise TypeError("`path` must be either string or Path object!")
        if (not absolute):
            os.chdir(os.path.dirname(os.path.abspath(path.path)))        
        return tree
        
    def insert(self, path):
        """Insert path to a tree.
        `path`: str/Path - path to insert, in order to be inserted must starts from same path as tree root."""
        if (isinstance(path, str)):
            path = Path(path)
        if (isinstance(path, Path)):        
            start = None
            startIdx = None
            if (self._root):
                if (self._root.data.casefold() == path[0].casefold()):
                    parent = self._root
                    for i in range(1, len(path)):                  
                        node = parent.findInChildren(path[i])
                        if (node):
                            parent = node
                        else:
                            start = parent
                            startIdx = i
                            break
                    else:
                        raise ValueError("Path '{0}' already in tree!".format(path.path))
                else:
                    raise ValueError("Cannot insert path with root '{0}'".format(path[0]))
            else:
                start = self._root = PathTreeNode(path[0])
                startIdx = 1
            lastNode = start
            for i in range(startIdx, len(path)):
                newNode = PathTreeNode(path[i])
                lastNode.appendChild(newNode)
                lastNode = newNode
        else:
            raise TypeError("`path` must be either string or Path object!")
                
    def find(self, path) -> PathTreeNode:
        """Get end node by given path. Returns None if not found.
        `path`: str/Path - path to find."""
        if (self._root):            
            if (isinstance(path, str)):
                path = Path(path)
            if (isinstance(path, Path)):
                if (self._root.data.casefold() == path.path.casefold()):
                    return self._root
                if (self._root.data.casefold() != path[0].casefold()):
                    return None
                parent = self._root
                for i in range(1, len(path)):
                    node = parent.findInChildren(path[i])
                    if (node == None):
                        return None
                    parent = node
                return parent
        else:
            raise RuntimeError("Tree is empty!")
                