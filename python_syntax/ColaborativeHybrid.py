#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:58:43 2024

@author: jargalbat
"""

# 1. Create the User-Item Interaction Matrix:
import pandas as pd
import numpy as np

# Example data
data = pd.DataFrame({
    'user_id': [1, 1, 2, 2, 3, 3, 4],
    'book_id': ['A', 'B', 'A', 'C', 'B', 'C', 'D'],
    'interaction': [1, 1, 1, 1, 1, 1, 1]  # Interaction could be a purchase
})

# Create user-item matrix
user_item_matrix = pd.pivot_table(data, index='user_id', columns='book_id', values='interaction', fill_value=0)
print('user_item_matrix', user_item_matrix)

# 2. Compute Collaborative Filtering Similarity:
from sklearn.metrics.pairwise import cosine_similarity

# Compute item-item similarity using collaborative filtering
item_similarity_cf = cosine_similarity(user_item_matrix.T)
item_similarity_cf_df = pd.DataFrame(item_similarity_cf, index=user_item_matrix.columns, columns=user_item_matrix.columns)
print('item_similarity_cf', item_similarity_cf)
print('item_similarity_cf_df', item_similarity_cf_df)


# Book attribute - Best seller
 