# 🧬 Protein Alignment Analysis Tool

**Web-based protein alignment analysis using ESM-2 embeddings, Smith-Waterman algorithm, and LLM interpretation**

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
## 📁 Data Files

**Data and cache folders are not included in the repository by default.**

- The `data/` and `cache/` folders are used to store generated files, outputs, and downloaded protein sequences (such as `.fasta` files).
- These folders are created automatically by the application as needed.
- **You do not need to manually add these folders or files unless you want to use your own data.**
- If you want to use your own `.fasta` or data files, place them in the appropriate folder (`data/` or `cache/`) and ensure the file names match the expected format.
---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Internet connection (for UniProt API)

### 1. (Recommended) Create a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Upgrade pip (recommended)
```bash
python -m pip install --upgrade pip
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Groq API Key for AI Interpretation
- Get a free key at: https://console.groq.com/keys
- Option A (recommended): Copy `.env.example` to `.env` and set `GROQ_API_KEY` in `.env`.
- Option B: Set OS environment variable (PowerShell):
  ```powershell
  $Env:GROQ_API_KEY="your_key"
  ```
- Or run the helper:
  ```bash
  python setup_llm.py
  ```

### 5. (Optional) Set Up Pfam for Domain Analysis
- See `docs/PFAM_SETUP.md` for WSL installation and setup instructions.

### 6. Run the Application

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

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

## 🆘 Support

Check documentation in `docs/` folder:
- `QUICK_START.md` - Getting started
- `USAGE_GUIDE.md` - Detailed API
- `PFAM_SETUP.md` - Domain analysis
- `LLM_SETUP.md` - AI interpretation

---



