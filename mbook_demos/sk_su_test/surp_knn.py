# import pandas as pd
# from surprise import Dataset, Reader, KNNBasic
# from surprise.model_selection import train_test_split
# import heapq
# from collections import defaultdict
# from operator import itemgetter
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
# # Use the KNNBasic algorithm for user-based collaborative filtering
# sim_options = {'name': 'cosine', 'user_based': True}
# algo = KNNBasic(sim_options=sim_options)
#
# # Train the algorithm on the training set
# algo.fit(trainset)
# simsMatrix = algo.compute_similarities()
#
#
# # Function to get top N book recommendations for a specific user using user-based collaborative filtering
# def get_top_n_recommendations(user_id, n=10):
#     # Get inner ID of the user
#     testUserInnerID = trainset.to_inner_uid(user_id)
#
#     # Get the top N similar users to our test subject
#     similarityRow = simsMatrix[testUserInnerID]
#     similarUsers = []
#     for innerID, score in enumerate(similarityRow):
#         if innerID != testUserInnerID:
#             similarUsers.append((innerID, score))
#
#     kNeighbors = heapq.nlargest(10, similarUsers, key=lambda t: t[1])
#
#     # Get the books they rated, and add up ratings for each item, weighted by user similarity
#     candidates = defaultdict(float)
#     for similarUser in kNeighbors:
#         innerID = similarUser[0]
#         userSimilarityScore = similarUser[1]
#         theirRatings = trainset.ur[innerID]
#         for rating in theirRatings:
#             candidates[rating[0]] += (rating[1] / 5.0) * userSimilarityScore
#
#     # Build a dictionary of books the user has already seen
#     watched = {}
#     for itemID, rating in trainset.ur[testUserInnerID]:
#         watched[itemID] = 1
#
#     # Get top-rated items from similar users:
#     top_books = []
#     for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
#         if itemID not in watched:
#             bookID = trainset.to_raw_iid(itemID)
#             top_books.append(bookID)
#             if len(top_books) >= n:
#                 break
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
#     top_n_books = get_top_n_recommendations(user_id, n=5)
#     print(top_n_books)
#     print()
