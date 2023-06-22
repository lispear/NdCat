from typing import Sequence
import numpy

from .generator import CatGenerator


class CatMatrix:
    """
    Represents a cat matrix.

    A cat matrix is a square matrix that satisfies the following conditions:
    - All elements are integers
    - The determinant of the matrix is equal to 1
    """

    def __init__(self, matrix: Sequence[Sequence[int]]) -> None:
        """
        Initializes a CatMatrix object.

        Args:
            matrix (Sequence[Sequence[int]]): The input matrix.

        Raises:
            ValueError: If the input matrix is not a cat matrix.
        """
        self.matrix = matrix
        self._dim = self._matrix.shape[0]

    def __eq__(self, other: object) -> bool:
        """
        Checks if two CatMatrix objects are equal.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if isinstance(other, CatMatrix):
            return numpy.array_equal(self._matrix, other.matrix)
        return False

    def __hash__(self) -> int:
        """
        Calculates the hash value of the CatMatrix object.

        Returns:
            int: The hash value.
        """
        return hash(numpy.array_str(self._matrix))

    def __str__(self) -> str:
        """
        Return a string representation of the Cat Matrix.

        Returns:
            str: The string representation.
        """
        return numpy.array_str(self._matrix)

    @property
    def matrix(self) -> numpy.ndarray:
        """
        Getter for the matrix property.

        Returns:
            numpy.ndarray: The matrix.
        """
        return self._matrix

    @matrix.setter
    def matrix(self, matrix: Sequence[Sequence[int]]) -> None:
        """
        Setter for the matrix property.

        Args:
            matrix (Sequence[Sequence[int]]): The new matrix.

        Raises:
            ValueError: If the new matrix is not a cat matrix.
        """
        if self.is_cat(matrix):
            self._matrix = numpy.asarray(matrix)
        else:
            raise ValueError("Input matrix is not a cat matrix")

    @property
    def dim(self) -> int:
        """
        Getter for the dim property.

        Returns:
            int: The dimension of the matrix.
        """
        return self._dim

    @staticmethod
    def is_cat(arr: Sequence) -> bool:
        """
        Checks if a given array represents a cat matrix.

        Args:
            arr (Sequence): The input array.

        Returns:
            bool: True if the array represents a cat matrix, False otherwise.
        """
        np_arr = numpy.asarray(arr)
        if len(np_arr.shape) < 2 or np_arr.shape[0] != np_arr.shape[1]:
            return False
        if not numpy.allclose(np_arr, np_arr.astype(numpy.int64)):
            return False
        if not numpy.isclose(numpy.linalg.det(np_arr), 1):
            return False
        return True

    @classmethod
    def random(cls, dim: int, algorithm: str = 'block', low: int = 0, high: int = 256) -> 'CatMatrix':
        """
        Generates a random cat matrix using the specified algorithm.

        Args:
            dim (int): The dimension of the matrix.
            algorithm (str, optional): The algorithm to use for generating the matrix. Defaults to 'block'.
            low (int, optional): The lower bound for random element values. Defaults to 0.
            high (int, optional): The upper bound for random element values. Defaults to 256.

        Returns:
            CatMatrix: A randomly generated cat matrix.

        Raises:
            ValueError: If the specified algorithm is not supported.
        """
        return cls(CatGenerator.random(dim, algorithm, low, high))

    @classmethod
    def create(cls, dim: int, algorithm: str,  *args) -> 'CatMatrix':
        """
        Creates a new CatMatrix object using the specified algorithm.

        Args:
            algorithm (str): The algorithm to generate the cat matrix.
            dim (int): The dimension of the matrix.
            *args: Additional arguments for the specified algorithm.

        Returns:
            CatMatrix: The newly created CatMatrix object.
        """
        return cls(CatGenerator.create(algorithm, dim, *args))

    def extend(self, algorithm: str, *args) -> None:
        """
        Extends the matrix using the specified algorithm.

        Args:
            algorithm (str): The algorithm to extend the cat matrix.
            *args: Additional arguments for the specified algorithm.
        """
        self._matrix = CatGenerator.extend(algorithm, self._matrix, *args)