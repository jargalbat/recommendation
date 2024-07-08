#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 08:54:53 2024

@author: jargalbat
"""

import pandas as pd

# Load the data from the CSV files
purchases_df = pd.read_csv('user_id_product_id_product_name.csv')
fans_df = pd.read_csv('khaitan_fans.csv')

# Display the first few rows of the purchases data to understand its structure
print(purchases_df.head())

# Display the first few rows of the fans data to understand its structure
print(fans_df.head())

# Filter the purchases to include only unique user-book combinations
unique_author_purchases_df = purchases_df.drop_duplicates(subset=['user_id', 'product_id'])

# Match users from the filtered purchases with those in the fans list
matched_users = unique_author_purchases_df[unique_author_purchases_df['user_id'].isin(fans_df['user_id'])]

# Print the matched users
print(matched_users)

# Save the matched users to a CSV file if needed
matched_users.to_csv('matched_users.csv', index=False)
