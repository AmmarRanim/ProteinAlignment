# Local PfamScan Setup Guide (via WSL)

## Overview

This guide helps you set up local PfamScan on Windows using WSL (Windows Subsystem for Linux). This matches the setup from your Colab notebook.

## Prerequisites

- Windows 10/11
- Administrator access
- ~15GB free disk space
- Internet connection

## Step-by-Step Setup

### Step 1: Install WSL

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

**Restart your computer** when prompted.

After restart, Ubuntu will open automatically. Create a username and password when asked.

### Step 2: Install Dependencies

Open **Ubuntu** (from Start menu) or type `wsl` in PowerShell.

Run these commands:

```bash
# Update package list
sudo apt-get update

# Install HMMER, Perl, and tools
sudo apt-get install -y hmmer cpanminus perl git

# Install Perl modules (may take a few minutes)
sudo cpanm Moose JSON List::MoreUtils
```

### Step 3: Create Pfam Directory

```bash
mkdir -p ~/pfam
```

### Step 4: Download Pfam Database

⚠️ **This is a large download (~10GB) and takes 30-60 minutes!**

```bash
wget -P ~/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz
```

**Tip:** You can continue with other steps while this downloads.

### Step 5: Decompress Database

After download completes:

```bash
gunzip ~/pfam/Pfam-A.hmm.gz
```

### Step 6: Create HMMER Index

⚠️ **This takes 5-10 minutes!**

```bash
hmmpress ~/pfam/Pfam-A.hmm
```

This creates index files (`.h3m`, `.h3i`, `.h3f`, `.h3p`).

### Step 7: Download PfamScan Scripts

```bash
git clone https://github.com/aziele/pfam_scan.git ~/pfam/PfamScan
chmod +x ~/pfam/PfamScan/pfam_scan.pl
```

### Step 8: Test the Setup

Back in Windows, run:

```bash
python test_pfam.py
```

You should see:

```
WSL                  ✓ PASS
HMMER                ✓ PASS
Pfam Database        ✓ PASS
Pfam Index           ✓ PASS
PfamScan Script      ✓ PASS
PfamScan Run         ✓ PASS
```

## Quick Test in WSL

You can also test directly in WSL:

```bash
# Create test sequence
cat > ~/pfam/test.fasta << 'EOF'
>test_trypsin
MKTFIFLALLGAAVAFPVDDDDKIVGGYTCGANTVPYQVSLNSGYHFCGGSLINSQWVVSAAHCYKSGIQVRLGEDNINVVEGNEQFISASKSIVHPSYNSNTLNNDIMLIKLKSAASLNSRVASISLPTSCASAGTQCLISGWGNTKSSGTSYPDVLKCLKAPILSDSSCKSAYPGQITSNMFCAGYLEGGKDSCQGDSGGPVVCSGKLQGIVSWGSGCAQKNKPGVYTKVCNYVSWIKQTIASN
EOF

# Run PfamScan
perl ~/pfam/PfamScan/pfam_scan.pl -fasta ~/pfam/test.fasta -dir ~/pfam -outfile ~/pfam/test.out

# View results
cat ~/pfam/test.out
```

Expected output shows Trypsin domain (PF00089).

## Configuration

After setup, the app will automatically use local PfamScan.

To switch between local and API:

Edit `config.py`:

```python
# Use local PfamScan via WSL
USE_LOCAL_PFAM = True

# Or use InterPro API (no setup needed)
USE_LOCAL_PFAM = False
```

## Troubleshooting

### "WSL not available"

**Fix:** Install WSL:
```powershell
wsl --install
```

### "HMMER not found"

**Fix:** Install in WSL:
```bash
sudo apt-get install -y hmmer
```

### "Pfam database not found"

**Fix:** Download it:
```bash
wget -P ~/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz
gunzip ~/pfam/Pfam-A.hmm.gz
```

### "Pfam index files not found"

**Fix:** Create index:
```bash
hmmpress ~/pfam/Pfam-A.hmm
```

### "PfamScan script not found"

**Fix:** Clone repository:
```bash
git clone https://github.com/aziele/pfam_scan.git ~/pfam/PfamScan
chmod +x ~/pfam/PfamScan/pfam_scan.pl
```

### "Perl module not found"

**Fix:** Install modules:
```bash
sudo cpanm Moose JSON List::MoreUtils
```

### "PfamScan times out"

**Fix:** The first run may be slow. Try again or increase timeout.

## File Locations

After setup, you should have:

```
~/pfam/
├── Pfam-A.hmm           # Main database (~10GB)
├── Pfam-A.hmm.h3m       # Index file
├── Pfam-A.hmm.h3i       # Index file
├── Pfam-A.hmm.h3f       # Index file
├── Pfam-A.hmm.h3p       # Index file
└── PfamScan/
    └── pfam_scan.pl     # Main script
```

## Performance

- **First scan:** ~5-10 seconds per protein
- **Subsequent scans:** ~2-5 seconds per protein
- **Results are cached** in `cache/functional/`

## Comparison: Local vs API

| Feature | Local PfamScan | InterPro API |
|---------|---------------|--------------|
| Setup | Complex | None |
| Speed | Fast (2-5 sec) | Slower (5-10 sec) |
| Offline | Yes | No |
| Disk space | ~15GB | None |
| Accuracy | Same | Same |

## Summary

1. ✅ Install WSL
2. ✅ Install HMMER and Perl modules
3. ✅ Download Pfam database (~10GB)
4. ✅ Create HMMER index
5. ✅ Clone PfamScan scripts
6. ✅ Run `python test_pfam.py` to verify

**Total setup time:** ~1-2 hours (mostly download time)

Once set up, PfamScan runs locally without internet!
