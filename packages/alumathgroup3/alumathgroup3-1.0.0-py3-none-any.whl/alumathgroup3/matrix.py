class Matrix:
    
    def __init__(self, data):

        if not isinstance(data, (list, tuple)):
            raise ValueError("Group 3 says: Matrix data must be a list or tuple")
        
        if not data:
            raise ValueError("Group 3 says: Matrix cannot be empty")
        
        # Convert to list of lists
        if isinstance(data[0], (int, float)):
            # Single row matrix
            self.data = [list(data)]
        else:
            self.data = [list(row) for row in data]
        
        # Validate matrix dimensions
        self.rows = len(self.data)
        self.cols = len(self.data[0]) if self.data else 0
        
        
        for i, row in enumerate(self.data):
            # Check all rows have same length
            if len(row) != self.cols:
                raise ValueError(f"Group 3 says: All rows must have the same length. Row {i} has {len(row)} elements, expected {self.cols}")
            # Check all elements are numbers
            for j, element in enumerate(row):
                if not isinstance(element, (int, float)):
                    raise ValueError(f"Group 3 says: All elements must be numbers. Element at ({i}, {j}) is {type(element).__name__}")
    
    def __repr__(self):
        """ Clean Representation Of the Matrix """

        max_width = max(len(str(element)) for row in self.data for element in row)
        rows = []
        for row in self.data:
            formatted_row = [f"{element:>{max_width}}" for element in row]
            rows.append("│ " + " ".join(formatted_row) + " │")
        return "\n".join(rows)
    
    def shape(self):
        """Return matrix dimensions as (rows, columns)."""
        return (self.rows, self.cols)
    
    def multiply(self, other):
       
        # Validation
        if not isinstance(other, Matrix):
            raise TypeError("Group 3 can only multiply with another Matrix instance")
        
        if self.cols != other.rows:
            raise ValueError(f"Groupp 3 cannot multiply matrices with shapes {self.shape()} and {other.shape()}. "
                           f"Columns of first matrix ({self.cols}) must equal rows of second matrix ({other.rows})")
        
        # Matrix multiplication
        result = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                # Dot product of row i and column j
                dot_product = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                row.append(dot_product)
            result.append(row)
        
        return Matrix(result)
    
    def __mul__(self, other):
        """Enable * operator for matrix multiplication."""
        return self.multiply(other)


def matrix_multiply(matrix1, matrix2):
    """
    Standalone function for matrix multiplication.
    
    Returns:
        Matrix: Result of multiplication
    """
    if not isinstance(matrix1, Matrix):
        raise TypeError("Group 3 says: both arguments must be Matrix instances")
    return matrix1.multiply(matrix2)




# Display success message if executed directly
if __name__ == "__main__":
    print("AlumMath Group 3 Matrix Multiplication Library installed successfully")