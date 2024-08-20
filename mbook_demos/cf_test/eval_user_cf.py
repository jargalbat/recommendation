# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Mon Jun 10 19:19:32 2024
#
# Author: jargalbat
# Notes:
# """
#
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from scipy import sparse
# import time
# from db_operations import fetch_purchase_history, fetch_books, clear_recommended_books, insert_recommendations_batch
# from file_operations import fetch_purchase_history_from_file, fetch_books_from_file, export_recommendations_to_file
# from sklearn.model_selection import train_test_split
#
# # For testing purpose only
# is_test = True
#
# # Top N recommendation
# top_n = 20
#
# # File paths
# purchaseHistoryFilePath = '../data/purchase_history.csv'
# booksFilePath = '../data/books.csv'
# recommendationsFilePath = '../data/recommendations.csv'
#
# print_user_ids = [
#     452553,  # Khaitan fan, 2 books
#     12449,  # Horror books fan
#     13042,  # Jagaa
#     2527,  # Tuvshin
#     286212,  # Horror books fan
#     104207,  # History fan
#     272842,  # AM - Kids
#     288152,  # AM - 4
#     8034,  # Byambaa
#     301596,  # AB
# ]
#
#
# def generate_recommendations(evaluate=False):
#     total_start_time = time.time()
#     print(
#         f"Total recommendation process started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(total_start_time))}")
#
#     # Fetch purchase history as DataFrame
#     if is_test:
#         purchase_history = fetch_purchase_history_from_file(purchaseHistoryFilePath)
#     else:
#         purchase_history = fetch_purchase_history()
#
#     # Split the data into training and test sets
#     if evaluate:
#         test_size = 0.2
#     else:
#         test_size = 0.0
#     train_data, test_data = train_test_split(purchase_history, test_size=test_size, random_state=42)
#
#     # Create the user-item matrix for training data
#     purchase_counts = train_data.groupby(['user_id', 'book_id']).size().unstack(fill_value=0)
#     sparse_purchase_counts = sparse.csr_matrix(purchase_counts)
#     cosine_similarities = cosine_similarity(sparse_purchase_counts.T)
#     user_id_to_index = {user_id: index for index, user_id in enumerate(purchase_counts.index)}
#
#     # Calculate item popularity
#     item_popularity = purchase_counts.sum(axis=0).to_dict()
#
#     def recommend_items(user_id, n=top_n):
#         if user_id not in user_id_to_index:
#             return []
#
#         user_index = user_id_to_index[user_id]
#         user_history = sparse_purchase_counts.getrow(user_index).toarray().flatten()
#         similarities = cosine_similarities.dot(user_history)
#         purchased_indices = np.where(user_history > 0)[0]
#         similarities[purchased_indices] = 0
#
#         # Multiply candidate
#         candidate_multiplier = 1
#         recommended_indices = np.argsort(similarities)[::-1][:n * candidate_multiplier]
#
#         recommended_items = list(purchase_counts.columns[recommended_indices])
#         purchased_items = list(purchase_counts.columns[purchase_counts.loc[user_id] > 0])
#         recommended_items = [item for item in recommended_items if item not in purchased_items]
#
#         # Re-rank based on popularity
#         recommended_items = sorted(recommended_items, key=lambda x: item_popularity.get(x, 0), reverse=True)[:n]
#         return recommended_items
#
#     # Fetch book details
#     if is_test:
#         book_details = fetch_books_from_file(booksFilePath)
#     else:
#         book_details = fetch_books()
#
#     # Run recommendations for all users
#     all_user_ids = purchase_history['user_id'].unique()
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
#     recommendation_end_time = time.time()
#
#     print(
#         f"Recommendation calculation ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(recommendation_end_time))}")
#     print(f"Total recommendation calculation time: {recommendation_end_time - start_time:.2f} seconds")
#     print(f"Total number of users recommended: {recommended_user_count}")
#
#     # Clear the recommended_books table if not using file
#     if not is_test:
#         clear_recommended_books()
#
#     # Insert or export all recommendations in batch
#     if is_test:
#         export_recommendations_to_file(recommendations_to_insert, recommendationsFilePath)
#     else:
#         insert_recommendations_batch(recommendations_to_insert)
#
#     total_end_time = time.time()
#     print(
#         f"Total recommendation process ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(total_end_time))}")
#     print(f"Total recommendation process time: {total_end_time - total_start_time:.2f} seconds")
#
#     # Evaluate the recommendations
#     if evaluate:
#         evaluate_recommendations(test_data, recommend_items)
#
#
# def evaluate_recommendations(test_data, recommend_items_fn, num_recommendations=top_n):
#     # Build the test user-item interaction matrix
#     test_user_book_matrix = test_data.groupby(['user_id', 'book_id']).size().unstack(fill_value=0)
#
#     precision_at_k = []
#     recall_at_k = []
#     f1_scores = []
#     all_recommended_items = []
#     all_actual_items = []
#     r_precision_errors = []
#     unique_books = set(test_data['book_id'].unique())
#     total_books = len(unique_books)
#
#     for user_id in test_user_book_matrix.index:
#         # Get the actual books purchased by the user in the test set
#         actual_books = set(test_user_book_matrix.columns[test_user_book_matrix.loc[user_id] > 0])
#         all_actual_items.extend(actual_books)
#
#         # Get the recommended books for the user
#         recommended_books = recommend_items_fn(user_id, num_recommendations)
#         recommended_books_set = set(recommended_books)
#         all_recommended_items.extend(recommended_books_set)
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
#         # Compute R-Precision Mean Error (RME)
#         r_precision_error = abs(len(relevant_and_recommended) - len(actual_books))
#         r_precision_errors.append(r_precision_error)
#
#     # Calculate diversity as the percentage of unique recommended items
#     diversity = len(set(all_recommended_items)) / len(all_recommended_items) if all_recommended_items else 0
#
#     # Calculate hit rate as the percentage of users with at least one relevant recommendation
#     hit_rate = sum(1 for user_id in test_user_book_matrix.index if
#                    len(set(recommend_items_fn(user_id, num_recommendations)) & set(
#                        test_user_book_matrix.columns[test_user_book_matrix.loc[user_id] > 0])) > 0) / len(
#         test_user_book_matrix.index)
#
#     # Calculate novelty as the average inverse popularity of recommended items
#     item_popularity = test_data['book_id'].value_counts().to_dict()
#     novelty = np.mean([1 / item_popularity.get(book, 1) for book in all_recommended_items])
#
#     # Calculate average Precision@K, Recall@K, F1 Score, and RME
#     avg_precision_at_k = np.mean(precision_at_k)
#     avg_recall_at_k = np.mean(recall_at_k)
#     avg_f1_score = np.mean(f1_scores)
#     rme = np.mean(r_precision_errors)
#
#     print(f'Average Precision@{top_n}: {avg_precision_at_k:.4f} (Goal: 0.10 to 0.30)')
#     print(f'Average Recall@{top_n}: {avg_recall_at_k:.4f} (Goal: 0.20 to 0.50)')
#     print(f'Average F1 Score@{top_n}: {avg_f1_score:.4f} (Goal: 0.15 to 0.35)')
#     print(f'Diversity: {diversity:.4f} (Goal: At least 10-20% diverse recommendations)')
#     print(f'Hit Rate: {hit_rate:.4f} (Goal: At least 0.5)')
#     print(f'Novelty: {novelty:.4f} (Goal: 0.01 to 0.05)')
#     print(f'R-Precision Mean Error (RME): {rme:.4f} (Goal: Closer to 1.0 or below)')
#
#     return avg_precision_at_k, avg_recall_at_k, avg_f1_score, diversity, hit_rate, novelty, rme
#
#
# if __name__ == "__main__":
#     generate_recommendations(evaluate=True)
