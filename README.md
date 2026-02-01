# 🧬 Protein Alignment Analysis Tool

**AI-Powered Protein Similarity Detection using ESM-2 Embeddings**

A comprehensive bioinformatics tool that analyzes and compares protein sequences between human and bacterial proteins using state-of-the-art AI embeddings (ESM-2), Smith-Waterman alignment, and biochemical descriptors.

---

## 📋 Table of Contents
- [What Does This Project Do?](#what-does-this-project-do)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Output Interpretation](#output-interpretation)

---

## 🎯 What Does This Project Do?

This tool helps you **discover and analyze similarities between human and bacterial proteins** by:

1. **Fetching protein sequences** from UniProt database
2. **Breaking them into overlapping chunks** (10 amino acids, stride 5)
3. **Computing AI embeddings** using Meta's ESM-2 protein language model (1280 dimensions)
4. **Finding similar regions** using Smith-Waterman alignment algorithm
5. **Analyzing biochemical properties** (hydrophobicity, charge, aromaticity, etc.)
6. **Detecting functional annotations** (Pfam domains, Prosite motifs, signal peptides, TM helices)
7. **Generating AI interpretations** using LLM (Groq API) to explain biological significance

### Real-World Use Cases:
- 🔬 **Drug Discovery**: Find conserved regions that could be drug targets
- 🧪 **Evolutionary Biology**: Identify horizontal gene transfer between species
- 💊 **Antibiotic Resistance**: Detect similar resistance mechanisms
- 🧬 **Functional Annotation**: Predict bacterial protein functions based on human homologs
- 🔍 **Protein Engineering**: Identify conserved structural/functional domains

---

## ✨ Key Features

### 1. **Intelligent Sequence Analysis**
- Automatic protein sequence fetching from UniProt
- Support for various ID formats (P04637, tr|A0A024RA31|A0A024RA31_HUMAN, etc.)

### 2. **AI-Powered Embeddings**
- Uses ESM-2 (650M parameter model) from Meta AI
- Captures deep structural and functional patterns
- 1280-dimensional embeddings per chunk

### 3. **Advanced Alignment**
- Smith-Waterman local alignment
- Detects multiple non-overlapping regions
- Customizable gap penalties and scoring thresholds

### 4. **Comprehensive Biochemical Analysis**
11+ biochemical descriptors per chunk:
- Hydrophobicity (GRAVY)
- Aromaticity
- Charge at pH 7
- Hydrophobic/Polar fractions
- Instability index
- Shannon entropy
- And more...

### 5. **Functional Annotations**
- **Pfam domains** (local PfamScan via WSL or API fallback)
- **Prosite motifs** (pattern detection)
- **Signal peptides** (heuristic prediction)
- **Transmembrane helices** (topology prediction)
- **Domain overlap analysis** between proteins

### 6. **AI-Powered Interpretation**
- Uses Groq's LLaMA models for biological interpretation
- Explains alignment significance
- Suggests evolutionary relationships
- Identifies potential functional implications

### 7. **Web Interface**
- intuitive Flask web application
- Real-time analysis progress

---

## 🔬 How It Works

### The Pipeline:

```
1. INPUT: Protein IDs (Human + Bacterial)
  ↓
2. FETCH: Download sequences from UniProt
  ↓
3. CHUNK: Split into overlapping 10 aa chunks (stride 5)
  ↓
4. EMBED: Generate ESM-2 embeddings (1280D vectors)
  ↓
5. ALIGN: Smith-Waterman finds similar regions
  ↓
6. ANALYZE: Compute biochemical descriptors
  ↓
7. ANNOTATE: Find Pfam/Prosite/Signal/TM features
  ↓
8. INTERPRET: Generate human-readable + AI analysis
  ↓
9. OUTPUT: Web display + detailed reports
```

### Technical Details:

**Chunking Strategy:**
- Chunk length: 10 amino acids
- Stride: 5 amino acids (50% overlap)
- Ensures smooth transitions and captures local structure

**Similarity Detection:**
- ESM-2 embeddings capture semantic protein meaning
- Cosine similarity between chunk embeddings
- Smith-Waterman finds optimal local alignments

**Alignment Scoring:**
- Match score: cosine similarity - 0.5 threshold
- Gap open penalty: -0.2
- Gap extend penalty: -0.1

---

## 📁 Project Structure

```
protein-alignment-tool/
│
├── 📄 Core Application Files
│   ├── app.py                    # Flask web application (main entry point)
│   ├── config.py                 # Configuration settings
│   ├── run.bat                   # Windows launch script
│   └── requirements.txt          # Python dependencies
│
├── 🧩 Core Analysis Modules
│   ├── protein_utils.py          # Protein fetching & ID sanitization
│   ├── chunking.py               # Sequence chunking logic
│   ├── embeddings.py             # ESM-2 embedding computation
│   ├── models.py                 # ESM-2 model loading
│   ├── alignment.py              # Smith-Waterman alignment
│   ├── descriptors.py            # Biochemical descriptor computation
│   ├── functional_annotations.py # Pfam/Prosite/Signal/TM detection
│   ├── interpretation.py         # Result interpretation
│   └── llm_interpretation.py     # AI-powered analysis (Groq)
│
├── 🌐 Web Interface
│   └── templates/
│       └── index.html            # web UI
│
├── 💾 Data & Cache
│   ├── cache/                    # Cached sequences, embeddings, descriptors
│   │   ├── *.fasta              # Protein sequences
│   │   ├── *_embeddings.npy     # ESM-2 embeddings
│   │   ├── *_descriptors.parquet # Biochemical descriptors
│   │   └── functional/          # Functional annotations cache
│   └── data/                     # Master chunk parquet files (optional)
│
├── 📚 Documentation
│   └── docs/
│       ├── README.md             # This file
│       ├── QUICK_START.md        # Getting started guide
│       ├── USAGE_GUIDE.md        # Detailed API documentation
│       ├── PFAM_SETUP.md         # Pfam domain analysis setup
│       ├── LLM_SETUP.md          # AI interpretation setup
│       └── *.md                  # Other documentation
│
├── 🧪 Tests
│   └── tests/
│       ├── test_modules.py       # Module integration tests
│       ├── test_protein_fetch.py # Protein fetching tests
│       ├── test_data_files.py    # Data file validation
│       └── test_pfam.py          # Pfam domain tests
│
└── 📓 Notebooks
   └── notebooks/
      ├── *.ipynb               # Original research notebooks
      └── notebook_descriptors.txt
```

---

## 🚀 Quick Start

### Prerequisites:
- Python 3.8+
- 4GB+ RAM (8GB+ recommended for GPU)
- Internet connection (for UniProt API)

### Installation:

```bash
# 1. Clone or navigate to project
cd path/to/protein-alignment-tool

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Set up Groq API key for AI interpretation
# Get a free key at: https://console.groq.com/keys
# Option A (recommended): copy .env.example to .env and set GROQ_API_KEY
# Option B: set OS env var (PowerShell) $Env:GROQ_API_KEY="your_key"

# 4. (Optional) Set up Pfam for domain analysis
# See docs/PFAM_SETUP.md for WSL installation
```

### Run the Application:

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

---

## 🧩 Setup Notes (to ensure it runs)

- Recommended: use a virtual environment

  Windows (PowerShell):
  ```powershell
  python -m venv .venv
  . .venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

  Linux/macOS:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- If PyTorch install fails on your platform:
  - CPU-only:
    ```bash
    pip install torch --index-url https://download.pytorch.org/whl/cpu
    ```
  - CUDA 12.1 (GPU):
    ```bash
    pip install torch --index-url https://download.pytorch.org/whl/cu121
    ```
  - See official options: https://pytorch.org/get-started/locally/

- Pfam domains are optional. If local PfamScan/WSL isn’t set up, the app automatically uses the InterPro API fallback.


## 🤖 LLM Interpretation

- Get a free key: https://console.groq.com/keys
- Easiest setup:
  - Copy `.env.example` → `.env`
  - Edit `.env` and set `GROQ_API_KEY=your_key_here` (no quotes)
- Or run the helper:
  ```bash
  python setup_llm.py
  ```
  This writes your key into `.env` (which is git-ignored).
- Dependencies: `groq` is included in `requirements.txt`.
- Run the app. If the key is detected, an AI interpretation section appears in results.

## 💡 Usage

### Web Interface:

1. Enter protein IDs:
  - Human: exemple  `P04637` or `tr|A0A024RA31|A0A024RA31_HUMAN`
  - Bacteria: exemple `P0A7B8` or `A0A0C7KF14`

2. Click "Analyze Proteins"

3. Wait for analysis (first run downloads ESM-2 model ~2.5GB)

4. View results:
  - Alignment summary
  - Significant regions with positions
  - Biochemical property comparisons
  - Functional annotations
  - AI interpretation

### Python API:

```python
from protein_utils import fetch_protein_sequence
from chunking import get_or_create_chunks
from embeddings import get_or_create_embeddings, compute_similarity_matrix
from alignment import smith_waterman_chunks
from descriptors import get_or_create_descriptors

# Fetch sequences
human_seq = fetch_protein_sequence("P04637")
bact_seq = fetch_protein_sequence("P0A7B8")

# Create chunks
human_chunks = get_or_create_chunks("P04637", human_seq, "human")
bact_chunks = get_or_create_chunks("P0A7B8", bact_seq, "bacteria")

# Compute embeddings
human_emb = get_or_create_embeddings(human_chunks, "P04637")
bact_emb = get_or_create_embeddings(bact_chunks, "P0A7B8")

# Compute similarity matrix
similarity_matrix = compute_similarity_matrix(human_emb, bact_emb)

# Align
score, alignment, _ = smith_waterman_chunks(similarity_matrix)

# Get descriptors
human_desc = get_or_create_descriptors(human_chunks, "P04637")
bact_desc = get_or_create_descriptors(bact_chunks, "P0A7B8")
```

---

## 🛠️ Technologies Used

### AI/ML:
- **ESM-2** (Meta AI) - Protein language model (650M parameters)
- **PyTorch** - Deep learning framework
- **Transformers** (Hugging Face) - Model loading & inference
- **Groq** - Fast LLM inference for interpretations

### Bioinformatics:
- **Biopython** - Sequence handling & analysis
- **Smith-Waterman** - Local alignment algorithm
- **UniProt API** - Protein database access
- **Pfam/Prosite** - Domain/motif detection

### Data Processing:
- **NumPy** - Numerical computations
- **Pandas** - Data manipulation
- **Parquet** - Efficient data storage

### Web:
- **Flask** - Web framework
- **HTML/CSS/JavaScript** - Beautiful UI

---

## 📊 Output Interpretation

### Alignment Scores:
- **Score ≥ 15**: 🟢 Very strong similarity (high confidence)
- **Score 10-15**: 🟡 Moderate similarity (potential relationship)
- **Score 5-10**: 🟠 Weak similarity (consider with caution)
- **Score < 5**: 🔴 Very weak (likely unrelated)

### Biochemical Indicators:
- **⬆️**: Significantly higher in human protein (>10% difference)
- **⬇️**: Significantly lower in human protein (>10% difference)
- **≈**: Similar between proteins (<10% difference)

### What "Significant Region" Means:
A continuous stretch of protein sequence where both proteins show strong structural/functional similarity based on ESM-2 embeddings. These regions may indicate:
- ✓ Conserved functional domains
- ✓ Similar 3D structure
- ✓ Shared evolutionary origin
- ✓ Potential horizontal gene transfer

---

## 🆘 Support

Check documentation in `docs/` folder:
- `QUICK_START.md` - Getting started
- `USAGE_GUIDE.md` - Detailed API
- `PFAM_SETUP.md` - Domain analysis
- `LLM_SETUP.md` - AI interpretation

---



