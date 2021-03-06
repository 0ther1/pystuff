# ==============-Math functions-============== #
from math import sin, cos, acos

def lerp(a, b, factor: float):
    """Lineary interpolate between [a;b] by factor.
    `a`: var - first value to start from
    `b`: var - second value to end with
    `factor` - value in range [0;1]."""
    factor = clamp(factor, 0.0, 1.0)
    if (factor == 0.0):
        return a
    elif (factor == 1.0):
        return b
    else:
        return a + (b - a) * factor
    
def clamp(value, floor, ceil):
    """Clamp value by up and down limits.
    `value`: var - value to clamp
    `floor`: var - lower limit
    `ceil`: var - upper limit."""
    if (value > ceil):
        return ceil
    elif (value < floor):
        return floor
    else:
        return value

def clamp_up(value, ceil):
    """Clamp value by up limit.
    `value`: var - value to clamp
    `ceil`: var - upper limit."""    
    if (value > ceil):
        return ceil
    else:
        return value   
    
def clamp_down(value, floor):
    """Clamp value by down limit.
    `value`: var - value to clamp
    `floor`: var - lower limit."""    
    if (value < floor):
        return floor
    else:
        return value
    
def bin8(number: int) -> str:
    """Get full 8-length binary representation of given nubmer."""
    return "0b%08d" % int(bin(number)[2:])

def distance(p1: iter, p2: iter) -> float:
    """Get distance between 2 points.
    `p1`, `p2` - a sequence of coordinates."""
    if (len(p1) == len(p2)):
        summ = 0.0
        for i in range(len(p1)):
            summ += (p2[i] - p1[i]) ** 2
        return summ ** 0.5
    else:
        raise ValueError("`p1` and `p2` must have same lenghts!")
    
def length(vec: iter) -> float:
    """Get vector length."""
    summ = 0.0
    for co in vec:
        summ += co ** 2
    return summ ** 0.5

def angle_between(v1: iter, v2: iter) -> float:
    """Get angle between 2 vectors in radians."""
    return acos(dot_product(v1, v2) / (length(v1) * length(v2)) )

def dot_product(v1: iter, v2: iter) -> float:
    """Get a dot product between 2 vectors."""
    if (len(v1) == len(v2)):
        summ = 0.0
        for i, co in enumerate(v1):
            summ += co * v2[i]
        return summ
    else:
        raise ValueError("`v1` and `v2` must have same lenghts!")
    
def cross_product(v1: iter, v2: iter) -> list:
    """Get a cross product between 2 vectors (3D)."""
    if (len(v1) != len(v2)):
        raise ValueError("`v1` and `v2` must have same lenghts!")   
    if (len(v1) != 3):
        raise ValueError("Cross product can only be calculated for 3D vectors!")
    return [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]
        
def triple_product(v1: iter, v2: iter, v3: iter) -> float:
    """Get a triple product between 3 vectors (3D)."""
    if (len(v1) != len(v2) != len(v3)):
        raise ValueError("`v1` and `v2` must have same lenghts!")   
    if (len(v1) != 3):
        raise ValueError("Triple product can be calculated for 3D vectors!")
    return dot_product(v1, cross_product(v2, v3))
    
def rotate_point(p: iter, angle: float, center: iter=[0, 0]):
    """Rotate 2D point around another.
    `p` - a sequence of coordinates of point to rotate
    `angle` - angle of rotation in radians
    [center] - a sequence of coordinates of point to rotate around."""
    if (len(center) == len(p)):
        moved = (p[0] - center[0], p[1] - center[1])
        rotated = (moved[0] * cos(angle) - moved[1] * sin(angle),
                   moved[0] * sin(angle) + moved[1] * cos(angle))
        return (rotated[0] + center[0], rotated[1] + center[1])
    else:
        raise ValueError("`p` and `center` must have same lenghts!")
    
# ==============-File functions-============== #    
def peek(file, size: int=-1):
    """Peek next `size` characters without moving cursor. If size is -1 - peeks till the end of file."""
    prev_pos = file.tell()
    if (size > -1):
        data = file.read(size)
    else:
        data = file.read()
    file.seek(prev_pos)
    return data

def peekline(file, limit: int=0) -> str:
    """Peek next characters untill next line or next `limit` characters if set."""
    prev_pos = file.tell()
    data = ""
    while True:
        new_char = file.read(1)
        if (not new_char or new_char == "\n"):
            break
        data += new_char
        if (limit > 0 and len(data) >= limit):
            break
    file.seek(prev_pos)
    return data
# ==============-File system functions-============== #
import os

def movefile(src: str, dest: str):
    """Move `src` file to `dest`.
    If `dest` is path to file `src` will have given name, if `dest` is path to directory to move to `src` will have same filename.
    If `dest` path is not exists it will be created."""
    src = os.path.normpath(src)
    dest = os.path.normpath(dest)
    filename = os.path.split(src)[1]
    if (os.path.splitext(dest)[1] == ""):
        destdir = dest
    else:
        destdir = os.path.split(dest)[0]
    if (not os.path.exists(destdir)):
        os.makedirs(destdir)
    if (destdir != dest):
        os.rename(src, destdir + filename)
    else:
        os.rename(src, dest)