from struct import pack, unpack, calcsize
from math import sin, cos, radians

from vector import Vector

class ZeroDeterminantException(Exception):
    """Exception in case of zero determinant."""
    def __init__(self):
        super().__init__("Matrix determinant is zero!")

class WrongDimensionsException(Exception):
    """Exception in case of wrong matrix dimension."""
    def __init__(self, message: str=""):
        super().__init__("Matrix have wrong dimensions! " + message)

class Matrix():
    """Class representing mathematical Matrix."""
    def __init__(self, rows: int, columns: int):
        """Create a new Matrix object. `rows` - count of rows in this matrix, `columns` - count of columns in this matrix."""
        if(rows < 0 or columns < 0):
            raise ValueError("Matrix cannot have negative dimensions!")
        self._rows = rows
        self._columns = columns
        self._mat = [Vector([0.0 for j in range(self._columns)]) for i in range(self._rows)]
        
    @property
    def rows(self):
        return self._rows
    
    @rows.setter
    def rows(self, value: int):
        """Get/set row count of this matrix."""
        if (self._rows != int(value)):
            self.resize(rows=int(value))
        
    @property
    def columns(self):
        return self._columns
    
    @columns.setter
    def columns(self, value: int):
        """Get/set column count of this matrix."""
        if (self._columns != int(value)):
            self.resize(columns=int(value))
            
    @staticmethod
    def identity(size: int):
        """Create and return a new identity Matrix of given size (all elements are 0.0 except main diagonal - they are 1.0)."""
        out = Matrix(size, size)
        for i in range(size):
            out[i][i] = 1.0
        return out
    
    @staticmethod
    def minor(mat, i: int, j: int):
        """Get minor of given matrix (given matrix without `i`-th row and `j`-th column)."""
        if ((i >= mat.rows or i < 0) or (j >= mat.columns or j < 0)):
            raise IndexError
        m = mat.copy()
        m._rows -= 1
        m._columns -= 1
        mat = m._mat[:i]
        mat.extend(m._mat[i+1:])
        m._mat = mat.copy()
        for i, row in enumerate(m._mat):
            r = row[:j]
            r.extend(row[j+1:])
            m._mat[i] = r.copy()
        return m
    
    @staticmethod
    def determinant(mat) -> float:
        """Get determinant of given matrix."""
        if (mat.columns != mat.rows):
            raise WrongDimensionsException("Matrix must be square to find determinant!")
        if (mat.rows < 1):
            raise WrongDimensionsException("One or all dimensions of matrix is zero!")
        if (mat.rows == 1):
            return mat._mat[0][0]
        elif (mat.rows == 2):
            return mat._mat[0][0] * mat._mat[1][1] - mat._mat[0][1] * mat._mat[1][0]
        else:
            d = 0
            for i in range(mat.rows):
                m = Matrix.minor(mat, i, 0)
                d += (-1)**i * mat[i][0] * Matrix.determinant(m)
            return d
                    
    @staticmethod
    def gauss(mat, vec: Vector) -> Vector:
        """Solve a system of linear equations with Gauss method. Requires matrix and a vector. Returns vector of results."""
        if (len(vec) != mat.rows):
            raise ValueError("Vector must have same length as matrix row count to perform this operation!")
        m = mat.copy()
        m.insert_column(vec, m.columns)
        m.to_lower_triangle()
        result = Vector([0.0 for i in range(len(vec))])
        for i in range(m.rows - 1, -1, -1):
            summ = 0.0
            for j in range(m.columns - 2, i, -1):
                summ += m[i][j] * result[j]
            result[i] = (m[i][m.columns - 1] - summ) / m[i][i]
        return result    
        
    @staticmethod
    def _column_max(mat, col: int) -> float:
        """[INTERNAL] get maximum element in given column of given matrix."""
        mx = abs(mat[col][col])
        max_idx = col
        for i in range(col + 1, mat.rows):
            e = abs(mat[i][col])
            if (e > mx):
                mx = e
                max_idx = i
        return max_idx
    
    @staticmethod
    def make_translation(dx: float, dy: float, dz: float=None):
        """Make translation matrix 2d or 3d if dz is given."""
        if (dz == None):
            mat = Matrix.identity(3)
            mat[0][2] = dx
            mat[1][2] = dy
        else:
            mat = Matrix.identity(4)
            mat[0][3] = dx
            mat[1][3] = dy
            mat[2][3] = dz
        return mat
    
    @staticmethod
    def make_rotation(angle_x: float, angle_y: float, angle_z: float=None):
        """Make rotation matrix 2d or 3d if angle_z is given."""
        mat_x = Matrix.identity(3)
        mat_x[1][1] = cos(radians(angle_x))
        mat_x[1][2] = -sin(radians(angle_x))
        mat_x[2][1] = sin(radians(angle_x))
        mat_x[2][2] = cos(radians(angle_x))
        mat_y = Matrix.identity(3)
        mat_y[0][0] = cos(radians(angle_y))
        mat_y[0][2] = sin(radians(angle_y))
        mat_y[2][0] = -sin(radians(angle_y))
        mat_y[2][2] = cos(radians(angle_y))
        mat_z = Matrix.identity(3)
        if (angle_z != None):
            mat_z[0][0] = cos(radians(angle_z))
            mat_z[0][1] = -sin(radians(angle_z))
            mat_z[1][0] = sin(radians(angle_z))
            mat_z[1][1] = cos(radians(angle_z))
        mat = mat_x * mat_y * mat_z
        return mat
    
    @staticmethod
    def make_scale(x: float, y: float, z: float=None):
        """Make scale matrix 2d or 3d if z is given."""
        if (z == None):
            mat = Matrix.identity(3)
            mat[0][0] = x
            mat[1][1] = y
        else:
            mat = Matrix.identity(4)
            mat[0][0] = x
            mat[1][1] = y
            mat[2][2] = z
        return mat
        
    def __getitem__(self, key):
        """Get row at `key` pos."""
        return self._mat[key]
    
    def __setitem__(self, key, value):
        """Set row at `key` pos."""
        if (len(value) == self._columns):
            if (isinstance(value, (list, tuple))):
                self._mat[key] = Vector(value)
            elif (isinstance(value, Vector)):
                self._mat[key] = value
            else:
                raise TypeError("`value` must be list, tuple or Vector object.")
        else:
            raise ValueError("`value` must have same length as matrix column count.")
            
    def __iter__(self):
        """Iterate through all elements of matrix."""
        for row in self._mat:
            for e in row:
                yield e
            
    def __str__(self):
        """String representaion of this matrix."""
        out = "Matrix("
        max_len = 0
        negs = False
        for row in self._mat:
            for e in row:
                if (len(str(int(e))) > max_len):
                    max_len = len(str(abs(int(e))))
                if (not negs and e < 0):
                    negs = True
        for i, row in enumerate(self._mat):
            for j, e in enumerate(row):
                out += ("%" + str(max_len + 3 + (1 if e >= 0.0 and negs else 0)) + ".2f") % e
                if (j != len(row) - 1):
                    out += " "
            if (i != len(self._mat) - 1):
                out += "\n"
                out += " " * 7
        out += ")"
        return out
    
    def __eq__(self, other):
        """Whether two matrices are equal."""
        if (not isinstance(other, Matrix)):
            raise TypeError("Only matrices can be compared!")
        return self._mat == other._mat
    
    def __add__(self, other):
        """Add matrix or number to another and return it."""
        m = self.copy()
        if (isinstance(other, Matrix)):            
            if ((self._rows != other._rows) and (self._columns != other._columns)):
                raise WrongDimensionsException("Matrices must have equal size to perform this operation!")
            for i in range(m.rows):
                for j in range(m.columns):
                    m[i][j] += other[i][j]
        else:
            for i in range(m.rows):
                for j in range(m.columns):
                    m[i][j] += other
        return m
    
    def __iadd__(self, other):
        """Add matrix or number to another and set result to current matrix."""
        self._mat = (self + other)._mat
        
    def __sub__(self, other):
        """Subtract from matrix another matrix or number and return it."""
        m = self.copy()
        if (isinstance(other, Matrix)):            
            if ((self._rows != other._rows) and (self._columns != other._columns)):
                raise WrongDimensionsException("Matrices must have equal size to perform this operation!")
            for i in range(m.rows):
                for j in range(m.columns):
                    m[i][j] -= other[i][j]
        else:
            for i in range(m.rows):
                for j in range(m.columns):
                    m[i][j] -= other
        return m
    
    def __isub__(self, other):
        """Subtract from matrix another matrix or number set result to current matrix."""
        self._mat = (self - other)._mat
        
    def __mul__(self, other):
        """Multiply matrix by another matrix, sequence or number."""
        if (isinstance(other, (list, tuple, Vector))):
            if (self._rows != len(other)):
                raise ValueError("`other` must have length equal to matrix row count.")
            if (not isinstance(other, Vector)):
                other = Vector(other)
            result = Vector()
            for i in range(self.columns):
                result.append(0.0)
                for k in range(self.rows):
                    result[i] += self[k][i] * other[k]
            return result
        if (isinstance(other, Matrix)):
            m = Matrix(self._rows, other._columns)
            if (self._columns != other._rows):
                raise WrongDimensionsException("First matrix must have column count equal to second matrix's row count to perform this operation!")
            for i in range(m.rows):
                for j in range(other.columns):
                    m[i][j] = 0.0
                    for k in range(self.columns):
                        m[i][j] += self[i][k] * other[k][j]
        else:
            m = self.copy()
            for i in range(m.rows):
                for j in range(m.columns):
                    m[i][j] *= other
        return m
           
    def __rmul__(self, other):
        """Multiply to one matrix another matrix in reversed order or number and return it."""
        print("FUCK")
        if (isinstance(other, Matrix)):
            return other * self
        else:
            return self * other
        
    def __imul__(self, other):
        """Multiply to one matrix another matrix or number and set result to current matrix."""
        self._mat = (self * other)._mat
        
    def __div__(self, other):
        """Muliply one matrix by inversed matrix or 1/number and return it."""
        if (isinstance(other, Matrix)):
            return self * other.inversed()
        else:
            return self * (1/other)
        
    def __rdiv__(self, other):
        """Muliply one matrix by inversed matrix in reversed order or 1/number and return it."""
        if (isinstance(other, Matrix)):
            return other * self.inversed()
        else:
            return self / other
        
    def __idiv__(self, other):
        """Muliply one matrix by inversed matrix or 1/number and set result to current matrix."""
        self._mat = (self / other)._mat
        
    def __neg__(self):
        """Return negative matrix to current (negate every element)."""
        m = self.copy()
        for row in m._mat:
            for j, e in  enumerate(row):
                row[j] = -e
        return m
        
    def clear(self):
        """Clear this matrix."""
        self._mat.clear()
        self._rows = self._columns = 0
        
    def resize(self, rows: int=-1, columns: int=-1):
        """Resize this matrix to given sizes. -1 - do not resize."""
        if (rows > self._rows):
            if (self._columns > 0):
                self._mat = [Vector([0.0 for j in range(self._columns)]) for i in range(rows)]
            else:
                self._mat = [Vector([0.0]) for i in range(rows)]
                self._columns = 1
            self._rows = rows
        elif (0 < rows < self._rows):
            self._mat = self._mat[:rows]
            self._rows = rows
        elif (rows == 0):
            self.clear()
        if (columns > self._columns):
            if (self._rows == 0):
                self._mat.append([0.0])
                self._rows = 1
                self._columns = 1
            for row in self._mat:
                row.extend([0.0 for j in range(columns - self._columns)])
            self._columns = columns
        elif (0 < columns < self._columns):
            for i, row in enumerate(self._mat):
                self._mat[i] = row[:columns]
            self._columns = columns
        elif (columns == 0):
            self.clear()
            
    def copy(self):
        """Return a copy of this matrix."""
        m = Matrix(self._rows, self._columns)
        for i, row in enumerate(self._mat):
            m._mat[i] = row.copy()
        return m
            
    def transpose(self):
        """Transpose this matrix (turn rows into columns and vice versa.)."""
        m = Matrix(self._columns, self._rows)
        for i in range(self._rows):
            for j in range(self._columns):
                m[j][i] = self._mat[i][j]
        self._columns = m.columns
        self._rows = m.rows
        self._mat = m._mat.copy()
            
    def transposed(self):
        """Get transposed version of this matrix."""
        m = self.copy()
        m.transpose()
        return m
    
    def inverse(self):
        """Inverse this matrix."""
        d = self.get_determinant()
        if (d == 0):
            raise ZeroDeterminantException()
        t = self.transposed()
        out = self.copy()
        for i in range(out._rows):
            for j in range(out._columns):
                m = Matrix.minor(t, i, j)
                out[i][j] = 1/d * (-1) ** (i + j) * m.get_determinant()
        return out
    
    def inversed(self):
        """Get inversed version of this matrix."""
        m = self.copy()
        m.inverse()
        return m
    
    def to_lower_triangle(self):
        """Turn given matrix into lower triangle state (elements below main diagonal are 0.0)."""
        for i in range(self.rows - 1):
            max_idx = Matrix._column_max(self, i)
            if (i != max_idx):
                self.swap_rows(i, max_idx)
            for j in range(i + 1, self.rows):
                mul = -self[j][i] / self[i][i]
                for k in range(i, self.columns):
                    self[j][k] += self[i][k] * mul    
    
    def get_determinant(self) -> float:
        """Get determinant of this matrix (only for square matrix)."""
        return Matrix.determinant(self)
    
    def swap_rows(self, i1: int, i2: int):
        """Swap `i1`-th row and `i2`-th."""
        self._mat[i1], self._mat[i2] = self._mat[i2], self._mat[i1]
        
    def swap_columns(self, j1: int, j2: int):
        """Swap `j1`-th column and `j2`-th."""
        for row in self._mat:
            row[j1], row[j2] = row[j2], row[j1]
            
    def insert_row(self, vec: Vector, i: int):
        """Insert `vec` before `i`-th row."""
        if (len(vec) != self.columns):
            raise ValueError("`vec` must have length equal matrix column count!")
        if (isinstance(vec, (list, tuple, Vector))):
            if (not isinstance(vec, Vector)):
                vec = Vector(vec)
        else:
            raise TypeError("`vec` must be a list, tuple or Vector object.")
        self._mat.insert(i, vec)
        self._rows += 1
        
    def insert_column(self, vec: Vector, j: int):
        """Insert `vec` before `j`-th column."""
        if (len(vec) != self.rows):
            raise ValueError("`vec` must have length equal matrix row count!")
        if (not isinstance(vec, (list, tuple, Vector))):
            raise TypeError("`vec` must be a list, tuple or Vector object.")        
        for i, row in enumerate(self._mat):
            row.insert(j, vec[i])
        self._columns += 1
        
    def remove_row(self, i: int):
        """Remove `i`-th row. Raises IndexError if given invalid index. Raises RuntimeError if matrix is empty."""
        if (self.rows > 0):
            try:
                self._mat.pop(i)
                self._rows -= 1
                if (self._rows == 0):
                    self._columns = 0
            except IndexError:
                raise IndexError("There's no row #{0} in matrix!".format(i))
        else:
            raise RuntimeError("Matrix is empty!")
        
    def remove_column(self, j: int):
        """Remove `j`-th column. Raises IndexError if given invalid index. Raises RuntimeError if matrix is empty."""
        if (self.columns > 0):
            try:
                for row in self._mat:
                    row.pop(j)
                self._columns -= 1
                if (self._columns == 0):
                    self._rows = 0
            except IndexError:
                raise IndexError("There's no column #{0} in matrix!".format(j))
        else:
            raise RuntimeError("Matrix is empty!")  
            
    def rang(self) -> int:
        """Get rang of this matrix."""
        m = self.copy()
        Matrix.to_lower_triangle(m)
        rang = min(m.rows, m.columns)
        for row in m._mat:
            for e in row:
                if (abs(e) > 0.00001):
                    break
            else:
                rang -= 1
        return rang
    
    def write(self, filepath: str):
        """Write this matrix to binary file at given `filepath`."""
        with open(filepath, "wb") as f:
            f.write(pack("i", self.rows))
            f.write(pack("i", self.columns))
            for row in self._mat:
                for e in row:
                    f.write(pack("f", e))
                           
    def read(self, filepath: str):
        """Read matrix from binary file at given `filepath`."""
        self.clear()
        with open(filepath, "rb") as f:
            self.rows = unpack("i", f.read(calcsize("i")))[0]
            self.columns = unpack("i", f.read(calcsize("i")))[0]
            for i in range(self.rows):
                for j in range(self.columns):
                    self._mat[i][j] = unpack("f", f.read(calcsize("f")))[0]
                    
