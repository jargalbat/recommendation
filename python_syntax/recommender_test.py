import numpy as np
import pandas as pd

column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('u.data', sep='\t', names=column_names)
df.head()

movie_titles = pd.read_csv('Movie_Id_Titles')

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
%matplotlib inline
df.groupby('title')

