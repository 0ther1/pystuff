import re

from stdlib import lerp

def hex_to_rgb(color: str) -> list:
    """Convert HEX color to RGB color."""
    return [ int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16) ]

def hex_to_cmy(color: str) -> list:
    """Convert HEX color to CMY color."""
    return rgb_to_cmy(hex_to_rgb(color))
    
def hex_to_cmyk(color: str) -> list:
    """Convert HEX color to CMYK color."""
    return rgb_to_cmyk(hex_to_rgb(color))
    
def hex_to_hsv(color: str) -> list:
    """Convert HEX color to HSV color."""
    return rgb_to_hsv(hex_to_rgb(color))

def hex_to_hsl(color: str) -> list:
    """Convert HEX color to HSL color."""
    return rgb_to_hsl(hex_to_rgb(color))


def cmy_to_hex(color: list) -> str:
    """Convert CMY color to HEX color."""
    return rgb_to_hex(cmy_to_rgb(color))

def cmy_to_rgb(color: list) -> list:
    """Convert CMY color to RGB color."""
    r = 255 * (1 - color[0])
    g = 255 * (1 - color[1])
    b = 255 * (1 - color[2])
    return [r, g, b]
    
def cmy_to_cmyk(color: list) -> list:
    """Convert CMY color to CMYK color."""
    return color + [0.0]

def cmy_to_hsv(color: list) -> list:
    """Convert CMY color to HSV color."""
    return rgb_to_hsv(cmy_to_rgb(color))

def cmy_to_hsl(color: list) -> list:
    """Convert CMY color to HSL color."""
    return rgb_to_hsl(cmy_to_rgb(color))

def cmyk_to_hex(color: list) -> str:
    """Convert CMYK color to HEX color."""
    return rgb_to_hex(cmyk_to_rgb(color))

def cmyk_to_rgb(color: list) -> list:
    """Convert CMYK color to RGB color."""
    r = 255 * (1 - color[0]) * (1 - color[3])
    g = 255 * (1 - color[1]) * (1 - color[3])
    b = 255 * (1 - color[2]) * (1 - color[3])
    return [r, g, b]
    
def cmyk_to_cmy(color: list) -> list:
    """Convert CMYK color to CMY color."""
    return color[:-1]

def cmyk_to_hsv(color: list) -> list:
    """Convert CMYK color to HSV color."""
    return rgb_to_hsv(cmyk_to_rgb(color))

def cmyk_to_hsl(color: list) -> list:
    """Convert CMYK color to HSL color."""
    return rgb_to_hsl(cmyk_to_rgb(color))

def hsv_to_hex(color: list) -> str:
    """Convert HSV color to HEX color."""
    return rgb_to_hex(hsv_to_rgb(color))

def hsv_to_rgb(color: list) -> list:
    """Convert HSV color to RGB color."""
    h = color[0]
    s = color[1]
    v = color[2]
    if (s > 1.0):
        s /= 100
    if (v > 1.0):
        v /= 100
    c = v * s
    x = c * (1 - abs( (h / 60) % 2 - 1))
    m = v - c
    if (0 <= h < 60):
        rp = c
        gp = x
        bp = 0
    elif (60 <= h < 120):
        rp = x
        gp = c
        bp = 0    
    elif (120 <= h < 180):
        rp = 0
        gp = c
        bp = x            
    elif (180 <= h < 240):
        rp = 0
        gp = x
        bp = c            
    elif (240 <= h < 300):
        rp = x
        gp = 0
        bp = c
    else:
        rp = c
        gp = 0
        bp = x    
    return [ (rp+m)*255, (gp+m)*255, (bp+m)*255 ]
        
def hsv_to_cmy(color: list) -> list:
    """Convert HSV color to CMY color."""
    return rgb_to_cmy(hsv_to_rgb(color))

def hsv_to_cmyk(color: list) -> list:
    """Convert HSV color to CMYK color."""
    return rgb_to_cmyk(hsv_to_rgb(color))

