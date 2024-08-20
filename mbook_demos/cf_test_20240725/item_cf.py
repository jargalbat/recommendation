# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Mon Jun 10 19:19:32 2024
#
# Author: jargalbat
# Notes:
# """
#
# import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from scipy import sparse
# import time
# from db_operations import fetch_purchase_history, fetch_books, clear_recommended_books, insert_recommendations_batch
# from file_operations import fetch_purchase_history_from_file, fetch_books_from_file, export_recommendations_to_file
#
# # Top N recommendation
# top_n = 5
#
# # Suggested 6-10
# threshold = 0.1  # Lowered threshold for testing
#
# # File paths
# purchaseHistoryFilePath = 'data/purchase_history_5.csv'
# booksFilePath = 'data/books.csv'
# recommendationsFilePath = 'data/recommendations.csv'
#
# # For testing purpose only
# file_data_source = True
# print_user_ids = [
#     452553,  # Khaitan fan, 2 books
#     12449,  # Horror books fan
#     13042,  # Jagaa
#     2527,  # Tuvshin
#     286212,  # Horror books fan
#     104207,  # History fan
#     272842,
#     288152,
#     8034,
# ]
#
#
# def run_rec():
#     total_start_time = time.time()
#     print(
#         f"Total recommendation process started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(total_start_time))}")
#
#     # Fetch purchase history as DataFrame
#     if file_data_source:
#         purchase_history = fetch_purchase_history_from_file(purchaseHistoryFilePath)
#     else:
#         purchase_history = fetch_purchase_history()
#
#     # Create the item-user matrix
#     purchase_counts = purchase_history.groupby(['book_id', 'user_id']).size().unstack(fill_value=0)
#     sparse_purchase_counts = sparse.csr_matrix(purchase_counts)
#     cosine_similarities = cosine_similarity(sparse_purchase_counts)
#     book_id_to_index = {book_id: index for index, book_id in enumerate(purchase_counts.index)}
#     user_id_to_index = {user_id: index for index, user_id in enumerate(purchase_counts.columns)}
#
#     def recommend_items(user_id, n=top_n):
#         if user_id not in user_id_to_index:
#             return f"User ID {user_id} not found."
#
#         user_index = user_id_to_index[user_id]
#         user_history = sparse_purchase_counts[:, user_index].toarray().flatten()
#         recommended_books = set()
#
#         for book_index, count in enumerate(user_history):
#             if count > 0:
#                 similar_books = cosine_similarities[book_index]
#                 similar_indices = np.argsort(similar_books)[::-1]
#                 for index in similar_indices:
#                     if similar_books[index] > threshold and sparse_purchase_counts[index, user_index] == 0:
#                         recommended_books.add(purchase_counts.index[index])
#                         if len(recommended_books) >= n:
#                             break
#             if len(recommended_books) >= n:
#                 break
#
#         return list(recommended_books)
#
#     # Fetch book details
#     if file_data_source:
#         book_details = fetch_books_from_file(booksFilePath)
#     else:
#         book_details = fetch_books()
#
#     # Run recommendations for all users
#     all_user_ids = purchase_counts.columns
#     recommended_user_count = 0
#
#     start_time = time.time()
#     print(f"Recommendation calculation started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
#     recommendations_to_insert = []
#
#     for user_id in all_user_ids:
#         recommendations = recommend_items(user_id)
#         recommended_user_count += 1
#
#         # Accumulate recommendations for batch insert
#         recommendations_to_insert.extend([(user_id, book_id) for book_id in recommendations])
#
#         if user_id in print_user_ids:
#             recommended_books = book_details[book_details['book_id'].isin(recommendations)]
#             print(f"Book titles for recommendations for user {user_id}:")
#             print(recommended_books[['book_id', 'book_title']].to_string(index=False))
#
#             # Print book titles for recommendations
#             recommended_titles = recommended_books['book_title'].tolist()
#             print(f"Recommended books for user {user_id}: {', '.join(recommended_titles)}")
#
#     recommendation_end_time = time.time()
#
#     print(
#         f"Recommendation calculation ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(recommendation_end_time))}")
#     print(f"Total recommendation calculation time: {recommendation_end_time - start_time:.2f} seconds")
#     print(f"Total number of users recommended: {recommended_user_count}")
#
#     # Clear the recommended_books table if not using file
#     if not file_data_source:
#         clear_recommended_books()
#
#     # Insert or export all recommendations in batch
#     if file_data_source:
#         export_recommendations_to_file(recommendations_to_insert, recommendationsFilePath)
#     else:
#         insert_recommendations_batch(recommendations_to_insert)
#
#     total_end_time = time.time()
#     print(
#         f"Total recommendation process ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(total_end_time))}")
#     print(f"Total recommendation process time: {total_end_time - total_start_time:.2f} seconds")
#
#
# if __name__ == "__main__":
#     run_rec()
