# import pandas as pd
# from surprise import Dataset, Reader, SVD
# from surprise.model_selection import train_test_split
#
# # Load the purchase history data
# file_path = '../data/purchase_history_5.csv'
# purchase_history = pd.read_csv(file_path)
#
# # Add a 'rating' column with a value of 1 for each purchase
# purchase_history['rating'] = 1
#
# # Load book metadata
# book_metadata_path = '../data/books.csv'
# book_metadata = pd.read_csv(book_metadata_path)
#
# # Load data into Surprise
# reader = Reader(rating_scale=(1, 1))
# data = Dataset.load_from_df(purchase_history[['user_id', 'book_id', 'rating']], reader)
#
# # Split the data into training and test sets
# trainset, testset = train_test_split(data, test_size=0.2)
#
# # Use the SVD algorithm
# algo = SVD()
#
# # Train the algorithm on the training set
# algo.fit(trainset)
#
# # Function to get top N book recommendations for a specific user
# def get_top_n_recommendations(user_id, n=10):
#     # Get a list of all book_ids
#     all_book_ids = purchase_history['book_id'].unique()
#
#     # Get a list of books the user has already purchased
#     user_purchased_books = purchase_history[purchase_history['user_id'] == user_id]['book_id'].unique()
#
#     # Predict scores for all books the user hasn't purchased yet
#     predictions = []
#     for book_id in all_book_ids:
#         if book_id not in user_purchased_books:
#             predictions.append((book_id, algo.predict(user_id, book_id).est))
#
#     # Sort the predictions by estimated rating and return the top N
#     predictions.sort(key=lambda x: x[1], reverse=True)
#     top_books = [book_id for book_id, _ in predictions[:n]]
#
#     # Merge with book metadata to get book titles
#     top_books_with_titles = book_metadata[book_metadata['book_id'].isin(top_books)]
#     return top_books_with_titles[['book_id', 'book_title']]
#
# # User IDs
# user_ids = [12449, 13042, 2527, 286212, 104207]
#
# # Get top book recommendations for each user
# for user_id in user_ids:
#     print(f"Top books for user {user_id}:")
#     top_n_books = get_top_n_recommendations(user_id, n=5)
#     print(top_n_books)
#     print()
