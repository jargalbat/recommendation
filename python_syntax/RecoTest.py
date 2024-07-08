#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 18:57:18 2024

@author: jargalbat
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

# Load the purchase history data into a DataFrame
data = {'user_id': [1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4],
        'product_id': ['A', 'B', 'B', 'C', 'D', 'A', 'C', 'D', 'E', 'A', 'E']}
purchase_history = pd.DataFrame(data)

# Count the number of purchases for each user and product combination
purchase_counts = purchase_history.groupby(['user_id', 'product_id']).size().unstack(fill_value=0)

# Convert the purchase counts to a sparse matrix
sparse_purchase_counts = sparse.csr_matrix(purchase_counts)

# Compute the cosine similarity matrix between the products
cosine_similarities = cosine_similarity(sparse_purchase_counts.T)

# Define a function to recommend items for a user based on their purchase history
def recommend_items(user_id, n=5):
    # Get the user's purchase history
    user_history = sparse_purchase_counts[user_id].toarray().flatten()

    # Compute the average cosine similarity between the user's purchased items and all other items
    similarities = cosine_similarities.dot(user_history)

    # Get the indices of the user's purchased items
    purchased_indices = np.where(user_history > 0)[0]

    # Set the similarity scores for purchased items to 0
    similarities[purchased_indices] = 0

    # Sort the items by similarity score and return the top n items
    recommended_indices = np.argsort(similarities)[::-1][:n]
    recommended_items = list(purchase_counts.columns[recommended_indices])
    
    # Remove the items that the user has already purchased
    purchased_items = list(purchase_counts.columns[purchase_counts.loc[user_id] > 0])
    recommended_items = [item for item in recommended_items if item not in purchased_items]

    return recommended_items

# Example usage:
print(recommend_items(1))  # Output: ['D', 'C', 'E']