def hsv_to_hsl(color: list) -> list:
    """Convert HSV color to HSL color."""
    return rgb_to_hsl(hsv_to_rgb(color))


def hsl_to_hex(color: list) -> str:
    """Convert HSL color to HEX color."""
    return rgb_to_hex(hsl_to_rgb(color))

def hsl_to_rgb(color: list) -> list:
    """Convert HSL color to RGB color."""
    h = color[0]
    s = color[1]
    l = color[2]
    if (s > 1.0):
        s /= 100
    if (l > 1.0):
        l /= 100
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs( (h / 60) % 2 - 1))
    m = l -  c / 2
    if (0 <= h < 60):
        rp = c
        gp = x
        bp = 0
    elif (60 <= h < 120):
        rp = x
        gp = c
        bp = 0    
    elif (120 <= h < 180):
        rp = 0
        gp = c
        bp = x            
    elif (180 <= h < 240):
        rp = 0
        gp = x
        bp = c            
    elif (240 <= h < 300):
        rp = x
        gp = 0
        bp = c
    else:
        rp = c
        gp = 0
        bp = x    
    return [ (rp+m)*255, (gp+m)*255, (bp+m)*255 ]
        
def hsl_to_cmy(color: list) -> list:
    """Convert HSL color to CMY color."""
    return rgb_to_cmy(hsl_to_rgb(color))

def hsl_to_cmyk(color: list) -> list:
    """Convert HSL color to CMYK color."""
    return rgb_to_cmyk(hsl_to_rgb(color))

def hsl_to_hsv(color: list) -> list:
    """Convert HSL color to HSV color."""
    return rgb_to_hsl(hsl_to_rgb(color))


def rgb_to_hex(color: list) -> str:
    """Convert RGB color to HEX color."""
    return "#%02X%02X%02X" % (color[0], color[1], color[2])

def rgb_to_cmy(color: list) -> list:
    """Convert RGB color to CMY color."""
    return rgb_to_cmyk(color)[:-1]

def rgb_to_cmyk(color: list) -> list:
    """Convert RGB color to CMYK color."""
    rp = color[0] / 255
    gp = color[1] / 255
    bp = color[2] / 255
    k = 1 - max(rp, gp, bp)
    if (k != 1.0):
        c = (1 - rp - k) / (1 - k)
        m = (1 - gp - k) / (1 - k)
        y = (1 - bp - k) / (1 - k)
    else:
        c = m = y = 0.0
    return [c, m, y, k]

def rgb_to_hsv(color: list) -> list:
    """Convert RGB color to HSV color."""
    rp = color[0] / 255
    gp = color[1] / 255
    bp = color[2] / 255
    cmax = max(rp, gp, bp)
    cmin = min(rp, gp, bp)
    delta = cmax - cmin
    if (delta == 0):
        h = 0
    elif (cmax == rp):
        h = 60 * (((gp - bp)/delta) % 6)
    elif (cmax == gp):
        h = 60 * (((bp - rp)/delta) + 2)
    else:
        h = 60 * (((rp - gp)/delta) + 4)    
    if (cmax == 0):
        s = 0
    else:
        s = (delta / cmax) * 100
    v = cmax * 100
    return [h, s, v]

def rgb_to_hsl(color: list) -> list:
    """Convert RGB color to HSL color."""
    rp = color[0] / 255
    gp = color[1] / 255
    bp = color[2] / 255
    cmax = max(rp, gp, bp)
    cmin = min(rp, gp, bp)
    delta = cmax - cmin
    l = (cmax + cmin) / 2
    if (delta == 0):
        h = 0
    elif (cmax == rp):
        h = 60 * (((gp - bp)/delta) % 6)
    elif (cmax == gp):
        h = 60 * (((bp - rp)/delta) + 2)
    else:
        h = 60 * (((rp - gp)/delta) + 4)    
    if (delta == 0):
        s = 0
    else:
        s = (delta / (1 - abs(2 * l - 1))) * 100
    return [h, s, l]

