"""Functional annotations: Pfam domains, Prosite motifs, Signal peptide, TM helices"""
import requests
import re
import os
from config import CACHE_DIR
from protein_utils import sanitize_protein_id

# Cache for functional annotations
FUNC_CACHE_DIR = os.path.join(CACHE_DIR, "functional")
os.makedirs(FUNC_CACHE_DIR, exist_ok=True)


# =============================================================================
# 1. PFAM DOMAINS - Local PfamScan via WSL (matching notebook)
# =============================================================================

# Import Pfam settings from config
try:
    from config import PFAM_DIR, PFAM_SCAN_PATH
except ImportError:
    PFAM_DIR = "~/pfam"
    PFAM_SCAN_PATH = "~/pfam/PfamScan/pfam_scan.pl"

PFAM_TEMP_DIR = os.path.join(CACHE_DIR, "pfam_temp")
os.makedirs(PFAM_TEMP_DIR, exist_ok=True)


def parse_pfam_output(output_file):
    """
    Parse PfamScan output file and extract domain accessions.
    Returns list of Pfam domain accessions (e.g., ['PF00001', 'PF00002']).
    """
    domains = []
    try:
        with open(output_file, 'r') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                parts = line.strip().split()
                if len(parts) >= 6:
                    # Column 6 contains Pfam accession (PF#####)
                    pfam_acc = parts[5]
                    if pfam_acc.startswith('PF') and pfam_acc not in domains:
                        domains.append(pfam_acc)
    except Exception as e:
        print(f"    Error parsing Pfam output: {e}")
    
    return domains


def search_pfam_domains_local(sequence, protein_id="unknown"):
    """
    Search Pfam domains using LOCAL PfamScan via WSL.
    Returns list of Pfam domain accessions.
    ~2-5 seconds per sequence
    """
    import subprocess
    
    clean_id = sanitize_protein_id(protein_id)
    fasta_file = os.path.join(PFAM_TEMP_DIR, f"{clean_id}.fasta")
    output_file = os.path.join(PFAM_TEMP_DIR, f"{clean_id}_pfam.out")
    
    try:
        # Write sequence to FASTA file
        with open(fasta_file, 'w') as f:
            f.write(f">{clean_id}\n{sequence}\n")
        
        # Convert Windows path to WSL path
        wsl_fasta = subprocess.run(
            ['wsl', 'wslpath', '-u', fasta_file],
            capture_output=True, text=True
        ).stdout.strip()
        
        wsl_output = subprocess.run(
            ['wsl', 'wslpath', '-u', output_file],
            capture_output=True, text=True
        ).stdout.strip()
        
        # Run PfamScan via WSL (with -I flag for Perl modules)
        cmd = f"perl -I {PFAM_DIR}/PfamScan {PFAM_SCAN_PATH} -fasta {wsl_fasta} -dir {PFAM_DIR} -outfile {wsl_output} -cpu 2"
        
        result = subprocess.run(
            ['wsl', 'bash', '-c', cmd],
            capture_output=True, text=True, timeout=120  # Increased timeout
        )
        
        if result.returncode == 0 and os.path.exists(output_file):
            domains = parse_pfam_output(output_file)
            return domains
        else:
            print(f"    PfamScan error: {result.stderr}")
            return []
            
    except subprocess.TimeoutExpired:
        print(f"    PfamScan timeout for {protein_id}")
        return []
    except Exception as e:
        print(f"    PfamScan error: {e}")
        # Fallback to API
        return search_pfam_domains_api(protein_id)


