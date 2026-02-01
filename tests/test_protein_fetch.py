"""Test protein fetching with different ID formats"""

from protein_utils import fetch_protein_sequence

def test_fetch():
    """Test fetching with different ID formats"""
    
    test_ids = [
        "P04637",  # Simple format
        "A0A024RA31",  # Accession only
        "tr|A0A024RA31|A0A024RA31_HUMAN",  # Full format
    ]
    
    print("Testing protein fetching with different ID formats...\n")
    
    for protein_id in test_ids:
        print(f"Testing: {protein_id}")
        try:
            seq = fetch_protein_sequence(protein_id)
            print(f"  ✓ Success! Sequence length: {len(seq)} aa")
            print(f"  First 50 aa: {seq[:50]}...")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
        print()

if __name__ == "__main__":
    test_fetch()
