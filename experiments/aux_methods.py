"""
Auxiliary methods for experiments
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import normalize
from sklearn.manifold import TSNE
from sklearn.metrics import pairwise_distances
from matplotlib.markers import MarkerStyle


def vectorize_text_tfidf(df_texts):
    """
    Vectorize texts using TF-IDF and compute pairwise cosine similarities.
    """
    texts = df_texts['value_text'].tolist()
    vectorizer = TfidfVectorizer()
    similarities = {}

    tfidf_matrix = vectorizer.fit_transform(texts)  # (n_users, n_feats)
    sim_matrix = cosine_similarity(tfidf_matrix)    # full (n_users, n_users) matrix

    # store pairwise similarities (only i<j to avoid duplicates)
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            similarities[(df_texts.iloc[i].user_id, df_texts.iloc[j].user_id)] = float(sim_matrix[i, j])

    return sim_matrix, similarities


def plot_similarity_matrix(similarities, user_ids):
    """
    Plot a heatmap of the similarity matrix.
    """
    matrix = np.zeros((len(user_ids), len(user_ids)))

    for (id1, id2), score in similarities.items():
        idx1 = user_ids.index(id1)
        idx2 = user_ids.index(id2)
        matrix[idx1, idx2] = score
        matrix[idx2, idx1] = score  # Symmetric matrix

    # Set diagonal to 1.0 (perfect self-similarity)
    np.fill_diagonal(matrix, 1.0)

    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, fmt=".2f", cmap="coolwarm", xticklabels=user_ids, yticklabels=user_ids)
    plt.title("Cosine Similarity Matrix")
    plt.xlabel("Users")
    plt.ylabel("Users")
    plt.show()



def cluster_tfidf(df_texts, n_clusters=3, method='kmeans', eps=0.35, min_samples=2):
    """
    Cluster users based on TF-IDF vectors.
    method: 'kmeans' | 'agglomerative' | 'dbscan'
    Returns: labels, model, vectorizer, tfidf_matrix
    """
    texts = df_texts['value_text'].tolist()
    users = df_texts['user_id'].tolist()
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)        # sparse (n_users, n_features)
    Xn = normalize(X)                         # normalize so cosine ~ dot product

    if method == 'kmeans':
        model = KMeans(n_clusters=n_clusters, random_state=42).fit(Xn)
        labels = model.labels_
    elif method == 'agglomerative':
        D = pairwise_distances(Xn, metric='cosine')
        model = AgglomerativeClustering(n_clusters=n_clusters, linkage='average').fit(D) # affinity='precomputed'
        labels = model.labels_
    elif method == 'dbscan':
        model = DBSCAN(metric='cosine', eps=eps, min_samples=min_samples).fit(Xn)
        labels = model.labels_
    else:
        raise ValueError("Unknown method")

    sil = None
    if len(set(labels)) > 1 and -1 not in set(labels):  # silhouette needs >=2 clusters (ignore noise)
        try:
            sil = silhouette_score(Xn, labels, metric='cosine')
        except Exception:
            sil = None

    # Print assignments
    for u, lab in zip(users, labels):
        print(f"User {u} -> cluster {lab}")

    print("Silhouette (cosine):", sil)

    return labels, model, vectorizer, X



def visualize_clusters(df_texts, labels, X, title='Cluster visualization'):
    """
    Produce a 2D t-SNE scatter of TF-IDF vectors colored by cluster.
    Annotates user ids and plots cluster centroids (2D mean of cluster points).
    """
    users = df_texts['user_id'].tolist()

    # Ensure dense array
    X_dense = X.toarray() if hasattr(X, 'toarray') else np.array(X)

    # 2D projection
    X2 = TSNE(n_components=2, random_state=42, perplexity=5, init='pca', learning_rate='auto').fit_transform(X_dense)

    labels_arr = np.array(labels)
    plt.figure(figsize=(8,6))
    sns.scatterplot(x=X2[:,0], y=X2[:,1], hue=labels_arr, palette='tab10', legend='full', s=80)

    # annotate points with user ids
    for i, u in enumerate(users):
        plt.text(X2[i,0] + 0.5, X2[i,1] + 0.5, "User "+str(u), fontsize=9)

    # compute and plot 2D centroids for each cluster (ignore noise label -1)
    unique = [l for l in np.unique(labels_arr) if l != -1]
    for l in unique:
        pts = X2[labels_arr == l]
        if len(pts) == 0:
            continue
        cen = pts.mean(axis=0)
        plt.scatter(cen[0], cen[1], s=200, marker=MarkerStyle('X'), color='k', edgecolor='k', linewidth=1)
        plt.text(cen[0], cen[1], f'  C{l} ({len(pts)})', fontsize=9, fontweight='bold')

    plt.title(title)
    plt.xlabel('TSNE-1')
    plt.ylabel('TSNE-2')
    plt.legend(title='cluster')
    plt.tight_layout()
    plt.show()
