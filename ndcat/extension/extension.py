from abc import ABC, abstractclassmethod, abstractstaticmethod
from typing import Sequence, Tuple
import numpy as np

class Extension(ABC):

    @abstractstaticmethod
    def check_parameters(dim: int, *args: Sequence) -> bool:
        """
        Check if the parameters are valid.

        Args:
            dim (int): The dimension.
            *args (Sequence): Other parameter sequence.

        Returns:
            bool: Boolean value indicating whether the parameters are valid.
        """
        ...
    
    @abstractclassmethod
    def create(cls, dim: int, *args: Sequence) -> np.ndarray:
        """
        Create a numpy array.

        Args:
            dim (int): The dimension.
            *args (Sequence): Other parameter sequence.

        Returns:
            np.ndarray: The created numpy array.
        """
        ...

    @abstractclassmethod
    def extend(cls, matrix: np.ndarray, *args: Sequence) -> np.ndarray:
        """
        Extend the given matrix.

        Args:
            matrix (np.ndarray): The matrix to extend.
            *args (Sequence): Other parameter sequence.

        Returns:
            np.ndarray: The extended numpy array.
        """
        ...
    
    @abstractclassmethod
    def random(cls, dim: int, algorithm: str, low: int, high: int) -> np.ndarray:
        """
        Generate a random numpy array.

        Args:
            dim (int): The dimension.
            algorithm (str): The algorithm used for random number generation.
            low (int): The lower bound of the random numbers.
            high (int): The upper bound of the random numbers.

        Returns:
            np.ndarray: The generated random numpy array.
        """
        ...
    
    @abstractstaticmethod
    def split_sequence(source: Sequence) -> Tuple[Sequence, ...]:
        """
        Split the source sequence into multiple sequences.

        Args:
            source (Sequence): The source sequence to split.

        Returns:
            Tuple[Sequence, ...]: A tuple of split sequences.
        """
        ...
