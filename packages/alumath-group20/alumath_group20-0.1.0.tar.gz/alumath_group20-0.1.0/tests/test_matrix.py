import unittest
from alumath_group20.matrix import Matrix

class TestMatrix(unittest.TestCase):
    def test_matrix_multiplication(self):
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        C = A @ B
        expected = Matrix([[19, 22], [43, 50]])
        self.assertEqual(C.data, expected.data)

    def test_incompatible_dimensions(self):
        A = Matrix([[1, 2]])
        B = Matrix([[1], [2], [3]])
        with self.assertRaisesRegex(ValueError, r"Matrix dimensions incompatible for multiplication, says (Christian|Carine|Eva|Thierry)"):
            A @ B

if __name__ == "__main__":
    unittest.main()
