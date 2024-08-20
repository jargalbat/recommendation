# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
# from scipy.sparse import csr_matrix
# from sklearn.model_selection import train_test_split
# import numpy as np
# import time
#
# # Load the purchase history data
# file_path = '../data/purchase_history_5.csv'
# purchase_history = pd.read_csv(file_path)
#
# # Load book metadata
# book_metadata_path = '../data/books.csv'
# book_metadata = pd.read_csv(book_metadata_path)
#
# # Split the data into training and test sets
# train_data, test_data = train_test_split(purchase_history, test_size=0.2, random_state=42)
#
# # Create a user-item interaction matrix for training data
# user_book_matrix = train_data.pivot_table(index='user_id', columns='book_id', aggfunc='size', fill_value=0)
#
# # Convert the user-item interaction matrix to a sparse matrix
# user_book_sparse = csr_matrix(user_book_matrix.values)
#
# # Compute cosine similarity between users
# user_similarity = cosine_similarity(user_book_sparse)
# user_sim_df = pd.DataFrame(user_similarity, index=user_book_matrix.index, columns=user_book_matrix.index)
#
# # Function to get book recommendations for a user based on similar users
# def get_top_n_recommendations(user_id, num_recommendations=10):
#     if user_id not in user_sim_df.index:
#         return []
#
#     # Get similar users and their similarity scores
#     similar_users = user_sim_df.loc[user_id].sort_values(ascending=False).drop(user_id)
#
#     # Map indices to match the sparse matrix
#     similar_users_indices = [user_book_matrix.index.get_loc(uid) for uid in similar_users.index]
#
#     # Weighted sum of the books purchased by similar users
#     weighted_sum = user_book_sparse[similar_users_indices].T.dot(similar_users.values)
#
#     # Get the index of the current user
#     user_index = user_book_matrix.index.get_loc(user_id)
#
#     # Remove books already purchased by the user
#     user_purchased_books = user_book_sparse[user_index].toarray().flatten()
#     weighted_sum[user_purchased_books > 0] = 0
#
#     # Sort by weighted sum to get the top N recommendations
#     top_books_indices = np.argsort(weighted_sum)[::-1][:num_recommendations]
#
#     return user_book_matrix.columns[top_books_indices]
#
# # Function to evaluate Precision@K and Recall@K
# def evaluate_recommendations(test_data, num_recommendations=5):
#     # Create the user-item interaction matrix for the test data
#     test_user_book_matrix = test_data.pivot_table(index='user_id', columns='book_id', aggfunc='size', fill_value=0)
#
#     precision_at_k = []
#     recall_at_k = []
#
#     for user_id in test_user_book_matrix.index:
#         # Get the actual books purchased by the user in the test set
#         actual_books = set(test_user_book_matrix.columns[test_user_book_matrix.loc[user_id] > 0])
#
#         # Get the recommended books for the user
#         recommended_books = get_top_n_recommendations(user_id, num_recommendations)
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
#     # Calculate average Precision@K and Recall@K
#     avg_precision_at_k = np.mean(precision_at_k)
#     avg_recall_at_k = np.mean(recall_at_k)
#
#     return avg_precision_at_k, avg_recall_at_k
#
# # Get top book recommendations for each user and export to CSV
# def recommend_and_export_all_users(output_path, num_recommendations=5):
#     recommendations = []
#     all_user_ids = user_book_matrix.index
#
#     for user_id in all_user_ids:
#         top_books = get_top_n_recommendations(user_id, num_recommendations)
#         for book_id in top_books:
#             recommendations.append((user_id, book_id))
#
#     recommendations_df = pd.DataFrame(recommendations, columns=['user_id', 'book_id'])
#     recommendations_df.to_csv(output_path, index=False)
#
# # Specify output file path
# output_file_path = '../data/sk_cosine_results.csv'
#
# # Measure and print the calculation time
# start_time = time.time()
#
# # Run recommendations and export
# recommend_and_export_all_users(output_file_path, num_recommendations=5)
#
# end_time = time.time()
# print(f"Total recommendation calculation time: {end_time - start_time:.2f} seconds")
#
# # Evaluate the recommendations
# start_eval_time = time.time()
# avg_precision, avg_recall = evaluate_recommendations(test_data, num_recommendations=5)
# end_eval_time = time.time()
#
# print(f'Average Precision@5: {avg_precision:.4f}')
# print(f'Average Recall@5: {avg_recall:.4f}')
# print(f"Total evaluation time: {end_eval_time - start_eval_time:.2f} seconds")