def convert_color(color, modefrom: str, modeto: str):
    """Convert color from `modefrom` to `modeto`.
    `color`: str/list - color to convert
    `modefrom`: mode of original color
    `modeto`: mode of result color.
    Modes are: 'hex', 'rgb', 'cmy', 'cmyk', 'hsv' and 'hsl'."""
    if (modefrom.casefold() not in ("hex", "rgb", "cmy", "cmyk", "hsv", "hsl")):
        raise ValueError("Invalid mode to convert from, must be 'hex', 'rgb', 'cmy', 'cmyk', 'hsv' or 'hsl'")
    if (modeto.casefold() not in ("hex", "rgb", "cmy", "cmyk", "hsv", "hsl")):
        raise ValueError("Invalid mode to convert to, must be 'hex', 'rgb', 'cmy', 'cmyk', 'hsv' or 'hsl'")    
    if (modefrom.casefold() == "hex"):
        if (modeto.casefold() == "hex"):
            return color        
        elif (modeto.casefold() == "rgb"):
            return hex_to_rgb(color)
        elif (modeto.casefold() == "cmy"):
            return hex_to_cmy(color)
        elif (modeto.casefold() == "cmyk"):
            return hex_to_cmyk(color)
        elif (modeto.casefold() == "hsv"):
            return hex_to_hsv(color)
        elif (modeto.casefold() == "hsl"):
            return hex_to_hsl(color)        
    elif (modefrom.casefold() == "rgb"):
        if (modeto.casefold() == "hex"):
            return rgb_to_hex(color)        
        elif (modeto.casefold() == "rgb"):
            return color
        elif (modeto.casefold() == "cmy"):
            return rgb_to_cmy(color)
        elif (modeto.casefold() == "cmyk"):
            return rgb_to_cmyk(color)
        elif (modeto.casefold() == "hsv"):
            return rgb_to_hsv(color)
        elif (modeto.casefold() == "hsl"):
            return rgb_to_hsl(color)        
    elif (modefrom.casefold() == "cmy"):
        if (modeto.casefold() == "hex"):
            return cmy_to_hex(color)        
        elif (modeto.casefold() == "rgb"):
            return cmy_to_rgb(color)
        elif (modeto.casefold() == "cmy"):
            return color
        elif (modeto.casefold() == "cmyk"):
            return cmy_to_cmyk(color)
        elif (modeto.casefold() == "hsv"):
            return cmy_to_hsv(color)
        elif (modeto.casefold() == "hsl"):
            return cmy_to_hsl(color)        
    elif (modefrom.casefold() == "cmyk"):
        if (modeto.casefold() == "hex"):
            return cmyk_to_hex(color)        
        elif (modeto.casefold() == "rgb"):
            return cmyk_to_rgb(color)
        elif (modeto.casefold() == "cmy"):
            return cmyk_to_cmy(color)
        elif (modeto.casefold() == "cmyk"):
            return color
        elif (modeto.casefold() == "hsv"):
            return cmyk_to_hsv(color)
        elif (modeto.casefold() == "hsl"):
            return cmyk_to_hsl(color)        
    elif (modefrom.casefold() == "hsv"):
        if (modeto.casefold() == "hex"):
            return hsv_to_hex(color)        
        elif (modeto.casefold() == "rgb"):
            return hsv_to_rgb(color)
        elif (modeto.casefold() == "cmy"):
            return hsv_to_cmy(color)
        elif (modeto.casefold() == "cmyk"):
            return hsv_to_cmyk(color)
        elif (modeto.casefold() == "hsv"):
            return color
        elif (modeto.casefold() == "hsl"):
            return hsv_to_hsl(color)
    elif (modefrom.casefold() == "hsl"):
        if (modeto.casefold() == "hex"):
            return hsl_to_hex(color)        
        elif (modeto.casefold() == "rgb"):
            return hsl_to_rgb(color)
        elif (modeto.casefold() == "cmy"):
            return hsl_to_cmy(color)
        elif (modeto.casefold() == "cmyk"):
            return hsl_to_cmyk(color)
        elif (modeto.casefold() == "hsv"):
            return hsl_to_hsv(color)
        elif (modeto.casefold() == "hsl"):
            return color
        
