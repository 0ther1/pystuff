from struct import pack, unpack, calcsize

class StringFile():
    """File-like structure based on string class.
    Allows get file's contents, store it as string and manipulate with methods like read, peek, seek, tell etc.."""
    def __init__(self, filepath: str=""):
        """Create a new StringFile object.
        Returns object with contents of file at [filepath] if given."""
        self._data = ""
        self.filepath = None
        self._eof = True
        self._current_position = 0 
        if (filepath):
            with open(filepath, "r") as f:
                self._data = f.read()
            self.filepath = filepath
            self._eof = False
        
    def __len__(self):
        return len(self._data)
    
    @property
    def eof(self) -> bool:
        """Is end of file reached."""
        return self._eof
        
    @property
    def data(self) -> str:
        """Get full data of this file."""
        return self._data
        
    def clear(self):
        """Removes all data."""
        self._data = ""
        
    def write(self, data: str, rewrite: int=0):
        """Write [data] to file starting from current position.
        If [rewrite] == 0, then [data] inserts in file;
        if == -1, [data] rewrites next (length of [data]) characters;
        if > 0, [data] rewrites next [rewrite] characters."""
        offset = 0
        if (rewrite == -1):
            offset = len(data)
        elif (rewrite > 0):
            offset = rewrite
        self._data = self._data[:self._current_position] + data + self._data[self._current_position + offset:]
        self._current_position += len(data)
        
    def read(self, size: int=-1) -> str:
        """Get next [size] characters from data. size=-1 - returns all characters from current position to end."""
        if (size == 0):
            return ""
        if (self._eof):  # raise EOFError if tries to read at end of file
            raise EOFError("Cannot read after end of file")
        output = ""
        if (self._current_position + size > len(self._data)):         # if tries to read more than left
            size = len(self._data) - 1 - self._current_position   # cut [size] to remaining count
        if (size == -1):                                # if size == -1            
            output = self._data[self._current_position:]   # read from current position to end of file
            self._current_position = len(self._data)       # set current position at end of file
        else:
            output = self._data[self._current_position:self._current_position+size]  # else read given size
            self._current_position += size                                        # move current position
        
        if (self._current_position >= len(self._data) - 1):    # if we at end of file
            self._eof = True                             # set end of file as True
        return output   # return read data
        
    def seek(self, position: int):
        """Set current position at file in [position] (-1 - at end of file). Raises ValueError if given position out of bounds."""
        if (position < -1 or position > len(self._data)): 
            raise ValueError("Position to seek is beyond file size")    # raise ValueError if position is out of bounds
        if (position == -1):
            self._current_position = len(self._data) # set current position in end of file
        else:
            self._current_position = position        # set current position in [position]
        if (position != len(self._data)):    # if position not at end of file    
            self._eof = False                # set end of file as False
        
    def tell(self) -> int:
        """Get current position."""
        return self._current_position
        
    def peek(self, size: int=-1) -> str:
        """Get next [size] characters from data, but do not move current position. size=-1 - returns all characters from current position to end."""
        old_eof = self._eof               # save state
        old_pos = self._current_position
        output = self.read(size)        # read data
        self._eof = old_eof               # restore state
        self._current_position = old_pos
        return output
        
    def find(self, substr: str, start: int=-1, seek: bool=False) -> int:
        """Get position of [substr] in file. Returns -1 if not found. 
        Start searching from [start], -1 - from current position.
        If [seek] current position will be moved after 'substr' if it's present."""
        output = 0
        if (start == -1):
            output = self._data.find(substr, self._current_position)
        else:
            output = self._data.find(substr, start)
        if (seek and output != -1):
            self._current_position = output + len(substr)
        return output
        
    def save(self):
        """Save data to file."""
        if (self.filepath):
            with open(self.filepath, "w") as f:
                f.write(self._data)            
        else:
            raise RuntimeError("Cannot save file without filepath. Consider setting `filepath` property.")            

class StringBinaryFile(StringFile):
    """File-like structure based on string class.
    Allows get file's contents, store it as byte string and manipulate with methods like read, peek, seek, tell etc..
    All methods are working with binary numbers."""    
    def __init__(self, filepath: str=""):
        """Create a new StringBinaryFile object.
        Returns object with contents of file at [filepath] if given."""
        self._data = b""
        self.filepath = None
        self._eof = True
        self._current_position = 0        
        if (filepath):
            with open(filepath, "rb") as f:  
                self._data = f.read()
            self.filepath = filepath
            self._eof = False               
    
    def write(self, data, rewrite: int=0, format: str=""):
        """Write packed [data] to file starting from current position.
        If [format] is not specified: int = "i", float = "f", str = "{string_length}s".
        If [rewrite] == 0, then [data] inserts in file;
        if == -1, [data] rewrites next (length of [data]) bytes;
        if > 0, [data] rewrites next [rewrite] characters."""
        if (format):
            frmt = format
        else:
            frmt = None
            if (isinstance(data, int)): 
                frmt = "i"
            elif (isinstance(data, float)): 
                frmt = "f"
            elif (isinstance(data, str)):   
                frmt = "%ds" % len(data)
                data = data.encode("cp1251")
            else:                           
                raise ValueError("Only int, float and string supported to write in binary file!")            
        offset = 0
        if (rewrite == -1):
            offset = calcsize(frmt)
        elif (rewrite > 0):
            offset = rewrite
        self._data = self._data[:self._current_position] + pack(frmt, data) + self._data[self._current_position+offset:]
        self._current_position += calcsize(frmt)
    
    def read(self, format: str):
        """Get unpacked data from given format."""
        expected_size = calcsize(format)       
        if (expected_size == 0):
            return b""
        rawdata = super().read(expected_size)    
        if (len(rawdata) < expected_size):       
            raise RuntimeError("Length of read bytes is lesser than expected!")
        output = unpack(format, rawdata)[0]     
        return output
        
    def peek(self, format: str):
        """Get unpacked data from given format, but do not move current position."""
        oldEof = self._eof              
        oldPos = self._current_position
        output = self.read(format)       
        self._eof = oldEof               
        self._current_position = oldPos        
        return output
        
    def find(self, substr: bytes, start: int=-1, seek: bool=False) -> int:
        """Get position of [substr] in file. Returns -1 if not found. 
        Start searching from [start], -1 - from current position.
        If [seek] current position will be moved after 'substr' if it's present."""
        pos = self._data.find(substr, start if start != -1 else self._current_position)
        if (pos != -1 and seek):
            self.seek(pos + len(substr))
        return pos
        
    def save(self):
        """Save data to file."""
        if (self.filepath):
            with open(self.filepath, "wb") as f:
                f.write(self._data)
        else:
            raise RuntimeError("Cannot save file without filepath. Consider setting `filepath` property.")
        