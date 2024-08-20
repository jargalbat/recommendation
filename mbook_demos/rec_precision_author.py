# import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.model_selection import train_test_split
# from scipy import sparse
# import time
#
# top_n = 5
# prec_k = 5
# filePath = '../data/purchase_history.csv'
# booksFilePath = 'data/books_authors.csv'
# print_user_ids = [452553, 12449, 13042]
#
#
# def run_rec_precision(threshold):
#     total_start_time = time.time()
#     # print(f"Total recommendation process started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(total_start_time))}")
#     # print("Running recommendation script...")
#
#     # Fetch purchase history as DataFrame from file
#     purchase_history = fetch_purchase_history_from_file(filePath)
#
#     # Filter users based on the threshold
#     purchase_history = filter_users_by_threshold(purchase_history, threshold)
#
#     # Load book titles and author information
#     book_details = fetch_books_from_file(booksFilePath)
#
#     # Compute author similarities
#     author_matrix, author_to_index = compute_author_similarities(book_details)
#
#     # Split data into training and testing sets
#     train_data, test_data = train_test_split(purchase_history, test_size=0.2, random_state=42)
#     # print(f"Training data size: {len(train_data)}, Testing data size: {len(test_data)}")
#
#     # Create the user-item matrix for the training set
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
#
#         # Enhance recommendations with author similarity
#         recommended_authors = book_details[book_details['book_id'].isin(recommended_items)]['author_id'].unique()
#         if recommended_authors.size > 0:
#             author_similarities = author_matrix[[author_to_index[author] for author in recommended_authors]].mean(
#                 axis=0)
#             author_similar_books = \
#             book_details[book_details['author_id'].isin(author_similarities.argsort()[::-1][:n])]['book_id'].tolist()
#         else:
#             author_similar_books = []
#
#         # Combine collaborative filtering and content-based filtering
#         combined_recommendations = list(set(recommended_items + author_similar_books))
#         combined_recommendations = [item for item in combined_recommendations if item not in purchased_items][:n]
#         return combined_recommendations
#
#     # Evaluate the model on the testing set
#     test_user_ids = test_data['user_id'].unique()
#     all_recommendations = {user_id: recommend_items(user_id) for user_id in test_user_ids}
#
#     # Print recommendations for specific users
#     print_recommendations_for_users(print_user_ids, all_recommendations, book_details)
#
#     # Calculate precision and recall
#     precision, recall = calculate_precision_recall(test_data,
#                                                    [(user_id, book_id) for user_id, books in all_recommendations.items()
#                                                     for book_id in books], k=prec_k)
#     print(f"Threshold: {threshold}, Mean Precision@5: {precision:.2f}, Mean Recall@5: {recall:.2f}")
#
#     print("Recommendation process completed")
#
#
# # Function to print recommendations for specific users
# def print_recommendations_for_users(print_user_ids, recommendations, book_details):
#     for user_id in print_user_ids:
#         if user_id in recommendations:
#             recommended_books = book_details[book_details['book_id'].isin(recommendations[user_id])]
#             print(f"Recommendations for user {user_id}: {recommendations[user_id]}")
#             print(f"Book titles for recommendations for user {user_id}:")
#             if not recommended_books.empty:
#                 print(recommended_books[['book_id', 'book_title', 'author_id', 'author_name']].to_string(index=False))
#             else:
#                 print("No recommendations found")
#
#
# def filter_users_by_threshold(purchase_history, threshold):
#     user_counts = purchase_history['user_id'].value_counts()
#     filtered_users = user_counts[user_counts >= threshold].index
#     return purchase_history[purchase_history['user_id'].isin(filtered_users)]
#
#
# def calculate_precision_recall(test_data, recommendations, k=prec_k):
#     test_set = set((row['user_id'], row['book_id']) for _, row in test_data.iterrows())
#     user_recommendations = {}
#
#     for user_id, book_id in recommendations:
#         if user_id not in user_recommendations:
#             user_recommendations[user_id] = []
#         user_recommendations[user_id].append(book_id)
#
#     precisions = []
#     recalls = []
#
#     for user_id in test_data['user_id'].unique():
#         true_positives = 0
#         recommended_books = user_recommendations.get(user_id, [])
#         relevant_books = test_data[test_data['user_id'] == user_id]['book_id'].tolist()
#
#         for book_id in recommended_books[:k]:
#             if book_id in relevant_books:
#                 true_positives += 1
#
#         precision = true_positives / k
#         recall = true_positives / len(relevant_books) if len(relevant_books) > 0 else 0
#
#         precisions.append(precision)
#         recalls.append(recall)
#
#     mean_precision = np.mean(precisions)
#     mean_recall = np.mean(recalls)
#
#     return mean_precision, mean_recall
#
#
# # Fetch purchase history from file
# def fetch_purchase_history_from_file(file_path):
#     # print("Fetching purchase history from file")
#     start_time = time.time()
#     df = pd.read_csv(file_path)
#     end_time = time.time()
#     fetch_time = end_time - start_time
#     # print(f"Fetch time: {fetch_time:.2f} seconds")
#     # print(f"Size: {len(df)}")
#     return df
#
#
# # Fetch book details from file
# def fetch_books_from_file(file_path):
#     # print("Fetching books from file...")
#     start_time = time.time()
#     df = pd.read_csv(file_path)
#     end_time = time.time()
#     fetch_time = end_time - start_time
#     # print(f"Fetch time: {fetch_time:.2f} seconds")
#     # print(f"Size: {len(df)}")
#     return df
#
#
# def compute_author_similarities(book_details):
#     authors = book_details[['author_id', 'author_name']].drop_duplicates().reset_index(drop=True)
#     author_to_index = {author_id: index for index, author_id in enumerate(authors['author_id'])}
#     author_matrix = sparse.eye(len(author_to_index)).toarray()  # Convert to dense NumPy array
#     return author_matrix, author_to_index
#
#
# # Example usage with different thresholds
# for threshold in [1, 5, 10, 15, 20]:
#     run_rec_precision(threshold)
#
# # books >= 2
# # Mean Precision@5: 0.13
# # Mean Recall@5: 0.32
#
# # books >= 5
# # Mean Precision@5: 0.18
# # Mean Recall@5: 0.33
#
# # books >= 10
# # Mean Precision@5: 0.23
# # Mean Recall@5: 0.32
#
# # books >= 15
# # Mean Precision@5: 0.26
# # Mean Recall@5: 0.27
#
# # books >= 20
# # Mean Precision@5: 0.30
# # Mean Recall@5: 0.24
#
# # Added threshold
# # Threshold: 2, Mean Precision@5: 0.13, Mean Recall@5: 0.32
# # Threshold: 5, Mean Precision@5: 0.19, Mean Recall@5: 0.33
# # Threshold: 10, Mean Precision@5: 0.23, Mean Recall@5: 0.33
# # Threshold: 15, Mean Precision@5: 0.26, Mean Recall@5: 0.27
# # Threshold: 20, Mean Precision@5: 0.29, Mean Recall@5: 0.23
#
# # Cross-validation
# # Threshold: 2, Mean Precision@5: 0.13, Mean Recall@5: 0.32
# # Threshold: 5, Mean Precision@5: 0.19, Mean Recall@5: 0.33
# # Threshold: 6, Mean Precision@5: 0.20, Mean Recall@5: 0.33
# # Threshold: 7, Mean Precision@5: 0.21, Mean Recall@5: 0.33
# # Threshold: 8, Mean Precision@5: 0.22, Mean Recall@5: 0.33
# # Threshold: 9, Mean Precision@5: 0.22, Mean Recall@5: 0.33
# # Threshold: 10, Mean Precision@5: 0.23, Mean Recall@5: 0.33
# # Threshold: 11, Mean Precision@5: 0.23, Mean Recall@5: 0.33
# # Threshold: 12, Mean Precision@5: 0.24, Mean Recall@5: 0.33
# # Threshold: 13, Mean Precision@5: 0.24, Mean Recall@5: 0.33 --- Better
# # Threshold: 14, Mean Precision@5: 0.25, Mean Recall@5: 0.29
# # Threshold: 15, Mean Precision@5: 0.26, Mean Recall@5: 0.27
# # Threshold: 20, Mean Precision@5: 0.29, Mean Recall@5: 0.24
#
#
# # Books and author based
# # Threshold: 1
# # Mean Precision@5: 0.07
# # Mean Recall@5: 0.17
# # Threshold: 5
# # Mean Precision@5: 0.10
# # Mean Recall@5: 0.18
# # Threshold: 10
# # Mean Precision@5: 0.12
# # Mean Recall@5: 0.18
# # Threshold: 15
# # Mean Precision@5: 0.13
# # Mean Recall@5: 0.14
# # Threshold: 20
# # Mean Precision@5: 0.15
# # Mean Recall@5: 0.12