"""Test if data files are accessible"""
import os
import pandas as pd
from config import MASTER_CHUNKS_DIR, HUMAN_CHUNKS_FILE, BACTERIA_CHUNKS_FILE

def test_data_files():
    """Check if master parquet files exist and are readable"""
    
    print("="*70)
    print("Testing Data Files")
    print("="*70)
    
    # Check directory
    print(f"\nLooking in directory: {MASTER_CHUNKS_DIR}")
    if os.path.exists(MASTER_CHUNKS_DIR):
        print(f"✓ Directory exists")
    else:
        print(f"✗ Directory NOT found")
        return False
    
    # Check human file
    human_path = os.path.join(MASTER_CHUNKS_DIR, HUMAN_CHUNKS_FILE)
    print(f"\nChecking: {human_path}")
    if os.path.exists(human_path):
        print(f"✓ File exists")
        try:
            df = pd.read_parquet(human_path)
            print(f"  - Rows: {len(df):,}")
            print(f"  - Columns: {list(df.columns)}")
            if 'protein_id' in df.columns:
                print(f"  - Unique proteins: {df['protein_id'].nunique():,}")
                print(f"  - Sample proteins: {list(df['protein_id'].unique()[:3])}")
            print(f"✓ File readable")
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            return False
    else:
        print(f"✗ File NOT found")
        return False
    
    # Check bacteria file
    bacteria_path = os.path.join(MASTER_CHUNKS_DIR, BACTERIA_CHUNKS_FILE)
    print(f"\nChecking: {bacteria_path}")
    if os.path.exists(bacteria_path):
        print(f"✓ File exists")
        try:
            df = pd.read_parquet(bacteria_path)
            print(f"  - Rows: {len(df):,}")
            print(f"  - Columns: {list(df.columns)}")
            if 'protein_id' in df.columns:
                print(f"  - Unique proteins: {df['protein_id'].nunique():,}")
                print(f"  - Sample proteins: {list(df['protein_id'].unique()[:3])}")
            print(f"✓ File readable")
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            return False
    else:
        print(f"✗ File NOT found")
        return False
    
    print("\n" + "="*70)
    print("✓ All data files found and readable!")
    print("="*70)
    return True

if __name__ == "__main__":
    success = test_data_files()
    if not success:
        print("\n⚠️  Please check your data folder and file names in config.py")
