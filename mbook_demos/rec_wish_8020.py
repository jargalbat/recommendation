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
# from db_connection import get_session
# from sqlalchemy import text
# import time
# from sklearn.model_selection import train_test_split
#
# # File or Database
# useDataFile = True
# print_user_ids = []
# # print_user_ids = [452553, 12449, 13042, 2527, 286212, 104207]
# top_n = 5
#
# # Suggested 6-10
# threshold = 1
#
# # File path
# wishlistFilePath = 'data/wishlist.csv'
# purchaseHistoryFilePath = 'data/purchase_history.csv'
#
#
# def run_rec8020():
#     total_start_time = time.time()
#     print(
#         f"Total recommendation process started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(total_start_time))}")
#     print("Running recommendation script...")
#
#     # Fetch purchase history as DataFrame
#     if useDataFile:
#         purchase_history = fetch_purchase_history_from_file(purchaseHistoryFilePath)
#     else:
#         purchase_history = fetch_purchase_history()
#
#     # Fetch wishlist data as DataFrame
#     if useDataFile:
#         wishlist = fetch_wishlist_from_file(wishlistFilePath)
#     else:
#         wishlist = fetch_wishlist()
#
#     # Combine purchase history and wishlist data
#     combined_history = pd.concat([purchase_history, wishlist]).drop_duplicates()
#
#     # Split the data into training and test sets
#     train_data, test_data = train_test_split(combined_history, test_size=0.2, random_state=42)
#
#     # Create the user-item matrix for training data
#     purchase_counts = train_data.groupby(['user_id', 'book_id']).size().unstack(fill_value=0)
#     sparse_purchase_counts = sparse.csr_matrix(purchase_counts)
#     cosine_similarities = cosine_similarity(sparse_purchase_counts.T)
#     user_id_to_index = {user_id: index for index, user_id in enumerate(purchase_counts.index)}
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
#         recommended_indices = np.argsort(similarities)[::-1][:n]
#         recommended_items = list(purchase_counts.columns[recommended_indices])
#         purchased_items = list(purchase_counts.columns[purchase_counts.loc[user_id] > 0])
#         recommended_items = [item for item in recommended_items if item not in purchased_items]
#         return recommended_items
#
#     # Fetch book details
#     if useDataFile:
#         book_details = fetch_books_from_file('../data/books_authors.csv')
#     else:
#         book_details = fetch_books()
#
#     # Run recommendations for all users in the test set
#     test_user_ids = test_data['user_id'].unique()
#     recommended_user_count = 0
#     precision_scores = []
#     recall_scores = []
#
#     start_time = time.time()
#     recommendations_to_insert = []
#
#     for user_id in test_user_ids:
#         recommendations = recommend_items(user_id)
#         recommended_user_count += 1
#
#         # Calculate precision and recall for the user
#         relevant_items = test_data[test_data['user_id'] == user_id]['book_id'].values
#         num_relevant_items = len([item for item in recommendations if item in relevant_items])
#         precision = num_relevant_items / len(recommendations) if len(recommendations) > 0 else 0
#         recall = num_relevant_items / len(relevant_items) if len(relevant_items) > 0 else 0
#         precision_scores.append(precision)
#         recall_scores.append(recall)
#
#         # Accumulate recommendations for batch insert
#         recommendations_to_insert.extend([(user_id, book_id) for book_id in recommendations])
#
#         if user_id in print_user_ids:
#             recommended_books = book_details[book_details['book_id'].isin(recommendations)]
#             print(f"Recommendations for user {user_id}: {recommendations}")
#             print(f"Book titles for recommendations for user {user_id}:")
#             print(recommended_books[['book_id', 'book_title']].to_string(index=False))
#
#     recommendation_end_time = time.time()
#
#     print(f"Recommendation calculation started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
#     print(
#         f"Recommendation calculation ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(recommendation_end_time))}")
#     print(f"Total recommendation calculation time: {recommendation_end_time - start_time:.2f} seconds")
#     print(f"Total number of users recommended: {recommended_user_count}")
#
#     # Calculate and print the average precision and recall
#     average_precision = np.mean(precision_scores)
#     average_recall = np.mean(recall_scores)
#     print(f"Average precision: {average_precision:.4f}")
#     print(f"Average recall: {average_recall:.4f}")
#
#     # Clear the recommended_books table if not using file
#     clear_start_time = time.time()
#     if not useDataFile:
#         clear_recommended_books()
#     clear_end_time = time.time()
#     print(f"Clear started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(clear_start_time))}")
#     print(f"Clear ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(clear_end_time))}")
#     print(f"Total clear time: {clear_end_time - clear_start_time:.2f} seconds")
#
#     # Insert or export all recommendations in batch
#     if useDataFile:
#         export_recommendations_to_file(recommendations_to_insert, '../data/recommendations.csv')
#     else:
#         insert_recommendations_batch(recommendations_to_insert)
#
#     total_end_time = time.time()
#     print(
#         f"Total recommendation process ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(total_end_time))}")
#     print(f"Total recommendation process time: {total_end_time - total_start_time:.2f} seconds")
#
#
# # Clear the recommended_books table
# def clear_recommended_books():
#     print("Clearing recommended books")
#     session = get_session("mplus_bp_newsfeed")
#     query = "DELETE FROM recommended_books"
#     session.execute(text(query))
#     session.commit()
#     session.close()
#
#
# # Fetch purchase history
# def fetch_purchase_history():
#     print("Fetching purchase history")
#     session = get_session("mplus_bp_server")
#     query = """
# SELECT DISTINCT u.user_id, b.id AS book_id
# FROM unlocks u
# JOIN books b ON (u.model_type = 'audio_book' AND u.model_id = b.audio_book_id)
#              OR (u.model_type = 'ebook' AND u.model_id = b.ebook_id)
# WHERE u.model_type IN ('audio_book', 'ebook')
# AND u.user_id IN (
#     SELECT user_id
#     FROM unlocks
#     WHERE model_type IN ('audio_book', 'ebook')
#     GROUP BY user_id
#     HAVING COUNT(DISTINCT model_id) >= 5
# )
# ORDER BY u.user_id
# LIMIT 500000;
#     """
#
#     start_time = time.time()
#     result = session.execute(text(query))
#     end_time = time.time()
#
#     fetch_time = end_time - start_time
#     print(f"Fetch time: {fetch_time:.2f} seconds")
#
#     result_list = result.fetchall()
#     df = pd.DataFrame(result_list, columns=['user_id', 'book_id'])
#     print(f"size: {len(df)}")
#
#     session.close()
#     return df
#
#
# # Fetch book details
# def fetch_books():
#     print("Fetching books...")
#     session = get_session("mplus_bp_server")
#     query = """
# SELECT
#     b.id AS book_id,
#     b.title AS book_title,
#     b.author_id,
#     a.name AS author_name
# FROM
#     books b
# JOIN
#     authors a ON b.author_id = a.id;
#     """
#
#     start_time = time.time()
#     result = session.execute(text(query))
#     end_time = time.time()
#
#     fetch_time = end_time - start_time
#     print(f"Fetch time: {fetch_time:.2f} seconds")
#
#     result_list = result.fetchall()
#     df = pd.DataFrame(result_list, columns=['book_id', 'book_title', 'author_id', 'author_name'])
#     print(f"size: {len(df)}")
#
#     session.close()
#     return df
#
#
# def fetch_purchase_history_from_file(file_path):
#     print("Fetching purchase history from file")
#     start_time = time.time()
#     df = pd.read_csv(file_path)
#     end_time = time.time()
#     fetch_time = end_time - start_time
#     print(f"Fetch time: {fetch_time:.2f} seconds")
#     print(f"Size: {len(df)}")
#     return df
#
#
# # Fetch wishlist data from file
# def fetch_wishlist_from_file(file_path):
#     print("Fetching wishlist from file")
#     start_time = time.time()
#     df = pd.read_csv(file_path)
#     end_time = time.time()
#     fetch_time = end_time - start_time
#     print(f"Fetch time: {fetch_time:.2f} seconds")
#     print(f"Size: {len(df)}")
#     return df
#
#
# # Fetch wishlist data from file
# def fetch_wishlist_from_file(file_path):
#     print("Fetching wishlist from file")
#     start_time = time.time()
#     df = pd.read_csv(file_path)
#     end_time = time.time()
#     fetch_time = end_time - start_time
#     print(f"Fetch time: {fetch_time:.2f} seconds")
#     print(f"Size: {len(df)}")
#     return df
#
#
# # Fetch wishlist data
# def fetch_wishlist():
#     print("Fetching wishlist data")
#     session = get_session("mplus_bp_server")
#     query = """
# SELECT user_id, wishlistable_id AS book_id
# FROM wishlists
# WHERE wishlistable_type = 'book'
# AND user_id IN (
#     SELECT user_id
#     FROM wishlists
#     WHERE wishlistable_type = 'book'
#     GROUP BY user_id
#     HAVING COUNT(wishlistable_id) >= 5
# );
#     """
#     start_time = time.time()
#     result = session.execute(text(query))
#     end_time = time.time()
#
#     fetch_time = end_time - start_time
#     print(f"Fetch time: {fetch_time:.2f} seconds")
#
#     result_list = result.fetchall()
#     df = pd.DataFrame(result_list, columns=['user_id', 'book_id'])
#     print(f"size: {len(df)}")
#
#     session.close()
#     return df
#
#
# # Fetch book details from file
# def fetch_books_from_file(file_path):
#     print("Fetching books from file...")
#     start_time = time.time()
#     df = pd.read_csv(file_path)
#     end_time = time.time()
#     fetch_time = end_time - start_time
#     print(f"Fetch time: {fetch_time:.2f} seconds")
#     print(f"Size: {len(df)}")
#     return df
#
#
# # Insert recommendations into the recommended_books table in batch
# def insert_recommendations_batch(recommendations):
#     session = get_session("mplus_bp_newsfeed")
#     query = text("INSERT INTO recommended_books (user_id, book_id) VALUES (:user_id, :book_id)")
#     session.execute(query, [{'user_id': user_id, 'book_id': book_id} for user_id, book_id in recommendations])
#     session.commit()
#     session.close()
#
#
# # Export recommendations to file
# def export_recommendations_to_file(recommendations, file_path):
#     df = pd.DataFrame(recommendations, columns=['user_id', 'book_id'])
#     df.to_csv(file_path, index=False)
#     print(f"Recommendations exported to {file_path}")
#
#
# run_rec8020()
#
# # threshold >= 2
# # Total number of users recommended: 32849
# # Average precision: 0.1279
# # Average recall: 0.3143
#
#
# # threshold >= 5
# # Total number of users recommended: 17604
# # Average precision: 0.1804
# # Average recall: 0.3277
