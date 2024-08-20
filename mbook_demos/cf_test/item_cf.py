# from book_lens import BookLens
# from surprise import KNNBasic
# import heapq
# from collections import defaultdict
# from operator import itemgetter
#
# # Uncomment the appropriate test subject
# # test_subject = 452553  # Khaitan fan, 2 books
# # test_subject = 12449  # Horror books fan
# # test_subject = 13042  # Jagaa
# # test_subject = 2527  # Tuvshin
# # test_subject = 286212  # Horror books fan
# test_subject = 104207  # History fan
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
# # Define similarity options for item-based collaborative filtering
# sim_options = {
#     'name': 'cosine',
#     'user_based': False  # False for item-based
# }
#
# # Train the model
# model = KNNBasic(sim_options=sim_options)
# model.fit(train_set)
# simsMatrix = model.compute_similarities()
#
# # Get the inner id of the items the test subject has interacted with
# test_user_inner_id = train_set.to_inner_uid(test_subject)
# test_user_ratings = train_set.ur[test_user_inner_id]
#
# # Get the top K items the user rated
# k_neighbors = heapq.nlargest(k, test_user_ratings, key=lambda t: t[1])
#
# # Accumulate ratings for each item, weighted by item similarity
# candidates = defaultdict(float)
# for item_id, rating in k_neighbors:
#     similarity_row = simsMatrix[item_id]
#     for inner_id, score in enumerate(similarity_row):
#         candidates[inner_id] += score * (rating / 1.0)  # Adjust the rating normalization as needed
#
# # Build a dictionary of items the user has already seen
# purchased = {item_id: 1 for item_id, rating in test_user_ratings}
#
# # Get top-rated items from similar items
# pos = 0
# print(f"Book titles for recommendations for user {test_subject}:")
# for item_id, rating_sum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
#     if item_id not in purchased:
#         book_id = train_set.to_raw_iid(item_id)
#         print(f"{bl.get_book_title(int(book_id))}: {rating_sum:.2f}")
#         pos += 1
#         if pos >= top_n:
#             break
