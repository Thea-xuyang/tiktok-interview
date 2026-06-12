import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


import numpy as np
from scipy.sparse import load_npz

# 加载训练集稀疏矩阵
train_matrix = load_npz('output/rating_matrix_train.npz')

# 查看形状 (6040, 3706)
print(train_matrix.shape)

# 如果需要转回坐标格式（Row, Col, Value）
rows, cols = train_matrix.nonzero()
ratings = train_matrix.data

# 假设你已经加载了清洗后的 ratings 数据框
# 1. 生成长尾分布图 (Q1_long_tail.png)
movie_counts = ratings['movieId'].value_counts()
plt.figure(figsize=(10, 5))
plt.hist(movie_counts, bins=100, color='#CC3333', edgecolor='white')
plt.axvline(x=120, color='black', linestyle='--') # 示意热门线
plt.title("Movie Rating Distribution (Long Tail)")
plt.xlabel("Ratings per Movie")
plt.ylabel("Count of Movies")
plt.savefig("Q1_long_tail.png")

# 2. 生成稀疏热力图 (Q1_sparse_heatmap.png)
# 选取 Top 80 用户和 Top 120 电影构建子矩阵
top_users = ratings['userId'].value_counts().head(80).index
top_movies = ratings['movieId'].value_counts().head(120).index
subset = ratings[ratings['userId'].isin(top_users) & ratings['movieId'].isin(top_movies)]
pivot = subset.pivot(index='userId', columns='movieId', values='rating')

plt.figure(figsize=(12, 6))
sns.heatmap(pivot, cmap="YlOrRd", cbar_kws={'label': 'Rating'}, mask=pivot.isnull())
plt.title("Matrix Sparsity Heatmap (Top 80 Users x Top 120 Movies)")
plt.savefig("Q1_sparse_heatmap.png")