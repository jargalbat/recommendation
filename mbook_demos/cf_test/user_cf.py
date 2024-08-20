# from book_lens import BookLens
# from surprise import KNNBasic
# import heapq
# from collections import defaultdict
# from operator import itemgetter
#
# # Uncomment the appropriate test subject
# # test_subject = 452553  # Khaitan fan, 2 books
# test_subject = 12449  # Horror books fan
# # test_subject = 13042  # Jagaa
# # test_subject = 2527  # Tuvshin
# # test_subject = 286212  # Horror books fan
# # test_subject = 104207  # History fan
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
# pos = 0
# for item_id, rating_sum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
#     if item_id not in purchased:
#         book_id = train_set.to_raw_iid(item_id)
#         print(bl.get_book_title(int(book_id)), rating_sum)
#         pos += 1
#         if pos >= top_n:
#             break
