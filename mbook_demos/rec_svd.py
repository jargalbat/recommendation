# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from scipy import sparse
# from scipy.sparse.linalg import svds
# import time
#
# top_n = 5
# prec_k = 5
# filePath = '../data/purchase_history_10.csv'
#
#
# def run_rec_precision():
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
#     purchase_counts = train_data.groupby(['user_id', 'book_id']).size().unstack(fill_value=0).astype(float)
#     sparse_purchase_counts = sparse.csr_matrix(purchase_counts)
#
#     # Perform SVD
#     U, sigma, Vt = svds(sparse_purchase_counts, k=50)
#     sigma = np.diag(sigma)
#
#     # Reconstruct the user-item matrix
#     reconstructed_matrix = np.dot(np.dot(U, sigma), Vt)
#     reconstructed_df = pd.DataFrame(reconstructed_matrix, columns=purchase_counts.columns, index=purchase_counts.index)
#
#     def recommend_items(user_id, n=top_n):
#         if user_id not in reconstructed_df.index:
#             return []
#
#         user_predictions = reconstructed_df.loc[user_id].sort_values(ascending=False)
#         user_history = purchase_counts.loc[user_id].to_numpy().nonzero()[0]
#         recommendations = [book_id for book_id in user_predictions.index if book_id not in user_history][:n]
#         return recommendations
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
#     # Calculate precision and recall
#     precision, recall = calculate_precision_recall(test_data, all_recommendations, k=prec_k)
#     print(f"Mean Precision@5: {precision:.2f}")
#     print(f"Mean Recall@5: {recall:.2f}")
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
# run_rec_precision()
