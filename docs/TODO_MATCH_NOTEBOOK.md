# TODO: Match Notebook JSON Structure Exactly

## Current Status

✅ **Working correctly:**
- Smith-Waterman alignment (39 chunks - matches notebook)
- Descriptors (11 biochemical - matches notebook)
- Functional annotations (Pfam, Prosite, Signal, TM)
- Basic LLM prompt

❌ **Not matching notebook:**
- JSON structure sent to LLM is simplified
- Missing multiple alignment finding
- Missing adaptive filtering
- Missing detailed chunk pair information

## Notebook's Complete JSON Structure

```json
{
  "metadata": {
    "timestamp": "...",
    "version": "..."
  },
  
  "input_sequences": {
    "human": {
      "protein_id": "...",
      "organism": "Homo_sapiens",
      "sequence": "...",
      "length_aa": 393,
      "num_chunks": 77,
      "functional_annotations": {
        "pfam_domains": [...],
        "prosite_motifs": [...],
        "has_signal_peptide": false,
        "tm_helix_count": 0
      }
    },
    "bacteria": { ... }
  },
  
  "parameters": {
    "chunk_length": 10,
    "chunk_stride": 5,
    "gap_open": -0.2,
    "gap_extend": -0.1,
    "score_threshold": 0.5
  },
  
  "similarity_matrix_stats": {
    "shape": [77, 90],
    "min": 0.234,
    "max": 0.987,
    "mean": 0.456,
    "median": 0.445
  },
  
  "alignment_summary": {
    "raw_alignments_found": 15,
    "filtered_alignments": 3,
    "total_human_aa_aligned": 348,
    "total_bact_aa_aligned": 347,
    "best_score": 12.45,
    "best_avg_similarity": 0.876,
    "best_continuity": 0.92
  },
  
  "alignments": [
    {
      "alignment_id": 1,
      "smith_waterman_score": 12.45,
      "num_chunks_aligned": 39,
      "avg_cosine_similarity": 0.876,
      "continuity": 0.92,
      
      "human_region": {
        "start": 45,
        "end": 234,
        "length_aa": 190,
        "coverage_percent": 48.3
      },
      
      "bacteria_region": {
        "start": 78,
        "end": 267,
        "length_aa": 190,
        "coverage_percent": 41.7
      },
      
      "aligned_chunk_pairs": [
        {
          "pair_id": 1,
          "human_chunk_idx": 5,
          "bact_chunk_idx": 8,
          "cosine_similarity": 0.923,
          
          "human_chunk": {
            "sequence": "MEKTAYILGD",
            "start": 45,
            "end": 54,
            "descriptors": {
              "GRAVY": -0.45,
              "aromaticity": 0.12,
              ...
            }
          },
          
          "bacteria_chunk": {
            "sequence": "MEKTAYILGD",
            "start": 78,
            "end": 87,
            "descriptors": {
              "GRAVY": -0.38,
              "aromaticity": 0.15,
              ...
            }
          },
          
          "descriptor_comparison": {
            "GRAVY_diff": 0.07,
            "GRAVY_similar": true,
            ...
          }
        },
        ... // 38 more pairs
      ]
    },
    ... // 2 more alignments
  ]
}
```

## What Needs to be Implemented

### 1. Multiple Alignment Finding
File: `alignment.py`

Add function:
```python
def find_all_alignments(S, gap_open, gap_extend, score_threshold, min_score, min_chunks):
    """Find multiple non-overlapping alignments by masking"""
    # Iteratively find alignments and mask them
    # Return list of all alignments with scores, continuity, etc.
```

### 2. Adaptive Filtering
File: `alignment.py`

Add function:
```python
def filter_alignments_adaptive(alignments, S):
    """Filter alignments using data-driven thresholds"""
    # Keep only high-quality alignments
    # Based on relative score, continuity, similarity
```

### 3. Build Complete JSON
File: `llm_interpretation.py`

Update `prepare_analysis_data()` to build the complete JSON structure matching the notebook.

### 4. Update LLM Prompt
File: `llm_interpretation.py`

Update `generate_llm_prompt_full()` to use the complete JSON data.

## Estimated Work

- **Multiple alignment finding**: 1-2 hours
- **Adaptive filtering**: 1 hour
- **Complete JSON structure**: 2-3 hours
- **Testing**: 1 hour

**Total**: ~5-7 hours of development

## Priority

**Current app is fully functional** with:
- Correct alignment (39 chunks)
- Correct descriptors
- Functional annotations
- LLM interpretation

**Matching exact JSON is optional** - it would make the LLM prompt more detailed but the current version works.

## Decision

Do you want me to:
1. **Implement the complete JSON now** (~5-7 hours)
2. **Keep current simplified version** (works, just less detailed)
3. **Implement later** (app works now, can enhance later)

The app is production-ready as-is. The complete JSON would make LLM responses more detailed but isn't required for functionality.
