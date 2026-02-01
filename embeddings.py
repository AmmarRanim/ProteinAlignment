"""Embedding computation and caching"""
import os
import numpy as np
from config import CACHE_DIR
from models import compute_embeddings
from protein_utils import sanitize_protein_id


def get_or_create_embeddings(chunks_df, protein_id):
    """
    Get embeddings from cache or compute new ones
    
    Args:
        chunks_df (pd.DataFrame): DataFrame containing chunks with 'chunk_seq' column
        protein_id (str): Protein identifier for caching
        
    Returns:
        numpy.ndarray: Embeddings matrix (n_chunks x embedding_dim)
    """
    clean_id = sanitize_protein_id(protein_id)
    cache_file = os.path.join(CACHE_DIR, f"{clean_id}_embeddings.npy")
    
    # Load from cache if exists
    if os.path.exists(cache_file):
        print(f"Loading embeddings for {clean_id} from cache...")
        return np.load(cache_file)
    
    # Compute new embeddings
    print(f"Computing embeddings for {clean_id} ({len(chunks_df)} chunks)...")
    sequences = chunks_df['chunk_seq'].tolist()
    embeddings = compute_embeddings(sequences)
    
    # Save to cache
    np.save(cache_file, embeddings)
    print(f"Saved embeddings to cache (shape: {embeddings.shape})")
    
    return embeddings


def compute_similarity_matrix(embeddings1, embeddings2):
    """
    Compute cosine similarity matrix between two sets of embeddings
    
    Args:
        embeddings1 (numpy.ndarray): First set of embeddings (n1 x dim)
        embeddings2 (numpy.ndarray): Second set of embeddings (n2 x dim)
        
    Returns:
        numpy.ndarray: Similarity matrix (n1 x n2)
    """
    # Compute dot product
    similarity_matrix = np.dot(embeddings1, embeddings2.T)
    
    # Normalize by vector norms (cosine similarity)
    norms1 = np.linalg.norm(embeddings1, axis=1, keepdims=True)
    norms2 = np.linalg.norm(embeddings2, axis=1, keepdims=True)
    similarity_matrix = similarity_matrix / (norms1 @ norms2.T + 1e-8)
    
    return similarity_matrix
