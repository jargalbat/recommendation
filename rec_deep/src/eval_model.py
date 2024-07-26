import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tqdm import tqdm

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


def precision_at_k(recommended, relevant, k):
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    return len(set(recommended_k) & relevant_set) / k


def recall_at_k(recommended, relevant, k):
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    return len(set(recommended_k) & relevant_set) / len(relevant_set)


def ndcg_at_k(recommended, relevant, k):
    recommended_k = recommended[:k]
    dcg = 0.0
    for i, rec in enumerate(recommended_k):
        if rec in relevant:
            dcg += 1.0 / np.log2(i + 2)
    idcg = sum([1.0 / np.log2(i + 2) for i in range(min(len(relevant), k))])
    return dcg / idcg if idcg > 0 else 0.0


def evaluate_model(test, model, book_id_mapping, user_id_mapping, k=5):
    precisions = []
    recalls = []
    ndcgs = []

    for user_id in tqdm(test['user_id'].unique()):
        relevant_books = test[test['user_id'] == user_id]['book_id'].values
        if len(relevant_books) == 0:
            continue

        recommendations = recommend_books(user_id, num_recommendations=k)

        precisions.append(precision_at_k(recommendations['book_id'].values, relevant_books, k))
        recalls.append(recall_at_k(recommendations['book_id'].values, relevant_books, k))
        ndcgs.append(ndcg_at_k(recommendations['book_id'].values, relevant_books, k))

    precision = np.mean(precisions)
    recall = np.mean(recalls)
    ndcg = np.mean(ndcgs)

    return precision, recall, ndcg

# Example evaluation
# precision, recall, ndcg = evaluate_model(purchased_books, model, book_id_mapping, user_id_mapping, k=5)
# print(f'Precision@5: {precision:.4f}')
# print(f'Recall@5: {recall:.4f}')
# print(f'NDCG@5: {ndcg:.4f}')
#
# Precision@5: 0.0004
# Recall@5: 0.0003
# NDCG@5: 0.0005
# 100%|██████████| 93749/93749 [48:52<00:00, 31.97it/s]
