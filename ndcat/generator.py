from typing import Dict, Sequence, Tuple, Type, Union
import numpy

from .extension import BlockExtension, LaplaceExtension

Extension = Union[BlockExtension, LaplaceExtension]

_expansion_dict: Dict[str, Type[Extension]] = {
    'block': BlockExtension,
    'laplace': LaplaceExtension
}

class CatGenerator:
    """
    Generates cat matrix using different algorithms.

    """

    @staticmethod
    def create(dim: int, algorithm: str, *args: Sequence[int]) -> numpy.ndarray:
        """
        Creates a cat matrix using the specified algorithm.

        Args:
            algorithm (str): The algorithm to use for matrix creation.
            dim (int): The dimension of the cat matrix.
            *args (Sequence[int]): Additional arguments specific to the algorithm.

        Returns:
            np.ndarray: The created cat matrix.

        Raises:
            ValueError: If the specified algorithm is invalid.

        """
        if algorithm in _expansion_dict:
            return _expansion_dict[algorithm].create(dim, *args)
        else:
            raise ValueError(f"Invalid algorithm {algorithm}")
    
    @staticmethod
    def extend(algorithm: str, matrix: Sequence[Sequence[int]], *args: Sequence[int]) -> numpy.ndarray:
        """
        Extends a cat matrix using the specified algorithm.

        Args:
            algorithm (str): The algorithm to use for matrix extension.
            matrix (Sequence[Sequence[int]]): The input cat matrix.
            *args (Sequence[int]): Additional arguments specific to the algorithm.

        Returns:
            np.ndarray: The extended cat matrix.

        Raises:
            ValueError: If the specified algorithm is invalid.

        """
        if algorithm in _expansion_dict:
            return _expansion_dict[algorithm].extend(matrix, *args)
        else:
            raise ValueError(f"Invalid algorithm {algorithm}")
    
    @staticmethod
    def split_sequence(dim: int, algorithm: str, source: Sequence[int]) -> Tuple[Sequence[int], ...]:
        """
        Splits a sequence using the specified algorithm.

        Args:
            algorithm (str): The algorithm to use for sequence splitting.
            dim (int): The dimension of the cat matrix.
            source (Sequence[int]): The input sequence to split.

        Returns:
            Tuple[Sequence[int], ...]: The split sequences.

        Raises:
            ValueError: If the specified algorithm is invalid.

        """
        if algorithm in _expansion_dict:
            return _expansion_dict[algorithm].split_sequence(dim, source)
        else:
            raise ValueError(f"Invalid algorithm {algorithm}")

    @staticmethod
    def random(dim: int, algorithm: str, low: int, high: int) -> numpy.ndarray:
        """
        Generates a random cat matrix using the specified algorithm.

        Args:
            dim (int): The dimension of the cat matrix.
            algorithm (str): The algorithm to use for matrix generation.
            low (int): The lower bound of the random values (inclusive).
            high (int): The upper bound of the random values (exclusive).

        Returns:
            np.ndarray: The generated random cat matrix.

        Raises:
            ValueError: If the specified algorithm is invalid.

        """
        if algorithm in _expansion_dict:
            return _expansion_dict[algorithm].random(dim, low, high)
        else:
            raise ValueError(f"Invalid algorithm {algorithm}")
