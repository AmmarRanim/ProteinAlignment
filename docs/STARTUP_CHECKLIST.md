# Startup Checklist ✓

## Before You Start

- [ ] Python 3.8+ installed
- [ ] pip installed
- [ ] Internet connection (for first run)
- [ ] 4GB+ RAM available
- [ ] 5GB+ disk space (for model and cache)

## Installation Steps

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed flask-3.0.0 biopython-1.83 pandas-2.1.4 ...
```

### 2. Run Tests (Optional but Recommended)
```bash
python test_modules.py
```

**Expected output:**
```
✓ All tests passed! Ready to run the application.
```

### 3. Test Protein Fetching (Optional)
```bash
python test_protein_fetch.py
```

**Expected output:**
```
✓ Success! Sequence length: XXX aa
```

## Running the Application

### Start the Server

**Windows:**
```bash
python app.py
```
Or double-click `run.bat`

**Linux/Mac:**
```bash
python3 app.py
```

### Expected Console Output

```
======================================================================
Starting Protein Alignment Analysis Server
======================================================================
Host: 0.0.0.0
Port: 5000
Debug: True
======================================================================

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
```

### Open Browser

Navigate to: **http://localhost:5000**

You should see a purple gradient page with "🧬 Protein Alignment Analysis"

## First Analysis

### Enter Protein IDs

**Try these examples:**

**Example 1: Simple IDs**
- Human: `P04637`
- Bacteria: `P0A7B8`

**Example 2: Your Notebook IDs**
- Human: `A0A024RA31`
- Bacteria: `A0A0C7KF14`

**Example 3: Full Format**
- Human: `tr|A0A024RA31|A0A024RA31_HUMAN`
- Bacteria: `tr|A0A0C7KF14|A0A0C7KF14_KLEPN`

### Click "Analyze Proteins"

**First run will:**
1. Download ESM-2 model (~2.5GB) - **ONE TIME ONLY**
2. Fetch sequences from UniProt
3. Create chunks
4. Compute embeddings
5. Run alignment
6. Compute descriptors
7. Generate interpretation

**Time: 2-5 minutes**

### Console Output During Analysis

```
======================================================================
Starting analysis: A0A024RA31 vs A0A0C7KF14
======================================================================

Step 1: Fetching protein sequences...
Extracted ID: A0A024RA31 from tr|A0A024RA31|A0A024RA31_HUMAN
Fetching A0A024RA31 from UniProt...
  Human: 393 aa
  Bacteria: 456 aa

Step 2: Chunking sequences...
Creating chunks for A0A024RA31...
Saved 77 chunks to cache
  Human chunks: 77
  Bacteria chunks: 90

Step 3: Computing embeddings...
Loading ESM-2 model...
Model loaded on GPU
Computing embeddings for A0A024RA31 (77 chunks)...
  Embeddings computed

Step 4: Computing similarity matrix...
  Similarity matrix shape: (77, 90)

Step 5: Running Smith-Waterman alignment...
  Alignment score: 12.45
  Aligned chunks: 15

Step 6: Computing biochemical descriptors...
Computing descriptors for A0A024RA31 (77 chunks)...
  Descriptors computed

Step 7: Generating interpretation...
  Interpretation generated

======================================================================
Analysis complete!
======================================================================
```

### View Results

Browser will show:
- ✓ Protein IDs
- ✓ Sequence lengths
- ✓ Number of chunks
- ✓ Alignment score
- ✓ Aligned regions
- ✓ Biochemical properties
- ✓ Detailed interpretation

## Subsequent Analyses

**Same proteins:** ~10-30 seconds (uses cache)
**Different proteins:** ~1-3 minutes (computes new embeddings)

## Troubleshooting

### ❌ "pyhton: command not found"
**Fix:** Typo! Use `python` not `pyhton`

### ❌ "Module not found"
**Fix:** 
```bash
pip install -r requirements.txt
```

### ❌ "HTTP Error 400"
**Fix:** Already fixed! App now handles all ID formats.

### ❌ "Port 5000 already in use"
**Fix:** Edit `config.py`:
```python
FLASK_PORT = 5001
```

### ❌ "Out of memory"
**Fix:** Edit `config.py`:
```python
CHUNK_LEN = 5  # Smaller chunks
```

### ❌ "CUDA out of memory"
**Fix:** App will automatically use CPU if GPU fails

## Success Indicators

✅ Server starts without errors
✅ Browser shows the interface
✅ Can enter protein IDs
✅ Analysis completes successfully
✅ Results are displayed
✅ Cache directory is created
✅ Subsequent analyses are faster

## File Structure Check

After first run, you should have:

```
.
├── app.py                 ✓ Main application
├── config.py             ✓ Configuration
├── models.py             ✓ ESM-2 model
├── protein_utils.py      ✓ Utilities
├── chunking.py           ✓ Chunking
├── embeddings.py         ✓ Embeddings
├── alignment.py          ✓ Alignment
├── descriptors.py        ✓ Descriptors
├── interpretation.py     ✓ Interpretation
├── requirements.txt      ✓ Dependencies
├── templates/
│   └── index.html       ✓ Web interface
└── cache/               ✓ Auto-created
    ├── *.fasta          ✓ Sequences
    ├── *_chunks.parquet ✓ Chunks
    ├── *_embeddings.npy ✓ Embeddings
    └── *_descriptors.parquet ✓ Descriptors
```

## Ready to Go!

If all checks pass:
1. ✅ Requirements installed
2. ✅ Tests passed
3. ✅ Server running
4. ✅ Browser shows interface
5. ✅ First analysis completed

**You're all set! 🎉**

## Next Steps

- Try different protein pairs
- Explore the interpretation results
- Check the cache directory
- Read USAGE_GUIDE.md for advanced features
- Customize config.py for your needs
