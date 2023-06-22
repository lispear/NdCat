from typing import Sequence, Tuple
import numpy
from sympy import Matrix

from .extension import Extension

class LaplaceExtension(Extension):
    """
    LaplaceExtension class that extends the cat matrix using laplace expansions algorithm.

    """
    @staticmethod
    def check_parameters(dim: int, *args: Sequence) -> int:
        """
        Checks the validity of input parameters.

        Args:
            dim (int): The dimension of the cat matrix.
            *args (Sequence): Input data sequences.

        Returns:
            int: The number of iterations.

        Raises:
            ValueError: If the dimension is less than or equal to 1 or the input data does not match the required size.

        """
        if dim <= 1:
            raise ValueError("Dimension must be greater than 1")

        iterations = dim - 1
        required = (dim - 1) * dim + 2 * (dim - 1)
        actual = sum(sum(len(seq) for seq in args[i]) for i in range(2)) + sum(len(args[i]) for i in range(2, 4))

        if required != actual:
            raise ValueError(f"Input data does not match required size. Required size: {required}, Actual size: {actual}")
        return iterations

    @classmethod
    def create(cls, dim: int, rows: Sequence[Sequence[int]], cols: Sequence[Sequence[int]], rows_loc: Sequence[int], cols_loc: Sequence[int]) -> numpy.ndarray:
        """
        Creates a cat matrix using the Laplace-based algorithm.

        Args:
            dim (int): The dimension of the cat matrix.
            rows (Sequence[Sequence[int]]): The rows of the cat matrix.
            cols (Sequence[Sequence[int]]): The columns of the cat matrix.
            rows_loc (Sequence[int]): The locations of the rows in the cat matrix.
            cols_loc (Sequence[int]): The locations of the columns in the cat matrix.

        Returns:
            numpy.ndarray: The created cat matrix.

        Raises:
            ValueError: If the dimension is less than or equal to 1 or the input data does not match the required size.

        """
        iterations = cls.check_parameters(dim, rows, cols, rows_loc, cols_loc)

        cat = numpy.array([[1]])

        for i in range(iterations):
            cat = cls.extend(cat, rows[i], cols[i], rows_loc[i], cols_loc[i])

        return cat.astype(numpy.int64)

    @classmethod
    def extend(cls, matrix: Sequence[Sequence[int]], row: Sequence[int], col: Sequence[int], row_loc: int, col_loc: int) -> numpy.ndarray:
        """
        Extends the cat matrix using the Laplace-based algorithm.

        Args:
            matrix (Sequence[Sequence[int]]): The input cat matrix.
            row (Sequence[int]): The row elements to extend.
            col (Sequence[int]): The column elements to extend.
            row_loc (int): The location of the rows in the cat matrix.
            col_loc (int): The location of the columns in the cat matrix.

        Returns:
            numpy.ndarray: The extended cat matrix.

        """
        diag1 = numpy.asarray(matrix[:row_loc, :col_loc], dtype=numpy.int64)
        diag2 = numpy.asarray(matrix[row_loc:, col_loc:], dtype=numpy.int64)
        off_diag1 = numpy.asarray(matrix[:row_loc, col_loc:], dtype=numpy.int64)
        off_diag2 = numpy.asarray(matrix[row_loc:, :col_loc], dtype=numpy.int64)

        top = numpy.asarray(row[:row_loc], dtype=numpy.int64).reshape(row_loc, 1)
        bottom = numpy.asarray(row[row_loc:], dtype=numpy.int64).reshape(off_diag2.shape[0])
        left = numpy.asarray(col[:col_loc], dtype=numpy.int64).reshape(1, col_loc)
        right = numpy.asarray(col[col_loc:], dtype=numpy.int64).reshape(1, off_diag1.shape[1])

        cat: numpy.ndarray = numpy.r_[(numpy.c_[diag1, top, off_diag1]), (numpy.c_[left, 0, right]), (numpy.c_[off_diag2, bottom, diag2])]
        cat[row_loc][col_loc] = (-1) ** (row_loc + col_loc) * (1 - cls.cofactors(cat, row_loc, col_loc))

        return cat.astype(numpy.int64)

    @classmethod
    def random(cls, dim: int, low: int, high: int) -> numpy.ndarray:
        """
        Generates a random cat matrix using the block-based algorithm.

        Args:
            dim (int): The dimension of the cat matrix.
            low (int): The lower bound (inclusive) for random element generation.
            high (int): The upper bound (exclusive) for random element generation.

        Returns:
            numpy.ndarray: The generated random cat matrix.

        """
        rows = [numpy.random.randint(low, high, i, dtype=numpy.int64) for i in range(1, dim)]
        cols = [numpy.random.randint(low, high, i, dtype=numpy.int64) for i in range(1, dim)]
        rows_loc = [numpy.random.randint(0, i + 1) for i in range(1, dim)]
        cols_loc = [numpy.random.randint(0, i + 1) for i in range(1, dim)]
        return cls.create(dim, rows, cols, rows_loc, cols_loc) 
        
    @classmethod
    def split_sequence(cls, dim: int, source: Sequence) -> Tuple[Sequence, ...]:
        """
        Splits the input sequence into individual components.

        Args:
            dim (int): The dimension of the cat matrix.
            source (Sequence): The input sequence.

        Returns:
            Tuple[Sequence, ...]: The split sequences.

        """
        rows_size = (dim - 1) * dim // 2
        iterations = (dim - 1)
        return source[:rows_size], source[rows_size: 2 * rows_size], source[-2 * iterations: -iterations], source[-iterations:]

    @staticmethod
    def cofactors(cat: numpy.ndarray, r: int, c: int) -> int:
        """
        Calculates the cofactors of the given element in the cat matrix.

        Args:
            cat (numpy.ndarray): The cat matrix.
            r (int): The row index.
            c (int): The column index.

        Returns:
            int: The sum of the cofactors.

        """
        matrix = Matrix(cat)
        cofactor_sum = 0
        for i in range(cat.shape[0]):
            if i != r:
                cofactor_sum += cat[i][c] * matrix.cofactor(i, c)
        return cofactor_sum
