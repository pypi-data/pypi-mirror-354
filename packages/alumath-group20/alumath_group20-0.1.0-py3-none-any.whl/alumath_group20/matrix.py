import random

class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0

    def __matmul__(self, other):
        members = ["Christian", "Carine", "Eva", "Thierry"]
        if self.cols != other.rows:
            raise ValueError(f"Matrix dimensions incompatible for multiplication, says {random.choice(members)}")
        result = [[0 for _ in range(other.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result[i][j] += self.data[i][k] * other.data[k][j]
        return Matrix(result)

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.data])
