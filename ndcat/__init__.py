"""
NdCat
===

Provides
--------
  1. Arnold's cat map object of arbitrary dimension
  2. Calculate period of cat map
  3. Maps the input data using the cat map.

Available subpackages
---------------------
extension
  Cat matrix extension algorithm

Extension Algorithm Reference
-----------------------------
- Based on Block Matrix Combination: 

Zhongyun Hua et al. “Designing Hyperchaotic Cat Maps With Any Desired Number of Positive Lyapunov Exponents”. In: IEEE Transactions on Cybernetics 48.2 (Feb. 2018). Conference Name: IEEE Transactions on Cybernetics, pp. 463–473. ISSN: 2168-2275. URL: https://ieeexplore.ieee.org/document/7805290
    
- Based on Laplace Expansions:

Y. Wu, Z. Hua, and Y. Zhou. “n-Dimensional Discrete Cat Map Generation Using Laplace Expansions”. In: IEEE Transactions on Cybernetics (2015), pp. 1–12. URL: https://ieeexplore.ieee.org/document/7302020
"""

__version__ = 0.1

from .matrix import CatMatrix
from .map import CatMap, cube_coord
from .generator import CatGenerator
from .extension import BlockExtension, LaplaceExtension

__all__ = [
    'CatMatrix', 'CatMap', 'CatGenerator', 'BlockExtension', 'LaplaceExtension', 'cube_coord'
]