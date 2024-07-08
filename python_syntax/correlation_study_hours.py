#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:13:25 2024

@author: jargalbat
"""

import pandas as pd

# Create a DataFrame with the data
data = {
    'Study Hours': [2, 3, 5, 4, 6],
    'Exam Score': [50, 60, 80, 70, 90]
}

df = pd.DataFrame(data)

# Calculate the correlation matrix
correlation_matrix = df.corr()

# Extract the correlation value between 'Study Hours' and 'Exam Score'
correlation_value = correlation_matrix.loc['Study Hours', 'Exam Score']

print(f"Correlation between Study Hours and Exam Score: {correlation_value}")
