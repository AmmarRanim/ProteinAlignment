# Usage Guide - Protein Alignment Analysis

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests** (optional but recommended):
   ```bash
   python test_modules.py
   ```

3. **Start the server**:
   ```bash
   python app.py
   ```
   Or double-click `run.bat` on Windows

4. **Open browser** to `http://localhost:5000`

## Module Overview

### 1. `config.py` - Configuration
Contains all configurable parameters:
- `CHUNK_LEN`: Length of each protein chunk (default: 10 aa)
- `CHUNK_STRIDE`: Overlap between chunks (default: 5 aa)
- `GAP_OPEN`: Smith-Waterman gap opening penalty (default: -0.2)
- `GAP_EXTEND`: Gap extension penalty (default: -0.1)
- `SCORE_THRESHOLD`: Minimum similarity score (default: 0.5)

### 2. `models.py` - ESM-2 Model
Handles loading and caching of the ESM-2 protein language model:
- `get_esm2_model()`: Loads model (cached globally)
- `compute_embeddings(sequences)`: Computes embeddings for sequences

### 3. `protein_utils.py` - Protein Handling
Fetches and manages protein sequences:
- `fetch_protein_sequence(protein_id)`: Gets sequence from UniProt or cache
- `clean_sequence(sequence)`: Cleans invalid characters

### 4. `chunking.py` - Sequence Chunking
Splits proteins into overlapping chunks:
- `chunk_protein(protein_id, sequence)`: Creates chunks
- `get_or_create_chunks(protein_id, sequence, organism)`: With caching

### 5. `embeddings.py` - Embedding Computation
Computes and caches ESM-2 embeddings:
- `get_or_create_embeddings(chunks_df, protein_id)`: With caching
- `compute_similarity_matrix(emb1, emb2)`: Cosine similarity

### 6. `alignment.py` - Smith-Waterman Alignment
Implements local alignment algorithm:
- `smith_waterman_chunks(S)`: Finds best alignment
- `find_multiple_alignments(S)`: Finds multiple non-overlapping regions

### 7. `descriptors.py` - Biochemical Descriptors
Computes protein properties:
- `compute_chunk_descriptors(sequence)`: 30+ descriptors
- `get_or_create_descriptors(chunks_df, protein_id)`: With caching
- `compare_descriptors(desc1, desc2)`: Compare regions

### 8. `interpretation.py` - Result Interpretation
Generates human-readable reports:
- `interpret_alignment(...)`: Creates detailed report
- `generate_summary_stats(...)`: Summary statistics

### 9. `app.py` - Flask Application
Main web application:
- `/` - Home page
- `/analyze` - Analysis endpoint (POST)

## Workflow

```
User Input (Protein IDs)
    ↓
Fetch Sequences (protein_utils.py)
    ↓
Create Chunks (chunking.py)
    ↓
Compute Embeddings (embeddings.py + models.py)
    ↓
Compute Similarity Matrix (embeddings.py)
    ↓
Smith-Waterman Alignment (alignment.py)
    ↓
Compute Descriptors (descriptors.py)
    ↓
Generate Interpretation (interpretation.py)
    ↓
Display Results (app.py + templates/index.html)
```

## Caching System

All intermediate results are cached in `cache/` directory:

| File Pattern | Content | Format |
|--------------|---------|--------|
| `{id}.fasta` | Protein sequence | FASTA |
| `{id}_chunks.parquet` | Chunks | Parquet |
| `{id}_embeddings.npy` | ESM-2 embeddings | NumPy |
| `{id}_descriptors.parquet` | Biochemical descriptors | Parquet |

**Benefits**:
- First analysis: ~2-5 minutes
- Subsequent analyses with same protein: ~10-30 seconds

**Clear cache**:
```bash
# Windows
rmdir /s /q cache

# Linux/Mac
rm -rf cache
```

## Example Analysis

### Input
- Human: `P04637` (Tumor protein p53)
- Bacteria: `P0A7B8` (RNA polymerase sigma factor)

