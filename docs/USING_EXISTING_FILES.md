# Using Your Existing Parquet Files

## Quick Setup

### Step 1: Place Your Files

Put your two parquet files in the **root directory** (same folder as `app.py`):

```
your-project/
├── app.py
├── Homo_sapiens_chunks.parquet          ← Your human file here
├── Klebsiella_pneumoniae_chunks.parquet ← Your bacteria file here
├── config.py
├── chunking.py
└── ...
```

### Step 2: That's It!

The app will automatically:
1. ✅ Check if protein ID exists in your files
2. ✅ Load chunks if found
3. ✅ Create new chunks if not found
4. ✅ Append new chunks to your files

## How It Works

### When You Analyze a Protein:

**Scenario 1: Protein EXISTS in your file**
```
User enters: A0A024RA31
    ↓
App checks: Homo_sapiens_chunks.parquet
    ↓
Found! ✓ Loading 77 chunks from master file
    ↓
Uses existing chunks (instant!)
```

**Scenario 2: Protein NOT in your file**
```
User enters: P04637
    ↓
App checks: Homo_sapiens_chunks.parquet
    ↓
Not found ✗ Creating new chunks...
    ↓
Creates 85 chunks
    ↓
Appends to Homo_sapiens_chunks.parquet
    ↓
Your file now has both proteins!
```

## File Structure

Your parquet files should have these columns:
- `protein_id` - Protein identifier
- `chunk_index` - Chunk number (0, 1, 2, ...)
- `start` - Start position in sequence
- `end` - End position in sequence
- `chunk_seq` - Chunk sequence
- `organism` - Organism name (optional)

## Different File Location?

If your files are in a different folder, edit `config.py`:

```python
# If files are in a 'data' folder:
MASTER_CHUNKS_DIR = "data"

# If files are in your Google Drive:
MASTER_CHUNKS_DIR = "/content/drive/MyDrive/uniprotkb/pfam_output_esmpipeline/chunks"
```

## Different File Names?

Edit `config.py`:

```python
HUMAN_CHUNKS_FILE = "your_human_file.parquet"
BACTERIA_CHUNKS_FILE = "your_bacteria_file.parquet"
```

## Example Console Output

```
======================================================================
Starting analysis: A0A024RA31 vs A0A0C7KF14
======================================================================

Step 1: Fetching protein sequences...
  Human: 393 aa
  Bacteria: 456 aa

Step 2: Chunking sequences...
Checking master file: Homo_sapiens_chunks.parquet
✓ Found 77 chunks for A0A024RA31 in master file
  Human chunks: 77

Checking master file: Klebsiella_pneumoniae_chunks.parquet
✗ Protein A0A0C7KF14 not found in master file
Creating new chunks for A0A0C7KF14...
Appending 90 chunks to master file...
✓ Saved to master file (total proteins: 32076)
  Bacteria chunks: 90
```

## Benefits

1. **Reuse Existing Work** - No need to rechunk proteins you already have
2. **Automatic Growth** - New proteins automatically added to your files
3. **Single Source of Truth** - All chunks in one file per organism
4. **Fast Lookups** - Instant loading for existing proteins
5. **Backward Compatible** - Works with your notebook's files

## File Growth

Your files will grow as you analyze new proteins:

```
Initial:     Homo_sapiens_chunks.parquet (38,818 proteins)
After run 1: Homo_sapiens_chunks.parquet (38,819 proteins) +1
After run 2: Homo_sapiens_chunks.parquet (38,820 proteins) +1
...
```

## Checking Your Files

To see what proteins are in your files:

```python
import pandas as pd

# Load file
df = pd.read_parquet('Homo_sapiens_chunks.parquet')

# See all proteins
print(df['protein_id'].unique())

# Count proteins
print(f"Total proteins: {df['protein_id'].nunique()}")

# Check specific protein
protein_id = 'A0A024RA31'
if protein_id in df['protein_id'].values:
    chunks = df[df['protein_id'] == protein_id]
    print(f"Found {len(chunks)} chunks for {protein_id}")
```

## Troubleshooting

### "Could not read master file"
**Fix:** Check file path and name in `config.py`

### "Protein not found" (but you know it's there)
**Fix:** Check the `protein_id` column format in your file

### Files not being used
**Fix:** Make sure files are in the location specified in `config.py`

### Want to start fresh?
**Fix:** Rename your old files and let the app create new ones

## Summary

1. ✅ Put your 2 parquet files in the root directory
2. ✅ Run `python app.py`
3. ✅ App automatically uses existing chunks
4. ✅ App automatically adds new proteins
5. ✅ Your files grow over time

**No manual work needed - it just works!** 🎉
