"""
This package provides a `BitMask` class for efficient manipulation and representation of binary data as a fixed-length
sequence of bits for bit manipulation, flag management, or compact binary representations of data.

It allows initializing a bitmask with a specified length and an optional starting value, provides methods for common
bitwise operations such as setting, resetting, and flipping individual or all bits and includes other useful
functionalities for various properties of the bitmask.
"""

from .bitmask_module import BitMask

__version__ = "1.2.0"
__author__ = "Adam Thieringer"
__all__ = ["BitMask"]
