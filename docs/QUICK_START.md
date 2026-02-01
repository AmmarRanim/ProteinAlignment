# Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- BioPython (protein analysis)
- PyTorch (deep learning)
- ESM-2 (protein embeddings)
- Pandas, NumPy (data processing)

## Step 2: Run the Application

**Option A: Using Python directly**
```bash
python app.py
```

**Option B: Using the batch file (Windows)**
Double-click `run.bat`

You should see:
```
======================================================================
Starting Protein Alignment Analysis Server
======================================================================
Host: 0.0.0.0
Port: 5000
Debug: True
======================================================================

 * Running on http://0.0.0.0:5000
```

## Step 3: Open Your Browser

Navigate to: `http://localhost:5000`

## Step 4: Enter Protein IDs

### Example 1: Simple IDs
- Human: `P04637`
- Bacteria: `P0A7B8`

### Example 2: Full Format IDs (from your notebook)
- Human: `tr|A0A024RA31|A0A024RA31_HUMAN`
- Bacteria: `tr|A0A0C7KF14|A0A0C7KF14_KLEPN`

### Example 3: Just the Accession
- Human: `A0A024RA31`
- Bacteria: `A0A0C7KF14`

**All three formats work!** The app automatically extracts the correct ID.

## Step 5: Click "Analyze Proteins"

First analysis takes 2-5 minutes:
- Downloads ESM-2 model (one-time, ~2.5GB)
- Fetches sequences from UniProt
- Computes embeddings
- Runs alignment
- Computes descriptors

Subsequent analyses with same proteins: ~10-30 seconds (uses cache)

## Step 6: View Results

You'll see:
- Protein lengths
- Number of chunks
- Alignment score
- Aligned regions
- Biochemical properties comparison

## Common Issues

### Issue: "pyhton: command not found"
**Fix**: Typo! Use `python` not `pyhton`
```bash
python app.py
```

### Issue: "HTTP Error 400: Bad Request"
**Fix**: Updated! The app now handles all ID formats automatically.

### Issue: "Module not found"
**Fix**: Install requirements
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Fix**: Change port in `config.py`
```python
FLASK_PORT = 5001  # or any other port
```

## Testing

Before running the app, test that everything works:
```bash
python test_modules.py
```

You should see:
```
✓ All tests passed! Ready to run the application.
```

## File Locations

- **Application**: `app.py`
- **Configuration**: `config.py`
- **Web Interface**: `templates/index.html`
- **Cache**: `cache/` (auto-created)
- **Requirements**: `requirements.txt`

## Next Steps

1. ✅ Tests passed
2. ✅ Run `python app.py`
3. ✅ Open `http://localhost:5000`
4. ✅ Enter protein IDs
5. ✅ Click Analyze
6. ✅ View results!

## Need Help?

- Read `USAGE_GUIDE.md` for detailed documentation
- Read `PROJECT_SUMMARY.md` for architecture overview
- Check `README.md` for quick reference
