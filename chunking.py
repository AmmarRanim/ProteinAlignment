"""Protein sequence chunking functionality"""
import os
import pandas as pd
from config import (CHUNK_LEN, CHUNK_STRIDE, CACHE_DIR, 
                   MASTER_CHUNKS_DIR, HUMAN_CHUNKS_FILE, BACTERIA_CHUNKS_FILE)
from protein_utils import sanitize_protein_id

# Master parquet files for organisms
MASTER_FILES = {
    'human': os.path.join(MASTER_CHUNKS_DIR, HUMAN_CHUNKS_FILE),
    'bacteria': os.path.join(MASTER_CHUNKS_DIR, BACTERIA_CHUNKS_FILE)
}


def chunk_protein(protein_id, sequence, chunk_len=CHUNK_LEN, stride=CHUNK_STRIDE):
    """
    Generate overlapping chunks from protein sequence
    
    Args:
        protein_id (str): Protein identifier
        sequence (str): Protein sequence
        chunk_len (int): Length of each chunk
        stride (int): Stride between chunks
        
    Returns:
        pd.DataFrame: DataFrame with columns [protein_id, chunk_index, start, end, chunk_seq]
    """
    chunks = []
    L = len(sequence)
    
    # Handle short sequences
    if L <= chunk_len:
        chunks.append({
            'protein_id': protein_id,
            'chunk_index': 0,
            'start': 1,
            'end': L,
            'chunk_seq': sequence
        })
    else:
        start = 0
        chunk_index = 0
        
        while start < L:
            end = min(start + chunk_len, L)
            subseq = sequence[start:end]
            
            chunks.append({
                'protein_id': protein_id,
                'chunk_index': chunk_index,
                'start': start + 1,  # 1-indexed
                'end': end,
                'chunk_seq': subseq
            })
            
            chunk_index += 1
            start += stride
            
            if end == L:
                break
    
    return pd.DataFrame(chunks)


def get_or_create_chunks(protein_id, sequence, organism, master_file_path=None):
    """
    Get chunks from master parquet file or create new ones and append
    
    Args:
        protein_id (str): Protein identifier
        sequence (str): Protein sequence
        organism (str): Organism name (e.g., 'human', 'bacteria')
        master_file_path (str): Path to master parquet file (optional)
        
    Returns:
        pd.DataFrame: Chunks dataframe for this protein
    """
    # Determine master file path
    if master_file_path is None:
        master_filename = MASTER_FILES.get(organism.lower())
        if master_filename:
            # Look in current directory first, then cache
            if os.path.exists(master_filename):
                master_file_path = master_filename
            elif os.path.exists(os.path.join(CACHE_DIR, master_filename)):
                master_file_path = os.path.join(CACHE_DIR, master_filename)
    
    # Try to load from master file
    if master_file_path and os.path.exists(master_file_path):
        print(f"Checking master file: {master_file_path}")
        try:
            master_df = pd.read_parquet(master_file_path)
            
            # Check if protein exists in master file
            if 'protein_id' in master_df.columns:
                protein_chunks = master_df[master_df['protein_id'] == protein_id]
                
                if not protein_chunks.empty:
                    print(f"✓ Found {len(protein_chunks)} chunks for {protein_id} in master file")
                    return protein_chunks.reset_index(drop=True)
                else:
                    print(f"✗ Protein {protein_id} not found in master file")
            
            # Protein not found - create new chunks
            print(f"Creating new chunks for {protein_id}...")
            new_chunks = chunk_protein(protein_id, sequence)
            new_chunks['organism'] = organism
            
            # Append to master file
            print(f"Appending {len(new_chunks)} chunks to master file...")
            combined_df = pd.concat([master_df, new_chunks], ignore_index=True)
            combined_df.to_parquet(master_file_path, index=False)
            print(f"✓ Saved to master file (total proteins: {combined_df['protein_id'].nunique()})")
            
            return new_chunks
            
        except Exception as e:
            print(f"Warning: Could not read master file: {e}")
            print(f"Creating individual cache file instead...")
    
    # Fallback: use individual cache file
    clean_id = sanitize_protein_id(protein_id)
    cache_file = os.path.join(CACHE_DIR, f"{clean_id}_chunks.parquet")
    
    if os.path.exists(cache_file):
        print(f"Loading chunks for {clean_id} from individual cache...")
        return pd.read_parquet(cache_file)
    
    # Create new chunks
    print(f"Creating chunks for {protein_id}...")
    chunks_df = chunk_protein(protein_id, sequence)
    chunks_df['organism'] = organism
    
    # Save to individual cache
    chunks_df.to_parquet(cache_file, index=False)
    print(f"Saved {len(chunks_df)} chunks to individual cache")
    
    return chunks_df
