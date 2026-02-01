"""
Test script to verify all modules are working correctly
"""

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        import config
        print("✓ config.py")
        
        import models
        print("✓ models.py")
        
        import protein_utils
        print("✓ protein_utils.py")
        
        import chunking
        print("✓ chunking.py")
        
        import embeddings
        print("✓ embeddings.py")
        
        import alignment
        print("✓ alignment.py")
        
        import descriptors
        print("✓ descriptors.py")
        
        import interpretation
        print("✓ interpretation.py")
        
        print("\n✓ All modules imported successfully!")
        return True
    except Exception as e:
        print(f"\n✗ Import failed: {e}")
        return False


def test_config():
    """Test configuration values"""
    print("\nTesting configuration...")
    try:
        from config import CHUNK_LEN, CHUNK_STRIDE, GAP_OPEN, GAP_EXTEND, CACHE_DIR
        print(f"  CHUNK_LEN: {CHUNK_LEN}")
        print(f"  CHUNK_STRIDE: {CHUNK_STRIDE}")
        print(f"  GAP_OPEN: {GAP_OPEN}")
        print(f"  GAP_EXTEND: {GAP_EXTEND}")
        print(f"  CACHE_DIR: {CACHE_DIR}")
        print("✓ Configuration loaded")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_chunking():
    """Test chunking functionality"""
    print("\nTesting chunking...")
    try:
        from chunking import chunk_protein
        
        test_seq = "ACDEFGHIKLMNPQRSTVWY" * 5  # 100 aa sequence
        chunks = chunk_protein("TEST_PROTEIN", test_seq)
        
        print(f"  Test sequence length: {len(test_seq)}")
        print(f"  Number of chunks: {len(chunks)}")
        print(f"  First chunk: {chunks.iloc[0]['chunk_seq']}")
        print("✓ Chunking works")
        return True
    except Exception as e:
        print(f"✗ Chunking test failed: {e}")
        return False


def test_descriptors():
    """Test descriptor computation"""
    print("\nTesting descriptors...")
    try:
        from descriptors import compute_chunk_descriptors
        
        test_seq = "ACDEFGHIKLMNPQRSTVWY"
        desc = compute_chunk_descriptors(test_seq)
        
        print(f"  Test sequence: {test_seq}")
        print(f"  Number of descriptors: {len(desc)}")
        print(f"  GRAVY: {desc.get('gravy', 'N/A')}")
        print(f"  Aromaticity: {desc.get('aromaticity', 'N/A')}")
        print("✓ Descriptors work")
        return True
    except Exception as e:
        print(f"✗ Descriptor test failed: {e}")
        return False


def test_alignment():
    """Test Smith-Waterman alignment"""
    print("\nTesting alignment...")
    try:
        import numpy as np
        from alignment import smith_waterman_chunks
        
        # Create a simple similarity matrix
        S = np.array([
            [0.9, 0.8, 0.3],
            [0.7, 0.9, 0.4],
            [0.3, 0.5, 0.8]
        ])
        
        score, alignment, _ = smith_waterman_chunks(S)
        
        print(f"  Test matrix shape: {S.shape}")
        print(f"  Alignment score: {score:.2f}")
        print(f"  Alignment length: {len(alignment)}")
        print("✓ Alignment works")
        return True
    except Exception as e:
        print(f"✗ Alignment test failed: {e}")
        return False


if __name__ == "__main__":
    print("="*70)
    print("Protein Alignment Analysis - Module Tests")
    print("="*70)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Config", test_config()))
    results.append(("Chunking", test_chunking()))
    results.append(("Descriptors", test_descriptors()))
    results.append(("Alignment", test_alignment()))
    
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:20s} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("="*70)
    if all_passed:
        print("✓ All tests passed! Ready to run the application.")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    print("="*70)
