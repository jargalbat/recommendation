#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:19:32 2024

@author: jargalbat

Notes: 

"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

# Load the purchase history data from a CSV file into a DataFrame
file_path = '../data/user_id_product_id_product_name.csv'
# file_path = 'user_id_product_id_product_name.csv'  # Assuming the file is in the current directory
purchase_history = pd.read_csv(file_path)

# Print the row count of the CSV file
print(f"Row count: {len(purchase_history)}")

# Create a DataFrame with product names indexed by product_id
product_names = purchase_history[['product_id', 'product_name']].drop_duplicates().set_index('product_id')

# Count the number of purchases for each user and product combination
purchase_counts = purchase_history.groupby(['user_id', 'product_id']).size().unstack(fill_value=0)

# Convert the purchase counts to a sparse matrix
sparse_purchase_counts = sparse.csr_matrix(purchase_counts)
# print('sparse_purchase_counts', sparse_purchase_counts)

# Compute the cosine similarity matrix between the products
cosine_similarities = cosine_similarity(sparse_purchase_counts.T)
# print('cosine_similarities', cosine_similarities)

# Create a mapping from user_id to matrix row index
user_id_to_index = {user_id: index for index, user_id in enumerate(purchase_counts.index)}
# print('user_id_to_index', user_id_to_index)

# Define a function to recommend items for a user based on their purchase history
def recommend_items(user_id, n=5):
    if user_id not in user_id_to_index:
        return f"User ID {user_id} not found."

    user_index = user_id_to_index[user_id]

    # Get the user's purchase history
    user_history = sparse_purchase_counts.getrow(user_index).toarray().flatten()

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

    # Get the names of the recommended items
    recommended_names = product_names.loc[recommended_items]['product_name'].tolist()
    # recommended_ids = product_names.loc[recommended_items]['product_id'].tolist()

    return recommended_names
    # return recommended_items

# 452553: ['Гуравласан аймшиг', 'Анарваан', 'Банхар', 'Хятад сүнс', 'Яс']
print('452553:', recommend_items(452553)) 

# 12449: ['Яс', 'Хэен хуар', 'Мэргэн', 'Хээрийн юм', 'Эмгэн']
print('12449:',recommend_items(12449))

# 13042: ['Би Солонгос хүн', 'Ухаалгаар төлсөн нь', 'Ж. Остен “Мэнсфилд парк” (В.Набоковын лекц)', 'Товгүй Баярын Хот', 'Нууц товчооны адуу']
print('13042:', recommend_items(13042))

