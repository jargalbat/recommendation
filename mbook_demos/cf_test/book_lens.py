# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Mon Jul 10 12:20:12 2024
#
# Author: jargalbat
# """
# import csv
# import os
# import sys
# from surprise import Reader, Dataset
# import pandas as pd
#
#
# class BookLens:
#     PURCHASES_PATH = '../data/purchase_history_5.csv'
#     BOOKS_PATH = '../data/books.csv'
#     RECS_PATH = '../data/recommendations.csv'
#
#     book_id_to_title = {}
#     book_title_to_id = {}
#
#     def load_book_lens_data(self):
#         # Look for files relative to the directory we are running from
#         os.chdir(os.path.dirname(sys.argv[0]))
#
#         self.book_id_to_title = {}
#         self.book_title_to_id = {}
#
#         # Load the purchase history CSV, skip the header row if present
#         df = pd.read_csv(self.PURCHASES_PATH, names=["user_id", "book_id"], header=0)
#
#         # Add a default 'implicit rating' column
#         df["implicit_rating"] = 1.0  # Treat each purchase as an implicit rating of 1
#
#         # Define the reader with the correct format
#         reader = Reader(rating_scale=(1, 1))
#
#         # Load the dataset from the DataFrame
#         purchases_dataset = Dataset.load_from_df(df[['user_id', 'book_id', 'implicit_rating']], reader)
#
#         with open(self.BOOKS_PATH, newline='') as csvfile:
#             book_reader = csv.reader(csvfile)
#             next(book_reader)  # skip header line
#             for row in book_reader:
#                 book_id = int(row[0])
#                 book_title = row[1]
#                 self.book_id_to_title[book_id] = book_title
#                 self.book_title_to_id[book_title] = book_id
#
#         return purchases_dataset
#
#     def get_book_title(self, book_id):
#         return self.book_id_to_title.get(book_id, "")
#
#
# if __name__ == "__main__":
#     bl = BookLens()
#     data = bl.load_book_lens_data()
