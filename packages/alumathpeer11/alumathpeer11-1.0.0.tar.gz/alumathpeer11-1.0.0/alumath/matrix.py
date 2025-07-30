"""
alumathpeer11 Core - Matrix operations without external dependencies
"""

class Matrix:
    def __init__(self, data):
        """Initialize matrix with 2D list data"""
        if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
            raise ValueError("Matrix data must be a 2D list")
        
        if not data or not data[0]:
            raise ValueError("Matrix cannot be empty")
        
        # Check if all rows have same length
        row_length = len(data[0])
        if not all(len(row) == row_length for row in data):
            raise ValueError("All rows must have the same length")
        
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])
    
    def __repr__(self):
        return f"Matrix({self.rows}x{self.cols})"
    
    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.data])
    
    def get(self, row, col):
        """Get element at position (row, col)"""
        return self.data[row][col]
    
    def set(self, row, col, value):
        """Set element at position (row, col)"""
        self.data[row][col] = value
    
    def multiply(self, other):
        """Matrix multiplication using efficient loops"""
        if not isinstance(other, Matrix):
            raise TypeError("Can only multiply with another Matrix")
        
        if self.cols != other.rows:
            raise ValueError(f"Cannot multiply {self.rows}x{self.cols} with {other.rows}x{other.cols}")
        
        # Initialize result matrix with zeros
        result_data = [[0 for _ in range(other.cols)] for _ in range(self.rows)]
        
        # Efficient matrix multiplication using three nested loops
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result_data[i][j] += self.data[i][k] * other.data[k][j]
        
        return Matrix(result_data)
    
    def __mul__(self, other):
        """Overload * operator for matrix multiplication"""
        return self.multiply(other)
    
    def transpose(self):
        """Return transposed matrix"""
        transposed_data = [[self.data[i][j] for i in range(self.rows)] 
                          for j in range(self.cols)]
        return Matrix(transposed_data)
    
    def to_list(self):
        """Return matrix as 2D list"""
        return [row[:] for row in self.data]

def create_matrix(data):
    """Convenience function to create a matrix"""
    return Matrix(data)

def identity_matrix(size):
    """Create identity matrix of given size"""
    data = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    return Matrix(data)

def zero_matrix(rows, cols):
    """Create zero matrix of given dimensions"""
    data = [[0 for _ in range(cols)] for _ in range(rows)]
    return Matrix(data)