def search_pfam_domains_api(protein_id):
    """
    Search Pfam domains using InterPro API (fallback).
    Returns list of Pfam domain accessions.
    """
    # Clean protein ID
    clean_id = sanitize_protein_id(protein_id)
    
    try:
        url = f"https://www.ebi.ac.uk/interpro/api/entry/pfam/protein/uniprot/{clean_id}"
        response = requests.get(url, timeout=30, headers={'Accept': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            domains = []
            
            if 'results' in data:
                for result in data['results']:
                    acc = result.get('metadata', {}).get('accession', '')
                    if acc and acc.startswith('PF') and acc not in domains:
                        domains.append(acc)
            
            return domains
        else:
            return []
            
    except Exception as e:
        print(f"    Pfam API error: {e}")
        return []


def search_pfam_domains(sequence, protein_id="unknown"):
    """
    Search Pfam domains using LOCAL PfamScan only (no API fallback).
    """
    return search_pfam_domains_local(sequence, protein_id)


# =============================================================================
# 2. PROSITE MOTIFS - ScanProsite API (same as notebook)
# =============================================================================

def search_prosite_motifs(sequence):
    """
    Search Prosite motifs using ScanProsite API.
    Returns list of Prosite pattern accessions.
    ~0.05 seconds per sequence
    """
    url = "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi"
    
    params = {
        'seq': sequence,
        'output': 'json',
        'skip': 'false'
    }
    
    try:
        response = requests.post(url, data=params, timeout=30)
        
        if response.status_code == 200:
            try:
                results = response.json()
                motifs = []
                
                if 'matchset' in results:
                    for match in results['matchset']:
                        acc = match.get('signature_ac', '')
                        if acc and acc not in motifs:
                            motifs.append(acc)
                
                return motifs
            except:
                # Fallback: parse text response
                motifs = []
                text = response.text
                pattern = re.findall(r'PS\d{5}', text)
                for p in pattern:
                    if p not in motifs:
                        motifs.append(p)
                return motifs
        else:
            return []
            
    except Exception as e:
        print(f"    Prosite error: {e}")
        return []


# =============================================================================
# 3. SIGNAL PEPTIDE - Heuristic (same as notebook)
# =============================================================================

def predict_signal_peptide(sequence):
    """
    Predict signal peptide using heuristic rules based on SignalP characteristics:
    - Positive N-region (first 1-5 aa with K, R)
    - Hydrophobic H-region (aa 5-20 with high hydrophobic content)
    - Polar C-region with cleavage site
    
    Returns True if signal peptide detected, False otherwise.
    """
    if len(sequence) < 20:
        return False
    
    n_term = sequence[:30].upper()
    
    # N-region: first 5 aa should have positive charge (K, R)
    n_region = n_term[:5]
    positive = sum(1 for aa in n_region if aa in 'KR')
    
    # H-region: aa 5-20 should be hydrophobic
    h_region = n_term[5:20]
    hydrophobic = set('AVLIMFWP')
    hydro_count = sum(1 for aa in h_region if aa in hydrophobic)
    hydro_fraction = hydro_count / len(h_region) if h_region else 0
    
    # C-region: should have small aa before cleavage (A, G, S)
    c_region = n_term[15:25]
    small_aa = sum(1 for aa in c_region if aa in 'AGS')
    
    # Decision: signal peptide if all criteria met
    has_signal = (positive >= 1 and hydro_fraction >= 0.5 and small_aa >= 2)
    
    return has_signal


# =============================================================================
# 4. TRANSMEMBRANE HELICES - Heuristic (same as notebook)
# =============================================================================

def predict_tm_helices(sequence):
    """
    Predict transmembrane helices using hydrophobicity-based heuristic.
    
    TM helices are typically:
    - 17-25 aa long
    - Highly hydrophobic (GRAVY > 1.5)
    - Contain mostly AVLIMFWP residues
    
    Returns number of predicted TM helices.
    """
    if len(sequence) < 20:
        return 0
    
    sequence = sequence.upper()
    hydrophobic = set('AVLIMFWP')
    
    # Kyte-Doolittle hydrophobicity scale
    kd_scale = {
        'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
        'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
        'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
        'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
    }
    
    tm_count = 0
    window_size = 19  # Typical TM helix length
    
    i = 0
    while i < len(sequence) - window_size:
        window = sequence[i:i + window_size]
        
        # Calculate hydrophobicity
        hydro_sum = sum(kd_scale.get(aa, 0) for aa in window)
        avg_hydro = hydro_sum / window_size
        
        # Calculate hydrophobic fraction
        hydro_count = sum(1 for aa in window if aa in hydrophobic)
        hydro_frac = hydro_count / window_size
        
        # TM helix criteria
        if avg_hydro > 1.5 and hydro_frac > 0.6:
            tm_count += 1
            i += window_size  # Skip past this helix
        else:
            i += 1
    
    return tm_count


# =============================================================================
# MAIN FUNCTION - Compute all functional annotations
# =============================================================================

def compute_functional_annotations(sequence, protein_id="unknown", use_cache=True):
    """
    Compute functional annotations using dedicated tools:
    1. Pfam domains (InterPro API)
    2. Prosite motifs (ScanProsite API)
    3. Signal peptide (heuristic)
    4. TM helices (heuristic)
    
    Args:
        sequence (str): Protein sequence
        protein_id (str): Protein identifier
        use_cache (bool): Whether to use cached results
        
    Returns:
        dict: Dictionary with all functional annotations
    """
    # Clean protein ID for caching
    clean_id = sanitize_protein_id(protein_id)
    cache_file = os.path.join(FUNC_CACHE_DIR, f"{clean_id}_functional.json")
    
    # Check cache
    if use_cache and os.path.exists(cache_file):
        try:
            import json
            with open(cache_file, 'r') as f:
                print(f"    Loading functional annotations from cache for {clean_id}")
                return json.load(f)
        except:
            pass
    
    print(f"    Computing functional annotations for {clean_id}...")
    
    annotations = {
        'pfam_domains': [],
        'prosite_motifs': [],
        'has_signal_peptide': False,
        'tm_helix_count': 0
    }
    
    try:
        # 1. Pfam domains (local via WSL or API fallback)
        print(f"      - Searching Pfam domains...")
        annotations['pfam_domains'] = search_pfam_domains(sequence, protein_id)
        
        # 2. Prosite motifs (API)
        print(f"      - Searching Prosite motifs...")
        annotations['prosite_motifs'] = search_prosite_motifs(sequence)
        
        # 3. Signal peptide (heuristic)
        print(f"      - Predicting signal peptide...")
        annotations['has_signal_peptide'] = predict_signal_peptide(sequence)
        
        # 4. TM helices (heuristic)
        print(f"      - Predicting TM helices...")
        annotations['tm_helix_count'] = predict_tm_helices(sequence)
        
        # Save to cache
        if use_cache:
            try:
                import json
                with open(cache_file, 'w') as f:
                    json.dump(annotations, f)
            except:
                pass
        
        print(f"      ✓ Found: {len(annotations['pfam_domains'])} Pfam, "
              f"{len(annotations['prosite_motifs'])} Prosite, "
              f"SP={annotations['has_signal_peptide']}, "
              f"TM={annotations['tm_helix_count']}")
        
    except Exception as e:
        print(f"    Error computing functional annotations: {e}")
    
    return annotations


def check_domain_overlap(human_domains, bact_domains):
    """
    Check if there's overlap between human and bacterial Pfam domains.
    
    Args:
        human_domains (list): List of human Pfam domain accessions
        bact_domains (list): List of bacterial Pfam domain accessions
        
    Returns:
        dict: Overlap information
    """
    human_set = set(human_domains) if human_domains else set()
    bact_set = set(bact_domains) if bact_domains else set()
    
    shared = human_set & bact_set
    
    return {
        'human_domains': list(human_set),
        'bacteria_domains': list(bact_set),
        'shared_domains': list(shared),
        'has_overlap': len(shared) > 0,
        'overlap_count': len(shared)
    }
