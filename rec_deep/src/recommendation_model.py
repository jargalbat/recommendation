import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Concatenate, Dense, Dropout

# Load data
books = pd.read_csv('/Users/jargalbat/PROJECTS/mbook_recommendation/src/recommendation/dl/books.csv')
purchased_books = pd.read_csv(
    '/Users/jargalbat/PROJECTS/mbook_recommendation/src/recommendation/dl/purchased_books.csv')

# Create a mapping from book_id to index
book_id_mapping = {id: idx for idx, id in enumerate(books['book_id'].unique())}
user_id_mapping = {id: idx for idx, id in enumerate(purchased_books['user_id'].unique())}

# Apply mappings
purchased_books['book_id'] = purchased_books['book_id'].map(book_id_mapping)
purchased_books['user_id'] = purchased_books['user_id'].map(user_id_mapping)

# Split data
train, test = train_test_split(purchased_books, test_size=0.2, random_state=42)

# Hyperparameters
n_users = len(user_id_mapping)
n_books = len(book_id_mapping)
embedding_size = 50

# Model definition
user_input = Input(shape=(1,))
user_embedding = Embedding(input_dim=n_users, output_dim=embedding_size)(user_input)
user_embedding = Flatten()(user_embedding)

book_input = Input(shape=(1,))
book_embedding = Embedding(input_dim=n_books, output_dim=embedding_size)(book_input)
book_embedding = Flatten()(book_embedding)

concat = Concatenate()([user_embedding, book_embedding])

dense_1 = Dense(128, activation='relu')(concat)
dropout_1 = Dropout(0.5)(dense_1)
dense_2 = Dense(64, activation='relu')(dropout_1)
dropout_2 = Dropout(0.5)(dense_2)
dense_3 = Dense(32, activation='relu')(dropout_2)

output = Dense(1, activation='sigmoid')(dense_3)

model = Model(inputs=[user_input, book_input], outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Model summary
model.summary()

# Prepare training data
x_train = [train['user_id'].values, train['book_id'].values]
y_train = np.ones(len(train))  # Implicit feedback: 1 for each interaction

# Prepare test data
x_test = [test['user_id'].values, test['book_id'].values]
y_test = np.ones(len(test))  # Implicit feedback: 1 for each interaction

# Train the model
history = model.fit(x=x_train, y=y_train, epochs=10, batch_size=64, validation_data=(x_test, y_test), verbose=1)

# Save the model
model.save('/Users/jargalbat/PROJECTS/mbook_recommendation/src/recommendation/dl/recommendation_model.h5')
