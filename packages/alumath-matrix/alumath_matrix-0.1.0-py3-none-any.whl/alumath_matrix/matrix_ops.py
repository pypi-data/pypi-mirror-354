class Matrix:
    def __init__(self, data):
        if not all(len(row) == len(data[0]) for row in data):
            raise ValueError("All rows must have the same length!")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Columns of A must match rows of B!")
        
        result = [
            [sum(a * b for a, b in zip(row, col)) 
            for col in zip(*other.data)
        ] for row in self.data]
        
        return Matrix(result)

    def __repr__(self):
        return f"Matrix({self.data})"

A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])


C = A @ B

print("Matrix A:")
print(A)
print("\nMatrix B:")
print(B)
print("\nMatrix A @ B:")
print(C)