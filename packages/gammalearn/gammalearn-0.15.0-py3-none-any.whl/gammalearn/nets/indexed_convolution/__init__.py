"""The indexed convolution module implements convolution on non-grid lattices

This module can be used to perform convolution operations on hexagonal images, such as the LST images,
without interpolating them to a square grid.

The indexed convolutions are much slower than pytorch convolution due to non-optimized memory access in the
1D image representation, and have been found to not increase the models performances compared to regular
convolution on interpolated images.
Therefore, the indexed convolution module is deprecated and will be removed in a future version
"""
