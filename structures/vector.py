from math import acos

class Vector():
    def __init__(self, values=[]):
        self._values = list(values)
        
    def __len__(self):
        return len(self._values)
    
    def __str__(self):
        out = "Vector("
        for v in self._values:
            out += str(v) + ", "
        return out[:-2] + ")"
    
    def __iter__(self):
        for v in self._values:
            yield v
            
    def __contains__(self, value):
        return value in self._values
    
    def __setitem__(self, key, value):
        self._values[key] = value
        
    def __getitem__(self, key):
        if (isinstance(key, slice)):
            return Vector(self._values[key])
        return self._values[key]
    
    def __add__(self, other):
        vec = Vector(self._values.copy())
        if (isinstance(other, (int, float))):
            for i in range(len(vec._values)):
                vec._values[i] += other    
        elif (isinstance(other, (list, tuple, Vector))):
            if (len(other) != len(vec._values)):
                raise ValueError("`other` must have same dimensions.")
            for i in range(len(vec._values)):
                vec._values[i] += other[i]
        else:
            raise TypeError("`other` - invalid type, must be: int, float, list, tuple, Vector")
        return vec
    
    def __iadd__(self, other):
        self._values = (self + other)._values
        
    def __sub__(self, other):
        vec = Vector(self._values.copy())
        if (isinstance(other, (int, float))):
            for i in range(len(vec._values)):
                vec._values[i] -= other    
        elif (isinstance(other, (list, tuple, Vector))):
            if (len(other) != len(vec._values)):
                raise ValueError("`other` must have same dimensions.")
            for i in range(len(vec._values)):
                vec._values[i] -= other[i]
        else:
            raise TypeError("`other` - invalid type, must be: int, float, list, tuple, Vector")
        return vec    
    
    def __isub__(self, other):
        self._values = (self - other)._values    
    
    def __mul__(self, other):
        vec = Vector(self._values.copy())
        if (isinstance(other, (int, float))):
            for i in range(len(vec._values)):
                vec._values[i] *= other    
        else:
            raise TypeError("`other` - invalid type, must be: int, float. To multiply Vectors use dot, cross and triple product methods.")
        return vec    
    
    def __imul__(self, other):
        self._values = (self * other)._values    
    
    def __div__(self, other):
        vec = Vector(self._values.copy())
        if (isinstance(other, (int, float))):
            for i in range(len(vec._values)):
                vec._values[i] /= other    
        else:
            raise TypeError("`other` - invalid type, must be: int, float.")
        return vec        
    
    def __idiv__(self, other):
        self._values = (self / other)._values
        
    def clear(self):
        """Clear this vector."""
        self._values.clear()
        
    def copy(self):
        """Copy this vector."""
        return Vector(self._values.copy())
        
    def append(self, value):
        """Add `value` at vector's end."""
        self._values.append(value)
        
    def insert(self, index, value):
        """Add `value` before `index` in vector."""
        self._values.insert(index, value)
        
    def extend(self, iterable):
        """Extend vector by appending elements from the iterable."""
        self._values.extend(iterable)
        
    def pop(self, index=None):
        """Remove value from vector and return it. If [index] is not given - pops last element."""
        if (index == None):
            return self._values.pop()
        else:
            return self._values.pop(index)
        
    def index(self, value, start=0, end=-1):
        """Get first index of value. Raises ValueError if not present."""
        try:
            self._values.index(value, start, end)
        except ValueError:
            raise ValueError("{} is not in vector.".format(value))
        
    def length(self) -> float:
        """Get vector length."""
        summ = 0.0
        for co in self._values:
            summ += co ** 2
        return summ ** 0.5
    
    def euclidean_distance(self, other) -> float:
        """Get Euclidean distance between this and other vector. Vectors must have same dimensions."""
        if (not isinstance(other, Vector)):
            raise TypeError("`other` must be a Vector object.")        
        if (len(self._values) != len(other)):
            raise ValueError("`other` must have same dimensions.")
        summ = 0.0
        for i, co in enumerate(self._values):
            summ += (other[i] - co) ** 2
        return summ ** 0.5    
    
    def dot_product(self, other) -> float:
        """Get a dot product between two vectors."""
        if (not isinstance(other, Vector)):
            raise TypeError("`other` must be a Vector object.")
        if (len(self._values) != len(other)):
            raise ValueError("`other` must have same dimensions.")        
        summ = 0.0
        for i, co in enumerate(self._values):
            summ += co * other[i]
        return summ
    
    def cross_product(self, other):
        """Get a cross product between two three-dimension vectors."""
        if (not isinstance(other, Vector)):
            raise TypeError("`other` must be a Vector object.")        
        if (len(self._values) != len(other)):
            raise ValueError("`other` must have same dimensions.")   
        if (len(self._values) != 3):
            raise ValueError("Cross product can only be calculated for three-dimension vectors.")
        return Vector([self._values[1] * other[2] - self._values[2] * other[1], self._values[2] * other[0] - self._values[0] * other[2], self._values[0] * other[1] - self._values[1] * other[0]])
    
    def triple_product(self, v2, v3) -> float:
        """Get a triple product between three three-dimension vectors."""
        if (not isinstance(v2, Vector) or not isinstance(v3, Vector)):
            raise TypeError("`v2` and `v3` must be a Vector objects.")        
        if (len(self._values) != len(v2) != len(v3)):
            raise ValueError("`v2` and `v3` must have same dimensions.")   
        if (len(self._values) != 3):
            raise ValueError("Triple product can only be calculated for three-dimension vectors!")
        return self.dot_product(v2.cross_product(v3))
    
    def angle_between(self, other) -> float:
        """Get angle between 2 vectors in radians."""
        return acos(self.dot_product(other) / (self.length * other.length))    
