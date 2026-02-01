"""Test PfamScan setup via WSL"""
import subprocess
import os

def test_wsl():
    """Test if WSL is available"""
    print("Testing WSL...")
    try:
        result = subprocess.run(['wsl', 'echo', 'WSL is working'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ WSL is available")
            return True
        else:
            print("✗ WSL error:", result.stderr)
            return False
    except Exception as e:
        print(f"✗ WSL not available: {e}")
        return False

def test_hmmer():
    """Test if HMMER is installed"""
    print("\nTesting HMMER...")
    try:
        result = subprocess.run(['wsl', 'hmmscan', '-h'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ HMMER is installed")
            return True
        else:
            print("✗ HMMER not found")
            return False
    except Exception as e:
        print(f"✗ HMMER error: {e}")
        return False

def test_pfam_database():
    """Test if Pfam database exists"""
    print("\nTesting Pfam database...")
    try:
        result = subprocess.run(['wsl', 'ls', '-la', '~/pfam/Pfam-A.hmm'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ Pfam database found")
            print(f"  {result.stdout.strip()}")
            return True
        else:
            print("✗ Pfam database not found at ~/pfam/Pfam-A.hmm")
            return False
    except Exception as e:
        print(f"✗ Error checking database: {e}")
        return False

def test_pfam_index():
    """Test if Pfam index files exist"""
    print("\nTesting Pfam index files...")
    try:
        result = subprocess.run(['wsl', 'ls', '~/pfam/Pfam-A.hmm.h3*'], 
                               capture_output=True, text=True, timeout=10)
        if 'h3m' in result.stdout or 'h3i' in result.stdout:
            print("✓ Pfam index files found")
            return True
        else:
            print("✗ Pfam index files not found (run: hmmpress ~/pfam/Pfam-A.hmm)")
            return False
    except Exception as e:
        print(f"✗ Error checking index: {e}")
        return False

def test_pfamscan_script():
    """Test if PfamScan script exists"""
    print("\nTesting PfamScan script...")
    try:
        result = subprocess.run(['wsl', 'ls', '-la', '~/pfam/PfamScan/pfam_scan.pl'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ PfamScan script found")
            return True
        else:
            print("✗ PfamScan script not found")
            return False
    except Exception as e:
        print(f"✗ Error checking script: {e}")
        return False

def test_pfamscan_run():
    """Test running PfamScan on a test sequence"""
    print("\nTesting PfamScan execution...")
    
    # Create test sequence
    test_seq = "MKTFIFLALLGAAVAFPVDDDDKIVGGYTCGANTVPYQVSLNSGYHFCGGSLINSQWVVSAAHCYKSGIQVRLGEDNINVVEGNEQFISASKSIVHPSYNSNTLNNDIMLIKLKSAASLNSRVASISLPTSCASAGTQCLISGWGNTKSSGTSYPDVLKCLKAPILSDSSCKSAYPGQITSNMFCAGYLEGGKDSCQGDSGGPVVCSGKLQGIVSWGSGCAQKNKPGVYTKVCNYVSWIKQTIASN"
    
    # Create temp directory
    os.makedirs("cache/pfam_temp", exist_ok=True)
    
    # Write test FASTA
    with open("cache/pfam_temp/test.fasta", "w") as f:
        f.write(f">test\n{test_seq}\n")
    
    # Get WSL path
    try:
        wsl_fasta = subprocess.run(
            ['wsl', 'wslpath', '-u', os.path.abspath("cache/pfam_temp/test.fasta")],
            capture_output=True, text=True
        ).stdout.strip()
        
        wsl_output = subprocess.run(
            ['wsl', 'wslpath', '-u', os.path.abspath("cache/pfam_temp/test_pfam.out")],
            capture_output=True, text=True
        ).stdout.strip()
        
        print(f"  FASTA path: {wsl_fasta}")
        print(f"  Output path: {wsl_output}")
        
        # Run PfamScan
        cmd = f"perl ~/pfam/PfamScan/pfam_scan.pl -fasta {wsl_fasta} -dir ~/pfam -outfile {wsl_output} -cpu 2"
        print(f"  Running: {cmd}")
        
        result = subprocess.run(
            ['wsl', 'bash', '-c', cmd],
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0:
            print("✓ PfamScan executed successfully")
            
            # Check output
            if os.path.exists("cache/pfam_temp/test_pfam.out"):
                with open("cache/pfam_temp/test_pfam.out", "r") as f:
                    content = f.read()
                    print("\n  Output:")
                    for line in content.split('\n')[:10]:
                        print(f"    {line}")
                    
                    # Count domains
                    domains = [l for l in content.split('\n') if l.strip() and not l.startswith('#')]
                    print(f"\n  Found {len(domains)} domain hits")
                return True
            else:
                print("✗ Output file not created")
                return False
        else:
            print(f"✗ PfamScan failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ PfamScan timed out (>120 seconds)")
        return False
    except Exception as e:
        print(f"✗ Error running PfamScan: {e}")
        return False


if __name__ == "__main__":
    print("="*70)
    print("PfamScan Setup Test")
    print("="*70)
    
    results = []
    
    results.append(("WSL", test_wsl()))
    results.append(("HMMER", test_hmmer()))
    results.append(("Pfam Database", test_pfam_database()))
    results.append(("Pfam Index", test_pfam_index()))
    results.append(("PfamScan Script", test_pfamscan_script()))
    results.append(("PfamScan Run", test_pfamscan_run()))
    
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:20s} {status}")
        if not passed:
            all_passed = False
    
    print("="*70)
    if all_passed:
        print("✓ All tests passed! PfamScan is ready to use.")
    else:
        print("✗ Some tests failed. Please complete the setup steps.")
        print("\nSetup commands:")
        print("  wsl sudo apt-get update")
        print("  wsl sudo apt-get install -y hmmer cpanminus perl git")
        print("  wsl sudo cpanm Moose JSON List::MoreUtils")
        print("  wsl mkdir -p ~/pfam")
        print("  wsl wget -P ~/pfam ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz")
        print("  wsl gunzip ~/pfam/Pfam-A.hmm.gz")
        print("  wsl hmmpress ~/pfam/Pfam-A.hmm")
        print("  wsl git clone https://github.com/aziele/pfam_scan.git ~/pfam/PfamScan")
    print("="*70)
