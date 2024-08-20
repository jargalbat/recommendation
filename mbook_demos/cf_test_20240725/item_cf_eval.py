# #!/opt/anaconda3/envs/RecSys/bin/python
# # -*- coding: utf-8 -*-
# """
# Created on Thu Jul 25 10:32:20 2024
#
# Author: jargalbat
# Notes: Evaluation and export script for item-based recommendations
# """
#
# import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from scipy import sparse
# import time
# from db_operations import fetch_purchase_history, fetch_books, clear_recommended_books, insert_recommendations_batch
# from file_operations import fetch_purchase_history_from_file, fetch_books_from_file, export_recommendations_to_file
# from sklearn.model_selection import train_test_split
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
#
# print_user_ids = [12449, 13042, 2527, 286212, 104207, 272842, 288152]
#
# def fetch_data():
#     # Fetch purchase history as DataFrame
#     if file_data_source:
#         purchase_history = fetch_purchase_history_from_file(purchaseHistoryFilePath)
#     else:
#         purchase_history = fetch_purchase_history()
#
#     # Fetch book details
#     if file_data_source:
#         book_details = fetch_books_from_file(booksFilePath)
#     else:
#         book_details = fetch_books()
#
#     return purchase_history, book_details
#
# def create_item_user_matrix(purchase_history):
#     purchase_counts = purchase_history.groupby(['book_id', 'user_id']).size().unstack(fill_value=0)
#     sparse_purchase_counts = sparse.csr_matrix(purchase_counts)
#     cosine_similarities = cosine_similarity(sparse_purchase_counts)
#     book_id_to_index = {book_id: index for index, book_id in enumerate(purchase_counts.index)}
#     user_id_to_index = {user_id: index for index, user_id in enumerate(purchase_counts.columns)}
#     return purchase_counts, sparse_purchase_counts, cosine_similarities, book_id_to_index, user_id_to_index
#
# def recommend_items(user_id, user_id_to_index, sparse_purchase_counts, cosine_similarities, purchase_counts, n=top_n):
#     if user_id not in user_id_to_index:
#         return []
#
#     user_index = user_id_to_index[user_id]
#     user_history = sparse_purchase_counts.getcol(user_index).toarray().flatten()
#     recommended_books = set()
#
#     for book_index, count in enumerate(user_history):
#         if count > 0:
#             similar_books = cosine_similarities[book_index]
#             similar_indices = np.argsort(similar_books)[::-1]
#             for index in similar_indices:
#                 if similar_books[index] > threshold and sparse_purchase_counts[index, user_index] == 0:
#                     recommended_books.add(purchase_counts.index[index])
#                     if len(recommended_books) >= n:
#                         break
#         if len(recommended_books) >= n:
#             break
#
#     return list(recommended_books)
#
# def run_recommendations():
#     total_start_time = time.time()
#     print(f"Total recommendation process started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(total_start_time))}")
#
#     purchase_history, book_details = fetch_data()
#     train_data, test_data = train_test_split(purchase_history, test_size=0.2, random_state=42)
#     purchase_counts, sparse_purchase_counts, cosine_similarities, book_id_to_index, user_id_to_index = create_item_user_matrix(train_data)
#
#     all_user_ids = train_data['user_id'].unique()
#     recommended_user_count = 0
#
#     start_time = time.time()
#     print(f"Recommendation calculation started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
#     recommendations_to_insert = []
#
#     for user_id in all_user_ids:
#         recommendations = recommend_items(user_id, user_id_to_index, sparse_purchase_counts, cosine_similarities, purchase_counts)
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
#     recommendation_end_time = time.time()
#
#     print(f"Recommendation calculation ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(recommendation_end_time))}")
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
#     print(f"Total recommendation process ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(total_end_time))}")
#     print(f"Total recommendation process time: {total_end_time - total_start_time:.2f} seconds")
#
#     # Evaluate the recommendations
#     avg_precision, avg_recall, avg_f1_score = evaluate_recommendations(test_data, recommend_items, user_id_to_index, sparse_purchase_counts, cosine_similarities, purchase_counts)
#     print(f'Average Precision@{top_n}: {avg_precision:.4f}')
#     print(f'Average Recall@{top_n}: {avg_recall:.4f}')
#     print(f'Average F1 Score@{top_n}: {avg_f1_score:.4f}')
#
# def evaluate_recommendations(test_data, recommend_items_fn, user_id_to_index, sparse_purchase_counts, cosine_similarities, purchase_counts, num_recommendations=top_n):
#     # Build the test user-item interaction matrix
#     test_user_book_matrix = test_data.groupby(['user_id', 'book_id']).size().unstack(fill_value=0)
#
#     precision_at_k = []
#     recall_at_k = []
#     f1_scores = []
#
#     for user_id in test_user_book_matrix.index:
#         # Get the actual books purchased by the user in the test set
#         actual_books = set(test_user_book_matrix.columns[test_user_book_matrix.loc[user_id] > 0])
#
#         # Get the recommended books for the user
#         recommended_books = recommend_items_fn(user_id, user_id_to_index, sparse_purchase_counts, cosine_similarities, purchase_counts, num_recommendations)
#         recommended_books_set = set(recommended_books)
#
#         # Compute Precision@K
#         relevant_and_recommended = actual_books & recommended_books_set
#         precision = len(relevant_and_recommended) / len(recommended_books_set) if recommended_books_set else 0
#         precision_at_k.append(precision)
#
#         # Compute Recall@K
#         recall = len(relevant_and_recommended) / len(actual_books) if actual_books else 0
#         recall_at_k.append(recall)
#
#         # Compute F1 Score
#         if precision + recall > 0:
#             f1_score = 2 * (precision * recall) / (precision + recall)
#         else:
#             f1_score = 0
#         f1_scores.append(f1_score)
#
#     # Calculate average Precision@K, Recall@K, and F1 Score
#     avg_precision_at_k = np.mean(precision_at_k)
#     avg_recall_at_k = np.mean(recall_at_k)
#     avg_f1_score = np.mean(f1_scores)
#
#     return avg_precision_at_k, avg_recall_at_k, avg_f1_score
#
# if __name__ == "__main__":
#     run_recommendations()
