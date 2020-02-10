from matrix import Matrix

class Graph():
    """A graph structure."""
    def __init__(self):
        """Create a new Graph object."""
        self._vertices = []
        self._edges = Matrix(0, 0)
        self._oriented = False
        self._weighted = False
        
    @property
    def oriented(self):
        return self._oriented
    
    @oriented.setter
    def oriented(self, value: bool):
        """Get/set whether this graph is oriented or not.
        If previously oriented graph will become not oriented all connected vertices will be connected both ways."""
        value = bool(value)
        if (self._oriented != value):
            self._oriented = value
            if (not self._oriented):
                for i in range(self._edges.rows):
                    for j in range(i + 1, self._edges.columns):
                        if (self._edges[i][j] != 0.0):
                            self._edges[j][i] = self._edges[i][j]
                        elif (self._edges[j][i] != 0.0):
                            self._edges[i][j] = self._edges[j][i]
                        
    @property
    def weighted(self):
        return self._weighted
    
    @weighted.setter
    def weighted(self, value: bool):
        """Get/set whether this graph is weighted or not.
        If previously weighted graph will become not weighted all connected vertices will have 1.0 weights."""
        value = bool(value)
        if (self._weighted != value):
            self._weighted = value
            if (not self._weighted):
                for i in range(self._edges.rows):
                    for j in range(self._edges.columns):
                        if (self._edges[i][j] != 0.0):
                            self._edges[i][j] = 1.0
                            
    def __len__(self):
        """Get count of vertices."""
        return len(self._vertices)
    
    def __contains__(self, vertex):
        """Whether vertex in graph or not."""
        return self.find(vertex) != -1
        
    def append(self, vertex):
        """Add given vertex to graph."""
        self._vertices.append(vertex)
        self._edges.resize(self._edges.rows + 1, self._edges.columns + 1)
        
    def remove(self, vertex):
        """Remove first occurrence of given vertex. Raises ValueError if vertex is not found."""
        idx = self.find(vertex)
        if (idx != -1):
            self._vertices.pop(idx)
            self._edges.removeRow(idx)
            try:
                self._edges.removeColumn(idx)
            except RuntimeError:
                pass
        else:
            raise ValueError("Given vertex is not in graph!")
        
    def find(self, vertex):
        """Get lowest index of given vertex. Returns -1 if not found."""
        try:
            return self._vertices.index(vertex)
        except ValueError:
            return -1
        
    def connect(self, vtx1, vtx2, weight: float=1.0):
        """Connect given vertices with given weight.
        Raises ValueError if:
        - weight is not 1.0 while graph is not weighted;
        - given weight is <= 0.0;
        - given vertices are same;
        - one of given vertices is not found."""
        if (weight != 1.0):
            if (not self._weighted):
                raise ValueError("Cannot set weight while graph is not weighted, consider changing property `weighted` before!")
            if (weight <= 0.0):
                raise ValueError("Weight cannot be <= 0.0!")
        if (vtx1 == vtx2):
            raise ValueError("Cannot connect vertex to itself!")
        idx1 = self.find(vtx1)
        idx2 = self.find(vtx2)
        if (idx1 == -1):
            raise ValueError("Given vertex 1 is not in graph!")
        if (idx2 == -1):
            raise ValueError("Given vertex 2 is not in graph!")        
        self._edges[idx1][idx2] = weight
        if (not self._oriented):
            self._edges[idx2][idx1] = weight
            
    def disconnect(self, vtx1, vtx2):
        """Disconnect given vertices.
        Raises ValueError if:
        - given vertices are same;
        - one of given vertices is not found."""
        if (vtx1 == vtx2):
            raise ValueError("Cannot disconnect vertex from itself!")
        idx1 = self.find(vtx1)
        idx2 = self.find(vtx2)
        if (idx1 == -1):
            raise ValueError("Given vertex 1 is not in graph!")
        if (idx2 == -1):
            raise ValueError("Given vertex 2 is not in graph!")
        self._edges[idx1][idx2] = 0.0
        if (not self._oriented):
            self._edges[idx2][idx1] = 0.0
            
    def weight(self, vtx1, vtx2) -> float:
        """Get weight between given vertices.
        Raises ValueError if:
        - given vertices are same;
        - one of given vertices is not found."""
        if (vtx1 == vtx2):
            raise ValueError("Cannot get weigth between vertex and itself!")
        idx1 = self.find(vtx1)
        idx2 = self.find(vtx2)
        if (idx1 == -1):
            raise ValueError("Given vertex 1 is not in graph!")
        if (idx2 == -1):
            raise ValueError("Given vertex 2 is not in graph!")
        return self._edges[idx1][idx2]
    
    def connected(self, vtx1, vtx2) -> bool:
        """Whether given vertices are connected or not.
        Raises ValueError if:
        - given vertices are same;
        - one of given vertices is not found."""
        try:
            return self.weight(vtx1, vtx2) != 0.0
        except ValueError:
            raise
