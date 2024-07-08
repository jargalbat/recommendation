#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:14:01 2024

@author: jargalbat
"""

import pandas as pd

# Create a DataFrame with the data
data = {
    'Arm Length (cm)': [60, 65, 70, 68, 72],
    'Height (cm)': [160, 170, 180, 175, 185]
}

df = pd.DataFrame(data)

# Calculate the correlation matrix
correlation_matrix = df.corr()

# Extract the correlation value between 'Arm Length (cm)' and 'Height (cm)'
correlation_value = correlation_matrix.loc['Arm Length (cm)', 'Height (cm)']

print(f"Correlation between Arm Length and Height: {correlation_value}")
