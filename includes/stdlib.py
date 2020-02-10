# ==============-Math functions-============== #
from math import sin, cos

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
    
def lerpColor(color1: str, color2: str, factor: float) -> str:
    """Lieary interpolate between two colors by factor.
    `color1`: - color in hex value in form '#RRGGBB' to interpolate from
    `color2`: - color in hex value in form '#RRGGBB' to interpolate to
    `factor`: - lerp factor."""
    c1r = int(color1[1:3], 16)
    c1g = int(color1[3:5], 16)
    c1b = int(color1[5:], 16)
    c2r = int(color2[1:3], 16)
    c2g = int(color2[3:5], 16)
    c2b = int(color2[5:], 16)
    c3r = round(lerp(c1r, c2r, factor))
    c3g = round(lerp(c1g, c2g, factor))
    c3b = round(lerp(c1b, c2b, factor))
    return "#%02X%02X%02X" % (c3r, c3g, c3b)
    
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

def clampUp(value, ceil):
    """Clamp value by up limit.
    `value`: var - value to clamp
    `ceil`: var - upper limit."""    
    if (value > ceil):
        return ceil
    else:
        return value   
    
def clampDown(value, floor):
    """Clamp value by down limit.
    `value`: var - value to clamp
    `floor`: var - lower limit."""    
    if (value < floor):
        return floor
    else:
        return value
    
def binFull(number: int) -> str:
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
    
def rotatePoint(p: iter, angle: float, center: iter=[0, 0]):
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
    prevPos = file.tell()
    if (size > -1):
        data = file.read(size)
    else:
        data = file.read()
    file.seek(prevPos)
    return data

def peekline(file, limit: int=0) -> str:
    """Peek next characters untill next line or next `limit` characters if set."""
    prevPos = file.tell()
    data = ""
    while True:
        newChar = file.read(1)
        if (not newChar or newChar == "\n"):
            break
        data += newChar
        if (limit > 0 and len(data) >= limit):
            break
    file.seek(prevPos)
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