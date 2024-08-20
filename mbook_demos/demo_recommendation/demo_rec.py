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
import os

def run_purchase_rec():
    print("Running recommendation script...")
    
    # Your existing recommendation code
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, './data/purchase_history.csv')

    purchase_history = pd.read_csv(file_path)
    print(f"Row count: {len(purchase_history)}")

    product_names = purchase_history[['product_id', 'product_name']].drop_duplicates().set_index('product_id')
    purchase_counts = purchase_history.groupby(['user_id', 'product_id']).size().unstack(fill_value=0)
    sparse_purchase_counts = sparse.csr_matrix(purchase_counts)
    cosine_similarities = cosine_similarity(sparse_purchase_counts.T)
    user_id_to_index = {user_id: index for index, user_id in enumerate(purchase_counts.index)}

    def recommend_items(user_id, n=5):
        if user_id not in user_id_to_index:
            return f"User ID {user_id} not found."

        user_index = user_id_to_index[user_id]
        user_history = sparse_purchase_counts.getrow(user_index).toarray().flatten()
        similarities = cosine_similarities.dot(user_history)
        purchased_indices = np.where(user_history > 0)[0]
        similarities[purchased_indices] = 0
        recommended_indices = np.argsort(similarities)[::-1][:n]
        recommended_items = list(purchase_counts.columns[recommended_indices])
        purchased_items = list(purchase_counts.columns[purchase_counts.loc[user_id] > 0])
        recommended_items = [item for item in recommended_items if item not in purchased_items]
        recommended_names = product_names.loc[recommended_items]['product_name'].tolist()
        return recommended_names

    print('452553:', recommend_items(452553))
    print('12449:', recommend_items(12449))
    print('13042:', recommend_items(13042))
 
# run_purchase_rec()