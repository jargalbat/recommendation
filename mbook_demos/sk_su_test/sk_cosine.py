# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
#
# # Load the purchase history data
# file_path = '../data/purchase_history_5.csv'
# purchase_history = pd.read_csv(file_path)
#
# # Load book metadata
# book_metadata_path = '../data/books.csv'
# book_metadata = pd.read_csv(book_metadata_path)
#
# # Create a user-item interaction matrix
# user_book_matrix = purchase_history.pivot_table(index='user_id', columns='book_id', aggfunc='size', fill_value=0)
#
# # Compute cosine similarity between users
# user_similarity = cosine_similarity(user_book_matrix)
# user_sim_df = pd.DataFrame(user_similarity, index=user_book_matrix.index, columns=user_book_matrix.index)
#
#
# # Function to get book recommendations for a user based on similar users
# def get_top_n_recommendations(user_id, num_recommendations=10):
#     # Get similar users and their similarity scores
#     similar_users = user_sim_df[user_id].sort_values(ascending=False).drop(user_id)
#
#     # Weighted sum of the books purchased by similar users
#     weighted_sum = user_book_matrix.loc[similar_users.index].T.dot(similar_users)
#
#     # Remove books already purchased by the user
#     user_purchased_books = user_book_matrix.loc[user_id]
#     weighted_sum = weighted_sum[~weighted_sum.index.isin(user_purchased_books[user_purchased_books > 0].index)]
#
#     # Sort by weighted sum to get the top N recommendations
#     top_books = weighted_sum.sort_values(ascending=False).head(num_recommendations).index.tolist()
#
#     # Merge with book metadata to get book titles
#     top_books_with_titles = book_metadata[book_metadata['book_id'].isin(top_books)]
#     return top_books_with_titles[['book_id', 'book_title']]
#
#
# # User IDs
# user_ids = [12449, 13042, 2527, 286212, 104207, 272842, 288152]
#
# # Get top book recommendations for each user
# for user_id in user_ids:
#     print(f"Top books for user {user_id}:")
#     top_n_books = get_top_n_recommendations(user_id, num_recommendations=5)
#     print(top_n_books)
#     print()
