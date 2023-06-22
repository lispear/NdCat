from functools import cache
from typing import Sequence, Optional
import numpy

from .matrix import CatMatrix


class CatMap(CatMatrix):
    """
    Represents a cat map, which is a type of cat matrix with mod size.

    Inherits from the CatMatrix class.

    Usage:
        catmap = CatMap([[1, 1], [1, 2]])

        catmap.period(5)
        
        catmap.mapping([2, 3])

        catmap = CatMap.random(3)
    
    Example:
        >>> catmap = CatMap([[1, 1], [1, 2]])
        >>> print(catmap)
        [[1 1]
         [1 2]]
        >>> catmap.period(5)
        10
        >>> catmap.mapping([2, 3], 5)
        array([[0],
               [3]], dtype=int32))
        >>> catmap = CatMap.random(3)
        >>> print(catmap)
        [[   1    0    0]
        [ 208 3025   84]
        [   9   36    1]]
    """

    def __init__(self, matrix: Sequence[Sequence[int]]) -> None:
        """
        Initializes a CatMap object.

        Args:
            matrix (Sequence[Sequence[int]]): The input matrix.

        """
        super().__init__(matrix)

    @cache
    def period(self, size: int) -> int:
        """
        Calculates the period of the cat map for a given size.

        Args:
            size (int): The size for which to calculate the period.

        Returns:
            int: The period of the cat map.

        """
        coord = cube_coord(self._dim, size)
        coord_p = self.mapping(coord, size)
        period = 1
        while not numpy.array_equal(coord, coord_p):
            self.mapping(coord_p, size, out=coord_p)
            period += 1
        return period

    def mapping(self, data: Sequence, size: int, out: Optional[numpy.ndarray] = None) -> Optional[numpy.ndarray]:
        """
        Maps the input data using the cat map matrix.

        Args:
            data (Sequence): The input data to be mapped.
            size (int): The size of the mapping space.
            out (Optional[numpy.ndarray], optional): The output array to store the mapped data. If not provided, a new array will be returned. Defaults to None.

        Returns:
            Optional[numpy.ndarray]: The mapped data, if out is not provided.

        """
        res = numpy.matmul(self._matrix, numpy.asarray(data).reshape(self._dim, -1)) % size
        if out is not None:
            out[...] = res
        else:
            return res

def cube_coord(dimension: int, size: int) -> numpy.ndarray:
    """
    Generates the cube coordinates for a given dimension and size.

    Args:
        dimension (int): The dimension of the cube.
        size (int): The size of each dimension.

    Returns:
        numpy.ndarray: The cube coordinates.

    """
    return numpy.asarray(
        numpy.meshgrid(*[numpy.arange(size) for _ in range(dimension)], indexing='ij'),
        dtype=numpy.int64
    ).reshape(dimension, -1)