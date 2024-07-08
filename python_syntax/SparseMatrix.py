#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 15:47:55 2024

@author: jargalbat
"""

import numpy as np
from scipy import sparse

# Нягт матриц үүсгэх
dense_matrix = np.array([
    [1, 0, 0],
    [0, 0, 2],
    [0, 3, 0]
])

# Нягт матрицыг CSR форматтай сул матриц болгон хөрвүүлэх
sparse_matrix = sparse.csr_matrix(dense_matrix)

# Сул матрицыг хэвлэх
print(sparse_matrix)

# Гаралт:
# (0, 0)    1
# (1, 2)    2
# (2, 1)    3

# Мөн CSR матрицын data, indices, indptr атрибутуудыг ашиглах боломжтой
print("Data:", sparse_matrix.data)
print("Indices:", sparse_matrix.indices)
print("Indptr:", sparse_matrix.indptr)
