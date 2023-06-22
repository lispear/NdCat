from itertools import islice
from typing import Iterator, Sequence, Tuple
import numpy

from .extension import Extension

class BlockExtension(Extension):
    """
    BlockExtension class that extends the cat matrix using block-based algorithm.

    """

    @staticmethod
    def check_parameters(dim: int, *args: Sequence[Sequence[int]]) -> int:
        """
        Checks the validity of input parameters.

        Args:
            dim (int): The dimension of the cat matrix.
            *args (Sequence[Sequence[int]]): Input data sequences.

        Returns:
            int: The number of iterations.

        Raises:
            ValueError: If the dimension is less than or equal to 1 or the input data does not match the required size.

        """
        if dim <= 1:
            raise ValueError("Dimension must be greater than 1")

        iterations = (dim - 1) // 2
        required = iterations * 2 + (dim ** 2) // 2
        actual = sum(len(seq) for seq in args)

        if required != actual:
            raise ValueError(f"Input data does not match required size. Required size: {required}, Actual size: {actual}")
        return iterations

    @classmethod
    def create(cls, dim: int, diag: Sequence[int], off_diag: Sequence[int], swap_diag: Sequence[bool], swap_off_diag: Sequence[bool]) -> numpy.ndarray:
        """
        Creates a cat matrix using the block-based algorithm.

        Args:
            dim (int): The dimension of the cat matrix.
            diag (Sequence[int]): The diagonal elements.
            off_diag (Sequence[int]): The off-diagonal elements.
            swap_diag (Sequence[bool]): Whether to swap the diagonal block matrix at each iteration.
            swap_off_diag (Sequence[bool]): Whether to swap the off-diagonal block matrix at each iteration.

        Returns:
            numpy.ndarray: The created cat matrix.

        Raises:
            ValueError: If the dimension is less than or equal to 1 or the input data does not match the required size.

        """
        iterations = cls.check_parameters(dim, diag, off_diag, swap_diag, swap_off_diag)

        diag_iter = iter(diag)
        off_diag_iter = iter(off_diag)

        c = (dim + 1) % 2 + 1
        if c == 1:
            cat = numpy.array([[1]])
        else:
            p, q = take(diag_iter, 2)
            cat = cls._diagonal_cat_matrix(p, q)

        for i in range(iterations):
            size = 2 * i + c
            cat = cls.extend(cat, take(diag_iter, 2), take(off_diag_iter, 2 * size), swap_diag[i], swap_off_diag[i])

        return cat.astype(numpy.int64)

    @classmethod
    def extend(cls, matrix: Sequence[Sequence[int]], diag: Sequence[int], off_diag: Sequence[int], swap_diag: bool, swap_off_diag: bool) -> numpy.ndarray:
        """
        Extends the cat matrix using the block-based algorithm.

        Args:
            matrix (Sequence[Sequence[int]]): The input cat matrix.
            diag (Sequence[int]): The diagonal elements.
            off_diag (Sequence[int]): The off-diagonal elements.
            swap_diag (bool): Whether to swap the diagonal block matrix.
            swap_off_diag (bool): Whether to swap the off-diagonal block matrix.

        Returns:
            numpy.ndarray: The extended cat matrix.

        """
        cat1 = cls._diagonal_cat_matrix(diag[0], diag[1])
        cat2 = numpy.asarray(matrix, dtype=numpy.int64)
        mat1 = numpy.asarray(off_diag, dtype=numpy.int64)
        mat2 = numpy.zeros_like(mat1, dtype=numpy.int64)

        if swap_diag:
            cat1, cat2 = cat2, cat1

        if swap_off_diag:
            mat1, mat2 = mat2, mat1

        return numpy.r_[(numpy.c_[cat1, mat1.reshape(cat1.shape[0], -1)]), (numpy.c_[mat2.reshape(cat2.shape[0], -1), cat2])]

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
        diag_size = (dim // 2) * 2
        off_diag_size = dim ** 2 // 2 - diag_size
        swap_size = (dim - 1) // 2
        diag = numpy.random.randint(low, high, diag_size, dtype=numpy.int64)
        off_diag = numpy.random.randint(low, high, off_diag_size, dtype=numpy.int64)
        swap_diag = numpy.random.choice([True, False], size=swap_size)
        swap_off_diag = numpy.random.choice([True, False], size=swap_size)
        return cls.create(dim, diag, off_diag, swap_diag, swap_off_diag)

    @classmethod
    def split_sequence(cls, dim: int, data: Sequence) -> Tuple[Sequence, ...]:
        """
        Splits the input sequence into individual components.

        Args:
            dim (int): The dimension of the cat matrix.
            data (Sequence): The input sequence.

        Returns:
            Tuple[Sequence, ...]: The split sequences.

        """
        diag_size = (dim // 2) * 2
        iterations = (dim - 1) // 2
        return data[:diag_size], data[diag_size: dim ** 2 // 2], data[-2 * iterations: -iterations], data[-iterations:]

    @staticmethod
    def _diagonal_cat_matrix(p: int, q: int) -> numpy.ndarray:
        """
        Generates a diagonal cat matrix with given parameters.

        Args:
            p (int): The first secondary diagonal element.
            q (int): The second secondary diagonal element.

        Returns:
            numpy.ndarray: The generated diagonal cat matrix.

        """
        if p * q == 0:
            return numpy.array([[1, 1], [1, 2]], dtype=numpy.int64)
        else:
            return numpy.array([[p * q + 1, p], [q, 1]], dtype=numpy.int64)

def take(data_iter: Iterator, count: int) -> numpy.ndarray:
    """
    Takes a specified number of elements from an iterator and returns them as a numpy array.

    Args:
        data_iter (Iterator): The input iterator.
        count (int): The number of elements to take.

    Returns:
        numpy.ndarray: The taken elements as a numpy array.

    """
    return numpy.fromiter(islice(data_iter, count), dtype=numpy.int64)
