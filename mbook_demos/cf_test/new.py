# import pandas as pd
# from surprise import Dataset, Reader, KNNBasic
# import heapq
# from collections import defaultdict
# from operator import itemgetter
#
# # Load purchase history
# df = pd.read_csv('../data/purchase_history_5.csv')  # Adjust path as needed
#
# # Load book titles
# books_df = pd.read_csv('../data/books.csv')  # Adjust path as needed
# book_id_to_title = dict(zip(books_df['book_id'], books_df['book_title']))
#
# # Add implicit rating column (every purchase is treated as a rating of 1.0)
# df['implicit_rating'] = 1.0
#
# # Define a reader for the dataset
# reader = Reader(rating_scale=(1, 1))
# data = Dataset.load_from_df(df[['user_id', 'book_id', 'implicit_rating']], reader)
#
# # Define similarity options
# sim_options = {
#     'name': 'cosine',
#     'user_based': False  # Item-based similarity
# }
#
# # Build the full training set and train the model
# trainset = data.build_full_trainset()
# model = KNNBasic(sim_options=sim_options)
# model.fit(trainset)
#
#
# # Function to recommend items for a user
# def recommend_items(test_user_id, k=5):
#     test_user_inner_id = trainset.to_inner_uid(test_user_id)
#     test_user_ratings = trainset.ur[test_user_inner_id]
#
#     # Accumulate ratings for each item, weighted by item similarity
#     candidates = defaultdict(float)
#     for item_id, rating in test_user_ratings:
#         similarity_row = model.sim[item_id]
#         for inner_id, score in enumerate(similarity_row):
#             if inner_id not in dict(test_user_ratings):
#                 candidates[inner_id] += score * rating
#
#     # Get top-rated items from similar items
#     recommended_items = heapq.nlargest(k, candidates.items(), key=itemgetter(1))
#
#     # Convert inner IDs to raw IDs and get item titles
#     recommended_books = [(trainset.to_raw_iid(item_id), score) for item_id, score in recommended_items]
#
#     # Print recommendations with book titles
#     for book_id, score in recommended_books:
#         book_title = book_id_to_title.get(int(book_id), "Unknown Title")
#         print(f"Book Title: {book_title}, Score: {score}")
#
#
# # Recommend items for the test user
# print(12449)
# recommend_items(test_user_id=12449, k=5)  # Replace with the actual user ID
#
# print(13042)
# recommend_items(test_user_id=13042, k=5)
#
# print(2527)
# recommend_items(test_user_id=2527, k=5)
#
# print(286212)
# recommend_items(test_user_id=286212, k=5)
#
# print(104207)
# recommend_items(test_user_id=104207, k=5)
#
