#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:19:32 2024

@author: jargalbat
"""

# https://docs.google.com/document/d/1pve8RTMNRk8dy4_4PbzO2Jq9v4NCk4cfOyEdq5odXlo/edit?usp=sharing

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

# Sample purchase history data
data = {
    'user_id': ['u1', 'u1', 'u2', 'u2', 'u3', 'u3', 'u3', 'u4', 'u4'],
    'product_id': ['pA', 'pB', 'pA', 'pC', 'pB', 'pC', 'pD', 'pA', 'pD']
}
purchase_history = pd.DataFrame(data)
# print('purchase_history', purchase_history)

# Create a user-product purchase matrix
purchase_counts = purchase_history.groupby(['user_id', 'product_id']).size().unstack(fill_value=0)
# print('purchase_counts', purchase_counts)

# Convert the purchase matrix to a sparse matrix
# Сийрэг матриц нь зөвхөн тэгээс ялгаатай элемент болон түүний байршлыг хадгалдаг. 
sparse_purchase_counts = sparse.csr_matrix(purchase_counts)
# print('sparse_purchase_counts', sparse_purchase_counts)
# print("Data:", sparse_purchase_counts.data)
# print("Indices:", sparse_purchase_counts.indices)
# print("Indptr:", sparse_purchase_counts.indptr)

# Compute the cosine similarity matrix between users
user_similarities = cosine_similarity(sparse_purchase_counts)
# print('user_similarities', user_similarities)

# Create a mapping from user_id to matrix row index
# (user_id: index) -> for (index,user_id) in (user_id-г жагсаалт хэлбэрээр авна)
user_id_to_index = {user_id: index for index, user_id in enumerate(purchase_counts.index)}
print('user_id_to_index', user_id_to_index)

# Define a function to recommend items for a user based on their purchase history
def recommend_items(user_id, n=2):
    if user_id not in user_id_to_index:
        return f"User ID {user_id} not found."

    user_index = user_id_to_index[user_id]

    # Get the user's similarity scores with other users
    user_similarity_scores = user_similarities[user_index]
    # print('user_similarity_scores', user_similarity_scores)

    # Get the purchase history of similar users
    # Энэ нь тухайн хэрэглэгчтэй ижил төстэй хэрэглэгчдийн худалдан авсан 
    # бүтээгдэхүүнүүдийн жигнэсэн нийлбэрийг өгнө. Жигнэсэн гэдэг нь өмнөх алхамд
    # гаргасан хамаарлын коэфицентээр үржүүлсэнийг хэлнэ.
    # Бүтээгдэхүүний жагсаалтыг худалдан авсан нийт хэрэглэгчдийн векторыг, 
    # тухайлсан нэг хэрэглэгчийн бусад хэрэглэгчдээс хэрхэн хамааралтай байгааг 
    # илэрхийлсэн косинус өнцгийн хамаарлын коэфициентээр үржүүлж, жигнэсэн 
    # нийлбэрийг гаргана.
    similar_users_purchases = sparse_purchase_counts.T.dot(user_similarity_scores).flatten()
    # print('sparse_purchase_counts', sparse_purchase_counts)
    # print('sparse_purchase_counts.T', sparse_purchase_counts.T)
    # print('user_similarity_scores', user_similarity_scores)
    # print('sparse_purchase_counts.T.dot(user_similarity_scores)', sparse_purchase_counts.T.dot(user_similarity_scores))
    # print('similar_users_purchases [pA pB pC pD]', similar_users_purchases)

    # Get the indices of the user's purchased items
    user_purchases = sparse_purchase_counts.getrow(user_index).toarray().flatten()
    purchased_indices = np.where(user_purchases > 0)[0]
    # print('user_purchases', user_purchases)
    # print('np.where(user_purchases > 0)', np.where(user_purchases > 0))
    # print('np.where(user_purchases > 0)[0]', np.where(user_purchases > 0)[0])
    # print('purchased_indices', purchased_indices)

    # Set the scores for purchased items to 0
    similar_users_purchases[purchased_indices] = 0
    # print('similar_users_purchases after', similar_users_purchases)

    # Sort the items by score and return the top n items
    # Өсөхөөр эрэмбэлснийг урвуугаар эрэмбэлж, эхний n элементийг авна
    recommended_indices = np.argsort(similar_users_purchases)[::-1][:n]
    # print('recommended_indices', recommended_indices)
    # Матрицаас баганы нэрс буюу бүтээгдэхүүний нэрсийг индексээр нь авна
    recommended_items = list(purchase_counts.columns[recommended_indices])
    # print('purchase_counts',purchase_counts)
    # print('purchase_counts.columns[recommended_indices]', purchase_counts.columns[recommended_indices])
    # print('recommended_items', recommended_items)

    return recommended_items

# Example usage:
print(f"Recommendations for user 1: {recommend_items('u1')}")
# print(f"Recommendations for user 2: {recommend_items('u2')}")
# print(f"Recommendations for user 3: {recommend_items('u3')}")
# print(f"Recommendations for user 4: {recommend_items('u4')}")
