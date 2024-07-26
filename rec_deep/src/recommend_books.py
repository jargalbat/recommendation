import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load data
books = pd.read_csv('/Users/jargalbat/PROJECTS/mbook_recommendation/src/recommendation/dl/books.csv')
purchased_books = pd.read_csv(
    '/Users/jargalbat/PROJECTS/mbook_recommendation/src/recommendation/dl/purchased_books.csv')

# Create a mapping from book_id to index
book_id_mapping = {id: idx for idx, id in enumerate(books['book_id'].unique())}
user_id_mapping = {id: idx for idx, id in enumerate(purchased_books['user_id'].unique())}

# Load the trained model
model = load_model('/Users/jargalbat/PROJECTS/mbook_recommendation/src/recommendation/dl/recommendation_model.h5')


def recommend_books(user_id, num_recommendations=5):
    # Map user ID to user index
    user_index = user_id_mapping[user_id]

    # Predict scores for all books
    book_indices = np.array(list(book_id_mapping.values()))
    user_indices = np.full_like(book_indices, user_index)
    scores = model.predict([user_indices, book_indices])

    # Get top book indices
    top_indices = np.argsort(-scores.flatten())[:num_recommendations]

    # Map book indices back to book IDs
    top_book_ids = [list(book_id_mapping.keys())[i] for i in top_indices]
    return books[books['book_id'].isin(top_book_ids)]


# Example usage
recommended_books = recommend_books(user_id=12449, num_recommendations=20)
print(recommended_books)
