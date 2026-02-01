"""Smith-Waterman alignment implementation"""
import numpy as np
from config import GAP_OPEN, GAP_EXTEND, SCORE_THRESHOLD


def smith_waterman_chunks(S, gap_open=GAP_OPEN, gap_extend=GAP_EXTEND, 
                          score_threshold=SCORE_THRESHOLD):
    """
    Smith-Waterman local alignment on chunk similarity matrix (matching notebook exactly)
    
    Args:
        S (numpy.ndarray): Similarity matrix (n_human x n_bact)
        gap_open (float): Gap opening penalty
        gap_extend (float): Gap extension penalty
        score_threshold (float): Minimum similarity score to consider
        
    Returns:
        tuple: (max_score, alignment_path, H_matrix)
            - max_score (float): Maximum alignment score
            - alignment_path (list): List of (i, j) tuples representing aligned positions
            - H_matrix (numpy.ndarray): Full scoring matrix
    """
    n_human, n_bact = S.shape
    H_matrix = np.zeros((n_human + 1, n_bact + 1))
    traceback = np.zeros((n_human + 1, n_bact + 1), dtype=int)
    max_score = 0
    max_pos = (0, 0)

    for i in range(1, n_human + 1):
        for j in range(1, n_bact + 1):
            # Subtract threshold from similarity (notebook logic)
            sim = S[i-1, j-1] - score_threshold
            match = H_matrix[i-1, j-1] + sim
            
            # Gap extension: use gap_extend if continuing a gap, gap_open if starting new gap
            gap_h = H_matrix[i-1, j] + (gap_extend if traceback[i-1, j] == 2 else gap_open)
            gap_b = H_matrix[i, j-1] + (gap_extend if traceback[i, j-1] == 3 else gap_open)

            # Choose best option: 0=stop, 1=match, 2=gap_h, 3=gap_b
            scores = [0, match, gap_h, gap_b]
            best = np.argmax(scores)
            H_matrix[i, j] = scores[best]
            traceback[i, j] = best

            if H_matrix[i, j] > max_score:
                max_score = H_matrix[i, j]
                max_pos = (i, j)

    # Traceback
    alignment = []
    i, j = max_pos
    while i > 0 and j > 0 and H_matrix[i, j] > 0:
        if traceback[i, j] == 1:  # match/mismatch
            alignment.append((i-1, j-1))
            i -= 1
            j -= 1
        elif traceback[i, j] == 2:  # gap in bacteria (move up)
            i -= 1
        elif traceback[i, j] == 3:  # gap in human (move left)
            j -= 1
        else:
            break

    alignment.reverse()
    return max_score, alignment, H_matrix


def find_multiple_alignments(S, gap_open=GAP_OPEN, gap_extend=GAP_EXTEND,
                             min_score=1.0, min_chunks=3, max_alignments=10):
    """
    Find multiple non-overlapping alignment regions
    
    Args:
        S (numpy.ndarray): Similarity matrix
        gap_open (float): Gap opening penalty
        gap_extend (float): Gap extension penalty
        min_score (float): Minimum score for an alignment to be kept
        min_chunks (int): Minimum number of chunks in an alignment
        max_alignments (int): Maximum number of alignments to find
        
    Returns:
        list: List of (score, alignment) tuples
    """
    alignments = []
    S_work = S.copy()
    
    for _ in range(max_alignments):
        score, alignment, _ = smith_waterman_chunks(S_work, gap_open, gap_extend)
        
        # Stop if score too low or alignment too short
        if score < min_score or len(alignment) < min_chunks:
            break
        
        alignments.append((score, alignment))
        
        # Mask the aligned region to find next alignment
        for i, j in alignment:
            S_work[i, j] = 0
    
    return alignments