def lerp_color(fromcolor, frommode: str, tocolor, tomode: str, factor: float):
    """Lieary interpolate between two colors by factor. Result always in same mode as start color.
    `fromcolor`: str/list - color to interpolate from
    `frommode` - mode of start color
    `tocolor`: str/list - color to interpolate to
    `tomode` - mode of end color
    `factor` - lerp factor.
    Modes are: 'hex', 'rgb', 'cmy', 'cmyk', 'hsv' and 'hsl'."""
    if (frommode.casefold() != "rgb"):
        fromcolor = convert_color(fromcolor, frommode, "rgb")
    if (tomode.casefold() != "rgb"):
        tocolor = convert_color(tocolor, tomode, "rgb")
    result = [ round(lerp(fromcolor[0], tocolor[0], factor)),
               round(lerp(fromcolor[1], tocolor[1], factor)),
               round(lerp(fromcolor[2], tocolor[2], factor))]
    if (frommode.casefold() != "rgb"):
        result = convert_color(result, "rgb", frommode)
    return result
    
        
class Color():
    """A color in of modes: HEX, RGB, CMY, CMYK, HSV or HSL.
    `value`: list - color value
    `mode`: str - color mode.
    HEX - string in format '#RRGGBB' where RR, GG and BB are hex numbers;
    RGB - list in format [R, G, B] where R, G and B are integers in range [0, 255];
    CMY - list in format [C, M, Y] where C, M and Y are floats in range [0, 1];
    CMYK - list in format [C, M, Y, K] where C, M, Y and K are floats in range [0, 1];
    HSV - list in format [H, S, V] where H are float in range [0, 360], S and V are ints in range [0, 100];
    HSL - list in format [H, S, L] where H are float in range [0, 360], S and L are ints in range [0, 100]."""
    def __init__(self, value, mode: str):
        """Create a new Color object.
        `value`: str/list - color value, str for HEX mode and list/tuple otherwise.
        `mode` - color mode.
        Modes are 'hex', 'rgb', 'cmy', 'cmyk', 'hsv' or 'hsl'."""
        if (not isinstance(value, (str, list, tuple))):
            raise TypeError("`value` must be a str for hex mode or list/tuple otherwise.")
        if (mode.casefold() not in ("hex", "rgb", "cmy", "cmyk", "hsv", "hsl")):
            raise ValueError("`mode` must be 'hex', 'rgb', 'cmy', 'cmyk', 'hsv' or 'hsl'")
        self.value = value
        if (isinstance(self.value, tuple)):
            self.value = list(self.value)
        self.mode = mode.casefold()
        if (not Color.validate(self.value, self.mode)):
            if (self.mode == "hex"):
                raise ValueError("'hex' color must be a '#RRGGBB' string where RR, GG and BB are hex numbers.")
            elif (self.mode == "rgb"):
                raise ValueError("'rgb' color must be a [R, G, B] list/tuple where R, G and B are integers in range [0, 255].")
            elif (self.mode == "cmy"):
                raise ValueError("'cmy' color must be a [C, M, Y] list/tuple where C, M and Y are floats in range [0, 1].")
            elif (self.mode == "cmyk"):
                raise ValueError("'cmyk' color must be a [C, M, Y,K] list/tuple where C, M, Y and K are floats in range [0, 1].")
            elif (self.mode == "hsv"):
                raise ValueError("'hsv' color must be a [H, S, V] list/tuple where H are float in range [0, 360], S and V are ints in range [0, 100].")
            elif (self.mode == "hsl"):
                raise ValueError("'hsl' color must be a [H, S, L] list/tuple where H are float in range [0, 360], S and V are ints in range [0, 100].")                        
        
    def __str__(self):
        if (self.mode == "hex"):
            return self.value
        else:
            if (self.mode == "cmyk"):
                return "{} {} {} {}".format(*self.value)
            else:
                return "{} {} {}".format(*self.value)
            
    def __add__(self, other):
        if (isinstance(other, self.__class__)):
            if (self.mode != other.mode):
                other = Color(convert_color(other.value, other.mode, self.mode), self.mode)
            if (self.mode == "hex"):
                value = "#%02X%02X%02X" % (int(self.value[1:3] + other.value[1:3], 16), int(self.value[3:5] + other.value[3:5], 16), int(self.value[5:7] + other.value[5:7], 16))
            else:
                value = []
                for i, v in enumerate(self.value):
                    value.append(v + other.value[i])
            try:
                return Color(value, self.mode)
            except ValueError:
                raise ValueError("Result is invalid.")
        else:
            raise TypeError("`other` must be a Color object.")
    
    def __iadd__(self, other):
        c = self + other
        self.value = c.value
    
    def __sub__(self, other):
        if (isinstance(other, self.__class__)):
            if (self.mode != other.mode):
                other = Color(convert_color(other.value, other.mode, self.mode), self.mode)
            if (self.mode == "hex"):
                value = "#%02X%02X%02X" % (int(self.value[1:3] - other.value[1:3], 16), int(self.value[3:5] - other.value[3:5], 16), int(self.value[5:7] - other.value[5:7], 16))
            else:
                value = []
                for i, v in enumerate(self.value):
                    value.append(v - other.value[i])            
            try:
                return Color(value, self.mode)
            except ValueError:
                raise ValueError("Result is invalid.")
        else:
            raise TypeError("`other` must be a Color object.")
        
    def __isub__(self, other):
        c = self - other
        self.value = c.value    
        
    def __mul__(self, other):
        if (isinstance(other, self.__class__)):
            if (self.mode != other.mode):
                other = Color(convert_color(other.value, other.mode, self.mode), self.mode)
            if (self.mode == "hex"):
                value = "#%02X%02X%02X" % (int(self.value[1:3] * other.value[1:3], 16), int(self.value[3:5] * other.value[3:5], 16), int(self.value[5:7] * other.value[5:7], 16))
            else:
                value = []
                for i, v in enumerate(self.value):
                    value.append(v * other.value[i])            
            try:
                return Color(value, self.mode)
            except ValueError:
                raise ValueError("Result is invalid.")
        else:
            raise TypeError("`other` must be a Color object.")
        
    def __imul__(self, other):
        c = self * other
        self.value = c.value    
        
    def __div__(self, other):
        if (isinstance(other, self.__class__)):
            if (self.mode != other.mode):
                other = Color(convert_color(other.value, other.mode, self.mode), self.mode)
            if (self.mode == "hex"):
                value = "#%02X%02X%02X" % (int(self.value[1:3] // other.value[1:3], 16), int(self.value[3:5] // other.value[3:5], 16), int(self.value[5:7] // other.value[5:7], 16))
            else:
                value = []
                for i, v in enumerate(self.value):
                    if (self.mode == "rgb"):
                        value.append(v // other.value[i])
                    else:
                        value.append(v / other.value[i])             
            try:
                return Color(value, self.mode)
            except ValueError:
                raise ValueError("Result is invalid.")
        else:
            raise TypeError("`other` must be a Color object.")
        
    def __idiv__(self, other):
        c = self / other
        self.value = c.value    
        
    def __invert__(self):
        c = Color(self.value.copy(), self.mode)
        if (c.mode == "hex"):
            c.value = "#%02X%02X%02X" % (255 - int(c.value[1:3], 16), 255 - int(c.value[3:5], 16), 255 - int(c.value[5:7], 16))
        elif (c.mode == "rgb"):
            c.value = [255 - c.value[0], 255 - c.value[1], 255 - c.value[2]]
        elif ("cmy" in c.mode):
            value = []
            for v in c.value:
                value.append(1.0 - v)
            c.value = value
        else:
            value = []
            for i, v in enumerate(c.value):
                if (i == 0):
                    value.append(360 - v)
                else:
                    value.append(100 - v)
            c.value = value
        return c
    
    @property
    def hex(self):
        """Get this color in HEX mode."""
        return convert_color(self.value, self.mode, "hex")
    
    @property
    def rgb(self):
        """Get this color in RGB mode."""
        return convert_color(self.value, self.mode, "rgb")
    
    @property
    def cmy(self):
        """Get this color in CMY mode."""
        return convert_color(self.value, self.mode, "cmy")
    
    @property
    def cmyk(self):
        """Get this color in CMYK mode."""
        return convert_color(self.value, self.mode, "cmyk")
    
    @property
    def hsv(self):
        """Get this color in HSV mode."""
        return convert_color(self.value, self.mode, "hsv")
    
    @property
    def hsl(self):
        """Get this color in HSL mode."""
        return convert_color(self.value, self.mode, "hsl")
    
    @staticmethod
    def validate(color, mode: str) -> bool:
        """Validate `color` with `mode`."""
        if (mode.casefold() == "hex"):
            if (isinstance(color, str)):
                if (len(color) == 7):
                    if (re.match("#[A-Fa-f0-9]{6}", color)):
                        return True
        elif (mode.casefold() == "rgb"):
            if (isinstance(color, (list, tuple))):
                if (len(color) == 3):
                    if (0 <= color[0] <= 255 and 0 <= color[1] <= 255 and 0 <= color[2] <= 255):
                        return True
        elif (mode.casefold() == "cmy"):
            if (isinstance(color, (list, tuple))):
                if (len(color) == 3):
                    if (0.0 <= color[0] <= 1.0 and 0.0 <= color[1] <= 1.0 and 0.0 <= color[2] <= 1.0):
                        return True
        elif (mode.casefold() == "cmyk"):
            if (isinstance(color, (list, tuple))):
                if (len(color) == 4):
                    if (0.0 <= color[0] <= 1.0 and 0.0 <= color[1] <= 1.0 and 0.0 <= color[2] <= 1.0 and 0.0 <= color[3] <= 1.0):
                        return True
        elif (mode.casefold() in ("hsv", "hsl")):
            if (isinstance(color, (list, tuple))):
                if (len(color) == 3):
                    if (0 <= color[0] <= 360 and 0 <= color[1] <= 100 and 0 <= color[2] <= 100):
                        return True        
        return False
    
    def to_hex(self):
        """Convert this color to HEX mode."""
        if (self.mode != "hex"):
            self.value = self.hex
            self.mode = "hex"            
        
    def to_rgb(self):
        """Convert this color to RGB mode."""
        if (self.mode != "rgb"):
            self.value = self.rgb
            self.mode = "rgb"
            
    def to_cmy(self):
        """Convert this color to CMY mode."""
        if (self.mode != "cmy"):
            self.value = self.cmy
            self.mode = "cmy"            
        
    def to_cmyk(self):
        """Convert this color to CMYK mode."""
        if (self.mode != "cmyk"):
            self.value = self.cmyk
            self.mode = "cmyk"
            
    def to_hsv(self):
        """Convert this color to HSV mode."""
        if (self.mode != "hsv"):
            self.value = self.hsv
            self.mode = "hsv"            
        
    def to_hsl(self):
        """Convert this color to HSL mode."""
        if (self.mode != "hsl"):
            self.value = self.hsl
            self.mode = "hsl"
            
    def lerp(self, color, factor: float):
        """Lieary interpolate between two colors by factor. Result always in same mode as start color.
        `color`: str/list - color to interpolate to
        `factor` - lerp factor."""
        self.value = lerp_color(self.value, self.mode, color.value, color.mode, factor)
        
    def lerped(self, color, factor):
        """Get this lerped copy of this color."""
        c = Color(self.value.copy(), self.mode)
        c.lerp(color, factor)
        return c
    
    def invert(self):
        """Invert this color."""
        c = ~self
        self.value = c.value
        
    def inverted(self):
        """Get inverted copy of this color."""
        return ~self