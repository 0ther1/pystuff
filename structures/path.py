import os.path

class Path():
    """A filepath."""
    def __init__(self, path: str):
        """Create new Path object.
        `path`: string - filepath."""
        self._path = Path.normalize(path)
        
    @property
    def path(self):
        return self._path
        
    def __str__(self):
        return self._path
    
    def __iter__(self):
        """Iterate through whole path starting from root."""
        if (self.isDir()):
            split = self._path[:-1].split("\\")            
        else:
            split = self._path.split("\\")            
        for i in range(len(split)):
            yield Path("\\".join(split[:i+1]))
            
    def __getitem__(self, key):
        if (self.isDir()):
            split = self._path[:-1].split("\\")            
        else:
            split = self._path.split("\\")          
        return split[key]
    
    def __len__(self):
        if (self.isDir()):
            split = self._path[:-1].split("\\")            
        else:
            split = self._path.split("\\")          
        return len(split)
        
    @staticmethod
    def normalize(path: str) -> str:
        """Make normal version of given path.
        Normal version has backslashes and if it's a dir additional backslash at the end.
        `path`: string - filepath."""
        normpath = os.path.normpath(path)
        split = os.path.splitext(normpath)
        if ( (os.path.exists(normpath) and os.path.isdir(normpath)) or (not os.path.exists(normpath) and (not split[1] and normpath[-1] != "\\")) ):
            normpath += "\\"
        return normpath
    
    def ext(self) -> str:
        """Get extension of this filepath. Returns None if path leads to dir."""
        if (self.isDir()):
            return None
        else:
            return os.path.splitext(self._path)[1]
        
    def filename(self) -> str:
        """Get name of file. Returns None if path leads to dir."""
        if (self.isDir()):
            return None
        else:
            return os.path.split(self._path)[1]
        
    def exists(self) -> bool:
        """Is this path exists in filesystem."""
        return os.path.exists(self._path)
        
    def parentDir(self) -> Path:
        """Get path to parent dir of this path."""
        if (self.isDir()):
            parentPath = os.path.split(self._path[:-1])[0] 
        else:
            parentPath = os.path.split(self._path)[0] 
        return Path(parentPath)
    
    def isDir(self) -> bool:
        """Is path leads to dir."""
        if (self.exists()):
            return os.path.isdir(self._path)
        else:            
            split = os.path.splitext(self._path)
            return split[1] == ""
    
    def append(self, path: str):
        """Add to this path additional one. Raises RuntimeError if current path is not a dir."""
        if (self.isDir()):
            self._path = Path.normalize(self._path + path)
        else:
            raise RuntimeError("Path can only be appended to dir!")
        
    def makepath(self):
        """Make whole path or path to file if it's not exsists."""
        if (self.isDir()):
            endPath = self
        else:
            endPath = self.parentDir()
        if (not endPath.exists()):
            os.makedirs(endPath._path)        
            