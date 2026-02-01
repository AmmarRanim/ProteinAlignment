"""Utilities for protein sequence handling and fetching"""
import os
from Bio import SeqIO
from urllib import request as url_request
from config import CACHE_DIR


def sanitize_protein_id(protein_id):
    """
    Sanitize protein ID for use in filenames
    Extracts the actual ID from formats like "tr|A0A024RA31|A0A024RA31_HUMAN"
    and removes any characters invalid for Windows filenames
    
    Args:
        protein_id (str): UniProt protein ID (may include tr| or sp| prefix)
        
    Returns:
        str: Sanitized protein ID safe for filenames
    """
    clean_id = protein_id
    if '|' in protein_id:
        parts = protein_id.split('|')
        if len(parts) >= 2:
            clean_id = parts[1]  # Extract the middle part (actual ID)
    
    # Remove any remaining invalid Windows filename characters
    # Invalid chars: < > : " / \ | ? *
    for char in '<>:"/\\|?*':
        clean_id = clean_id.replace(char, '_')
    
    return clean_id


def fetch_protein_sequence(protein_id):
    """
    Fetch protein sequence from UniProt or local cache
    
    Args:
        protein_id (str): UniProt protein ID (can include tr| or sp| prefix)
        
    Returns:
        str: Protein sequence
        
    Raises:
        ValueError: If protein cannot be fetched
    """
    # Clean the protein ID - extract actual ID from formats like "tr|A0A024RA31|A0A024RA31_HUMAN"
    clean_id = sanitize_protein_id(protein_id)
    if clean_id != protein_id:
        print(f"Sanitized ID: {clean_id} from {protein_id}")
    
    # Try local cache first
    cache_file = os.path.join(CACHE_DIR, f"{clean_id}.fasta")
    
    if os.path.exists(cache_file):
        print(f"Loading {clean_id} from cache...")
        for record in SeqIO.parse(cache_file, "fasta"):
            return str(record.seq)
    
    # Fetch from UniProt
    print(f"Fetching {clean_id} from UniProt...")
    try:
        url = f"https://rest.uniprot.org/uniprotkb/{clean_id}.fasta"
        with url_request.urlopen(url) as response:
            fasta_data = response.read().decode('utf-8')
            
        # Save to cache
        with open(cache_file, 'w') as f:
            f.write(fasta_data)
        
        # Parse and return sequence
        for record in SeqIO.parse(cache_file, "fasta"):
            return str(record.seq)
            
    except Exception as e:
        raise ValueError(f"Could not fetch protein {clean_id}: {str(e)}")


def clean_sequence(sequence):
    """
    Clean protein sequence by removing invalid characters
    
    Args:
        sequence (str): Raw protein sequence
        
    Returns:
        str: Cleaned sequence
    """
    import re
    sequence = sequence.upper()
    # Replace ambiguous residues with X
    sequence = re.sub(r"[BZUO\*]", "X", sequence)
    # Remove any other weird characters
    sequence = re.sub(r"[^ACDEFGHIKLMNPQRSTVWYX]", "", sequence)
    return sequence
