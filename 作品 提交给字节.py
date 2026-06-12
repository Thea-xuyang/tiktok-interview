import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.sparse import csr_matrix, save_npz
import os
import json

# 路径配置
DATA_PATH = 'ml-1m'
OUTPUT_PATH = 'output'
os.makedirs(OUTPUT_PATH, exist_ok=True)

# 数据加载与清洗
print("1. Loading and cleaning data...")
ratings_cols = ['UserID', 'MovieID', 'Rating', 'Timestamp']
ratings = pd.read_csv(
    os.path.join(DATA_PATH, 'ratings.dat'),
    sep='::',
    names=ratings_cols,
    engine='python',
    encoding='latin-1'
)

movies_cols = ['MovieID', 'Title', 'Genres']
movies = pd.read_csv(
    os.path.join(DATA_PATH, 'movies.dat'),
    sep='::',
    names=movies_cols,
    engine='python',
    encoding='latin-1'
)

ratings = ratings[(ratings['Rating'] >= 1) & (ratings['Rating'] <= 5)]
ratings = ratings.drop_duplicates(subset=['UserID', 'MovieID'], keep='first')

print(f"Unique users: {ratings['UserID'].nunique()}")
print(f"Unique movies: {ratings['MovieID'].nunique()}")
print(f"Total ratings: {len(ratings)}")

# 索引映射构建
print("\n2. Creating user and movie mappings...")
unique_users = sorted(ratings['UserID'].unique())
unique_movies = sorted(ratings['MovieID'].unique())

user_to_idx = {user: i for i, user in enumerate(unique_users)}
movie_to_idx = {movie: i for i, movie in enumerate(unique_movies)}

n_users = len(unique_users)
n_movies = len(unique_movies)
print(f"Users: {n_users}, Movies: {n_movies}")

# 构建完整稀疏评分矩阵
print("\n3. Building full sparse rating matrix...")
rows = ratings['UserID'].map(user_to_idx).values
cols = ratings['MovieID'].map(movie_to_idx).values
data = ratings['Rating'].values
rating_matrix = csr_matrix((data, (rows, cols)), shape=(n_users, n_movies))

print(f"Matrix shape: {rating_matrix.shape}")
print(f"Non-zero entries: {rating_matrix.nnz}")
sparsity = (1 - rating_matrix.nnz / (n_users * n_movies)) * 100
print(f"Sparsity: {sparsity:.4f}%")

# 训练集与测试集划分
print("\n4. Splitting train and test datasets...")
ratings_train, ratings_test = train_test_split(
    ratings, test_size=0.2, random_state=42, stratify=ratings['Rating']
)

# 训练矩阵
rows_train = ratings_train['UserID'].map(user_to_idx).values
cols_train = ratings_train['MovieID'].map(movie_to_idx).values
data_train = ratings_train['Rating'].values
rating_matrix_train = csr_matrix((data_train, (rows_train, cols_train)), shape=(n_users, n_movies))

# 测试矩阵
rows_test = ratings_test['UserID'].map(user_to_idx).values
cols_test = ratings_test['MovieID'].map(movie_to_idx).values
data_test = ratings_test['Rating'].values
rating_matrix_test = csr_matrix((data_test, (rows_test, cols_test)), shape=(n_users, n_movies))

print(f"Train non-zero: {rating_matrix_train.nnz}")
print(f"Test non-zero: {rating_matrix_test.nnz}")

# 保存稀疏矩阵
print("\n5. Saving sparse matrices...")
save_npz(os.path.join(OUTPUT_PATH, 'rating_matrix_full.npz'), rating_matrix)
save_npz(os.path.join(OUTPUT_PATH, 'rating_matrix_train.npz'), rating_matrix_train)
save_npz(os.path.join(OUTPUT_PATH, 'rating_matrix_test.npz'), rating_matrix_test)

# 电影类型特征处理
print("\n6. Processing movie genre features...")
movies['Genres_List'] = movies['Genres'].str.split('|')
all_genres = sorted({g for genres in movies['Genres_List'] for g in genres})

genre_rows = []
genre_cols = []
genre_data = []
for i, row in movies.iterrows():
    for g in row['Genres_List']:
        genre_rows.append(i)
        genre_cols.append(all_genres.index(g))
        genre_data.append(1)

genre_matrix = csr_matrix((genre_data, (genre_rows, genre_cols)), shape=(len(movies), len(all_genres)))
save_npz(os.path.join(OUTPUT_PATH, 'genre_matrix.npz'), genre_matrix)
print(f"Genre matrix shape: {genre_matrix.shape}")

# 保存元数据与映射关系
print("\n7. Saving metadata and mappings...")
metadata = {
    'n_users': n_users,
    'n_movies': n_movies,
    'n_ratings_total': len(ratings),
    'n_ratings_train': len(ratings_train),
    'n_ratings_test': len(ratings_test),
    'sparsity_percent': sparsity,
    'movie_genres': all_genres,
    'n_genres': len(all_genres)
}

with open(os.path.join(OUTPUT_PATH, 'metadata.json'), 'w') as f:
    json.dump(metadata, f, indent=2)

user_mapping = {int(k): int(v) for k, v in user_to_idx.items()}
movie_mapping = {int(k): int(v) for k, v in movie_to_idx.items()}

with open(os.path.join(OUTPUT_PATH, 'user_mapping.json'), 'w') as f:
    json.dump(user_mapping, f, indent=2)

with open(os.path.join(OUTPUT_PATH, 'movie_mapping.json'), 'w') as f:
    json.dump(movie_mapping, f, indent=2)

# 保存说明文档
print("\n8. Generating project documentation...")
with open(os.path.join(OUTPUT_PATH, 'sparse_matrix_explanation.txt'), 'w') as f:
    f.write("SPARSE MATRIX INFORMATION\n")
    f.write(f"Matrix dimensions: {n_users} users × {n_movies} movies\n")
    f.write(f"Total possible entries: {n_users * n_movies:,}\n")
    f.write(f"Actual ratings: {rating_matrix.nnz:,}\n")
    f.write(f"Sparsity: {sparsity:.4f}%\n\n")
    f.write("Files generated:\n")
    f.write("- rating_matrix_full.npz: Complete user-movie rating matrix\n")
    f.write("- rating_matrix_train.npz: Training subset\n")
    f.write("- rating_matrix_test.npz: Test subset\n")
    f.write("- genre_matrix.npz: Movie genre features\n")
    f.write("- metadata.json: Dataset statistics\n")
    f.write("- user_mapping.json / movie_mapping.json: Index mappings\n\n")
    f.write("Loading method:\n")
    f.write(">>> from scipy.sparse import load_npz\n")
    f.write(">>> mat = load_npz('output/rating_matrix_full.npz')\n")

print("\nProcessing completed successfully.")
print(f"All files saved to: {OUTPUT_PATH}/")