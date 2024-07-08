#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:19:32 2024

@author: jargalbat
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

# Load the purchase history data from a CSV file into a DataFrame
file_path = 'data2.csv'  # Assuming the file is in the current directory
purchase_history = pd.read_csv(file_path)

# Print the row count of the CSV file
print(f"Row count: {len(purchase_history)}")

# Create a DataFrame with product names, authors, and topics indexed by product_id
product_info = purchase_history[['product_id', 'product_name', 'author_name', 'topic_name']].drop_duplicates().set_index('product_id')

# Fill NaN values in author_name and topic_name with empty strings
product_info['author_name'] = product_info['author_name'].fillna('')
product_info['topic_name'] = product_info['topic_name'].fillna('')

# Combine product name, author, and topic into a single string for each product
product_info['combined_features'] = product_info['product_name'] + ' ' + product_info['author_name'] + ' ' + product_info['topic_name']

# Ensure the product_info index matches the purchase_counts columns
common_product_ids = purchase_history['product_id'].unique()
product_info = product_info.loc[common_product_ids]

# Count the number of purchases for each user and product combination
purchase_counts = purchase_history.groupby(['user_id', 'product_id']).size().unstack(fill_value=0)

# Ensure purchase_counts has all products in product_info
purchase_counts = purchase_counts.reindex(columns=product_info.index, fill_value=0)

# Create a combined feature matrix for products
combined_features_matrix = sparse.csr_matrix(pd.get_dummies(product_info['combined_features']))

# Compute the cosine similarity matrix between the products based on combined features
cosine_similarities = cosine_similarity(combined_features_matrix)

# Create a mapping from user_id to matrix row index
user_id_to_index = {user_id: index for index, user_id in enumerate(purchase_counts.index)}

# Convert purchase_counts to a sparse matrix
sparse_purchase_counts = sparse.csr_matrix(purchase_counts)

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
    recommended_names = product_info.loc[recommended_items]['product_name'].tolist()

    # Remove duplicates
    recommended_names = list(set(recommended_names))

    return recommended_names

# ['Вавилоны хамгийн баян хүн', 'Сиддхарта', 'XXI зууны ёс суртахуун', 
# 'Боодол мөнгө', 'Аяга кофены бясалгалаар тэрбумтан болсон хүмүүс']
print('452553:', recommend_items(452553)) 

# ['Үхлийн хот', 'Улаан шиш', 'Будант цадиг']
print('12449:',recommend_items(12449))

# ['Сүүдэргүй хүмүүс', 'Сайн уу, Айдас минь', 'Бидний мэдэхгүй амьдрал', 'Эгэл амьдрах ухаан', 'Харизм']
print('13042:', recommend_items(13042))