### Output
```
Analysis of P04637 (Human) vs P0A7B8 (Bacteria)
======================================================================

Found 1 significant alignment region(s):

Region 1 (Alignment Score: 15.43)
----------------------------------------------------------------------
  Human protein:    positions   45-  120 ( 16 chunks)
  Bacterial protein: positions   78-  145 ( 14 chunks)

  Biochemical Properties:
    Hydrophobicity (GRAVY):
      Human:  -0.45  |  Bacteria:  -0.38  |  Δ:  -0.07
    Aromaticity:
      Human:   0.12  |  Bacteria:   0.15  |  Δ:  -0.03
    Secondary Structure:
      Helix  - Human:   0.34  |  Bacteria:   0.41
      Sheet  - Human:   0.28  |  Bacteria:   0.22
    Charge at pH 7:
      Human:   2.50  |  Bacteria:   1.80  |  Δ:   0.70
    Instability Index:
      Human:  42.30  |  Bacteria:  38.50  |  Δ:   3.80

======================================================================
Summary:
  Total aligned chunk pairs: 30
  Average alignment score: 15.43
```

## Customization

### Change Chunk Size
Edit `config.py`:
```python
CHUNK_LEN = 20      # Larger chunks
CHUNK_STRIDE = 10   # Less overlap
```

### Adjust Alignment Sensitivity
Edit `config.py`:
```python
GAP_OPEN = -0.5        # Stricter gap penalty
SCORE_THRESHOLD = 0.7  # Higher similarity threshold
```

### Use Different Model
Edit `models.py`:
```python
# Change this line:
_esm_model, _esm_alphabet = esm.pretrained.esm2_t33_650M_UR50D()

# To use smaller/larger model:
_esm_model, _esm_alphabet = esm.pretrained.esm2_t12_35M_UR50D()  # Smaller
_esm_model, _esm_alphabet = esm.pretrained.esm2_t36_3B_UR50D()   # Larger
```

## Troubleshooting

### Issue: "Module not found"
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### Issue: "Out of memory"
**Solution**: Use smaller chunks or CPU
```python
# In config.py
CHUNK_LEN = 5  # Smaller chunks
```

### Issue: "Protein not found"
**Solution**: 
- Check UniProt ID is correct
- Try accessing https://www.uniprot.org/uniprot/{ID}.fasta manually
- Check internet connection

### Issue: "Model loading is slow"
**Solution**: First run downloads ~2.5GB model. Subsequent runs are faster.

### Issue: "Analysis takes too long"
**Solution**:
- Use GPU if available
- Reduce chunk size
- Use smaller ESM-2 model

## Performance Tips

1. **Use GPU**: 10-20x faster for embeddings
2. **Batch similar analyses**: Cache is reused
3. **Adjust chunk size**: Smaller = faster but less context
4. **Keep cache**: Don't delete unless necessary

## API Usage

You can also use the API directly:

```python
import requests

response = requests.post('http://localhost:5000/analyze', json={
    'human_protein_id': 'P04637',
    'bacteria_protein_id': 'P0A7B8'
})

result = response.json()
print(result['interpretation'])
```

## Advanced Usage

### Programmatic Access

```python
from protein_utils import fetch_protein_sequence
from chunking import get_or_create_chunks
from embeddings import get_or_create_embeddings, compute_similarity_matrix
from alignment import smith_waterman_chunks
from descriptors import get_or_create_descriptors
from interpretation import interpret_alignment

# Fetch sequences
human_seq = fetch_protein_sequence('P04637')
bact_seq = fetch_protein_sequence('P0A7B8')

# Process
human_chunks = get_or_create_chunks('P04637', human_seq, 'human')
bact_chunks = get_or_create_chunks('P0A7B8', bact_seq, 'bacteria')

human_emb = get_or_create_embeddings(human_chunks, 'P04637')
bact_emb = get_or_create_embeddings(bact_chunks, 'P0A7B8')

similarity = compute_similarity_matrix(human_emb, bact_emb)
score, alignment, _ = smith_waterman_chunks(similarity)

human_desc = get_or_create_descriptors(human_chunks, 'P04637')
bact_desc = get_or_create_descriptors(bact_chunks, 'P0A7B8')

interpretation = interpret_alignment(
    'P04637', 'P0A7B8', [(score, alignment)],
    human_chunks, bact_chunks, human_desc, bact_desc
)

print(interpretation)
```
