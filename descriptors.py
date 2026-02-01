"""Biochemical and structural descriptor computation"""
import os
import pandas as pd
import math
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from collections import Counter
from config import CACHE_DIR
from protein_utils import sanitize_protein_id


def compute_chunk_descriptors(sequence, include_structural=False):
    """
    Compute 16 descriptors for a protein chunk sequence (matching notebook exactly)
    
    BIOCHEMICAL (11): length, aromaticity, aliphatic_fraction, GRAVY, 
    hydrophobic_fraction, polar_fraction, instability_index, charge_at_pH7,
    positive_fraction, negative_fraction, shannon_entropy
    
    STRUCTURAL (4): helix_fraction, sheet_fraction, disorder_fraction, 
    surface_exposed_fraction (not implemented - requires ESM2 structural prediction)
    
    Args:
        sequence (str): Protein sequence
        include_structural (bool): Include structural descriptors (not implemented)
        
    Returns:
        dict: Dictionary of descriptor values
    """
    # Clean sequence
    clean_seq = ''.join([aa for aa in sequence.upper() if aa in 'ACDEFGHIKLMNPQRSTVWY'])
    
    if len(clean_seq) < 2:
        default = {
            "length": len(sequence), "aromaticity": 0.0, "aliphatic_fraction": 0.0,
            "GRAVY": 0.0, "hydrophobic_fraction": 0.0, "polar_fraction": 0.0,
            "instability_index": 0.0, "charge_at_pH7": 0.0, "positive_fraction": 0.0,
            "negative_fraction": 0.0, "shannon_entropy": 0.0
        }
        if include_structural:
            default.update({"helix_fraction": 0.0, "sheet_fraction": 0.0,
                          "disorder_fraction": 0.0, "surface_exposed_fraction": 0.5})
        return default
    
    try:
        analysis = ProteinAnalysis(clean_seq)
    except:
        fallback = {
            "length": len(sequence), "aromaticity": 0.0, "aliphatic_fraction": 0.0,
            "GRAVY": 0.0, "hydrophobic_fraction": 0.0, "polar_fraction": 0.0,
            "instability_index": 0.0, "charge_at_pH7": 0.0, "positive_fraction": 0.0,
            "negative_fraction": 0.0, "shannon_entropy": 0.0
        }
        if include_structural:
            fallback.update({"helix_fraction": 0.0, "sheet_fraction": 0.0,
                           "disorder_fraction": 0.0, "surface_exposed_fraction": 0.5})
        return fallback
    
    L = len(clean_seq)
    
    # Residue groups
    aliphatic = set('AVLIM')
    hydrophobic = set('AVLIMFWP')
    polar = set('STNQCY')
    positive = set('KRH')
    negative = set('DE')
    
    aa_counts = Counter(clean_seq)
    aliphatic_count = sum(aa_counts.get(aa, 0) for aa in aliphatic)
    hydrophobic_count = sum(aa_counts.get(aa, 0) for aa in hydrophobic)
    polar_count = sum(aa_counts.get(aa, 0) for aa in polar)
    positive_count = sum(aa_counts.get(aa, 0) for aa in positive)
    negative_count = sum(aa_counts.get(aa, 0) for aa in negative)
    
    # Shannon entropy
    def shannon_entropy(seq):
        counts = Counter(seq)
        total = len(seq)
        entropy = 0.0
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        return entropy
    
    # Build result with BioPython methods (matching notebook exactly)
    result = {
        "length": len(sequence),
        "aromaticity": round(analysis.aromaticity(), 4),
        "aliphatic_fraction": round(aliphatic_count / L, 4) if L > 0 else 0.0,
        "GRAVY": round(analysis.gravy(), 4),
        "hydrophobic_fraction": round(hydrophobic_count / L, 4) if L > 0 else 0.0,
        "polar_fraction": round(polar_count / L, 4) if L > 0 else 0.0,
        "instability_index": round(analysis.instability_index(), 4),
        "charge_at_pH7": round(analysis.charge_at_pH(7.0), 4),
        "positive_fraction": round(positive_count / L, 4) if L > 0 else 0.0,
        "negative_fraction": round(negative_count / L, 4) if L > 0 else 0.0,
        "shannon_entropy": round(shannon_entropy(clean_seq), 4)
    }
    
    # Add structural descriptors (simplified - not using ESM2 structural prediction)
    if include_structural:
        # Use BioPython's secondary structure prediction as approximation
        try:
            ss = analysis.secondary_structure_fraction()
            result.update({
                "helix_fraction": round(ss[0], 4),
                "sheet_fraction": round(ss[2], 4),
                "disorder_fraction": 0.0,  # Would need ESM2 structural prediction
                "surface_exposed_fraction": 0.5  # Default value
            })
        except:
            result.update({"helix_fraction": 0.0, "sheet_fraction": 0.0,
                          "disorder_fraction": 0.0, "surface_exposed_fraction": 0.5})
    
    return result


def get_or_create_descriptors(chunks_df, protein_id):
    """
    Get descriptors from cache or compute new ones
    
    Args:
        chunks_df (pd.DataFrame): DataFrame containing chunks with 'chunk_seq' column
        protein_id (str): Protein identifier for caching
        
    Returns:
        pd.DataFrame: DataFrame with descriptors for each chunk
    """
    clean_id = sanitize_protein_id(protein_id)
    cache_file = os.path.join(CACHE_DIR, f"{clean_id}_descriptors.parquet")
    
    # Load from cache if exists
    if os.path.exists(cache_file):
        print(f"Loading descriptors for {clean_id} from cache...")
        return pd.read_parquet(cache_file)
    
    # Compute new descriptors
    print(f"Computing descriptors for {clean_id} ({len(chunks_df)} chunks)...")
    descriptors_list = []
    
    for idx, row in chunks_df.iterrows():
        desc = compute_chunk_descriptors(row['chunk_seq'])
        desc['chunk_index'] = row['chunk_index']
        descriptors_list.append(desc)
    
    descriptors_df = pd.DataFrame(descriptors_list)
    
    # Save to cache
    descriptors_df.to_parquet(cache_file, index=False)
    print(f"Saved descriptors to cache")
    
    return descriptors_df


def compare_descriptors(desc1, desc2, keys=None):
    """
    Compare descriptors between two regions
    
    Args:
        desc1 (pd.DataFrame): Descriptors for first region
        desc2 (pd.DataFrame): Descriptors for second region
        keys (list): List of descriptor keys to compare (None = all numeric)
        
    Returns:
        dict: Comparison results
    """
    if keys is None:
        keys = ['gravy', 'aromaticity', 'helix_fraction', 'sheet_fraction', 
                'instability_index', 'charge_at_pH7']
    
    comparison = {}
    for key in keys:
        if key in desc1.columns and key in desc2.columns:
            comparison[key] = {
                'region1_mean': desc1[key].mean(),
                'region2_mean': desc2[key].mean(),
                'difference': desc1[key].mean() - desc2[key].mean()
            }
    
    return comparison
