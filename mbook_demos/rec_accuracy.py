# import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.model_selection import train_test_split
# from scipy import sparse
# import time
#
# top_n = 5
# filePath = '../data/purchase_history.csv'
#
# def run_rec_accuracy():
#     total_start_time = time.time()
#     print(
#         f"Total recommendation process started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(total_start_time))}")
#     print("Running recommendation script...")
#
#     # Fetch purchase history as DataFrame from file
#     purchase_history = fetch_purchase_history_from_file(filePath)
#
#     # Split the data into training and testing sets
#     train_data, test_data = train_test_split(purchase_history, test_size=0.2, random_state=42)
#     print(f"Training data size: {len(train_data)}, Testing data size: {len(test_data)}")
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
#         return recommended_items
#
#     # Fetch book details from file
#     book_details = fetch_books_from_file('../data/books.csv')
#
#     # Evaluate the model on the testing set
#     test_user_ids = test_data['user_id'].unique()
#     all_recommendations = []
#
#     for user_id in test_user_ids:
#         recommendations = recommend_items(user_id)
#         all_recommendations.extend([(user_id, book_id) for book_id in recommendations])
#
#     # Calculate accuracy or another evaluation metric
#     accuracy = calculate_accuracy(test_data, all_recommendations)
#     print(f"Model accuracy: {accuracy:.2f}")
#
#     # Continue with the rest of your logic for recommendations...
#
#
# def calculate_accuracy(test_data, recommendations):
#     test_set = set((row['user_id'], row['book_id']) for _, row in test_data.iterrows())
#     recommended_set = set(recommendations)
#
#     hits = len(test_set & recommended_set)
#     total_recommendations = len(recommended_set)
#     accuracy = hits / total_recommendations if total_recommendations > 0 else 0
#     return accuracy
#
#
# # Fetch purchase history from file
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
# # Example usage
# run_rec_accuracy()
#
# # books >= 2
# # Model accuracy: 0.13
#
# # books >= 5
# # Model accuracy: 0.18
#
# # books >= 10
# # Model accuracy: 0.23
