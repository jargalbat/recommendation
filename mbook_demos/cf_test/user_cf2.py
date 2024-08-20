# from book_lens import BookLens
# from surprise import KNNBasic, Dataset, Reader
# import heapq
# from collections import defaultdict
# from operator import itemgetter
# import pandas as pd
#
# # Define the test subject and parameters
# test_subject = 12449  # Horror books fan
#
# k = 5
# top_n = 5
#
# # Initialize BookLens and load data
# bl = BookLens()
# data = bl.load_book_lens_data()
#
# # Build the full training set
# train_set = data.build_full_trainset()
# print(f"First 5 rows of the training set:\n{list(train_set.all_ratings())[:5]}")
#
# # Define similarity options
# sim_options = {
#     'name': 'cosine',
#     'user_based': True
# }
#
# # Train the model
# model = KNNBasic(sim_options=sim_options)
# model.fit(train_set)
# simsMatrix = model.compute_similarities()
#
# # Get the top-N similar users to the test subject
# test_user_inner_id = train_set.to_inner_uid(test_subject)
# similarity_row = simsMatrix[test_user_inner_id]
#
# # Find similar users
# similar_users = [(inner_id, score) for inner_id, score in enumerate(similarity_row) if inner_id != test_user_inner_id]
# k_neighbors = heapq.nlargest(k, similar_users, key=lambda t: t[1])
#
# # Accumulate ratings for each item, weighted by user similarity
# candidates = defaultdict(float)
# for similar_user in k_neighbors:
#     inner_id, user_similarity_score = similar_user
#     their_ratings = train_set.ur[inner_id]
#     for rating in their_ratings:
#         candidates[rating[0]] += rating[1] * user_similarity_score
#
# # Build a dictionary of items the user has already seen
# purchased = {item_id: 1 for item_id, rating in train_set.ur[test_user_inner_id]}
#
# # Get top-rated items from similar users
# recommended_items = []
# for item_id, rating_sum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
#     if item_id not in purchased:
#         book_id = train_set.to_raw_iid(item_id)
#         recommended_items.append((bl.get_book_title(int(book_id)), rating_sum))
#         if len(recommended_items) >= top_n:
#             break
#
# # Print recommendations
# print(f"Book titles for recommendations for user {test_subject}:")
# for book_title, score in recommended_items:
#     print(f"{book_title}: {score}")
#
# # If you want to print details of the recommendations:
# book_details = pd.read_csv(bl.BOOKS_PATH, names=["book_id", "book_title"], header=0)
# recommended_book_ids = [train_set.to_raw_iid(item_id) for item_id, _ in recommended_items]
# recommended_books = book_details[book_details['book_id'].isin(recommended_book_ids)]
# print(recommended_books[['book_id', 'book_title']].to_string(index=False))
