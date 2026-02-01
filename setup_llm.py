"""Quick setup for LLM interpretation (writes .env)"""

print("="*70)
print("LLM Interpretation Setup")
print("="*70)
print()
print("To enable AI-powered interpretation:")
print()
print("1. Get a FREE API key:")
print("   → Go to: https://console.groq.com/keys")
print("   → Sign up (free)")
print("   → Create new API key")
print("   → Copy the key (starts with 'gsk_...')")
print()
print("2. Install groq library:")
print("   → Run: pip install groq")
print()
print("3. Set your API key:")
print()
api_key = input("Paste your Groq API key here (or press Enter to skip): ").strip()

if api_key:
    # Write to .env file (ignored by git). config.py reads from env.
    try:
        env_path = '.env'
        lines = []
        # Preserve existing .env content if exists, replacing GROQ_API_KEY
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        key_written = False
        new_lines = []
        for line in lines:
            if line.strip().startswith('GROQ_API_KEY='):
                new_lines.append(f'GROQ_API_KEY={api_key}\n')
                key_written = True
            else:
                new_lines.append(line)
        if not key_written:
            new_lines.append(f'GROQ_API_KEY={api_key}\n')
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("\n✓ API key saved to .env (git-ignored)")
        print("✓ LLM interpretation is now enabled!")
        print()
        print("Run the app: python app.py")
        print("Note: config loads .env automatically (python-dotenv).")
    except Exception as e:
        print(f"\n✗ Error writing .env: {e}")
        print("   You can set it manually as an environment variable:")
        print('   Windows (PowerShell): $Env:GROQ_API_KEY = "your_key_here"')
        print('   Linux/macOS (bash):   export GROQ_API_KEY="your_key_here"')
else:
    print("\nSkipped. You can set it later via:")
    print('  1) .env file: GROQ_API_KEY=your_key_here')
    print('  2) Environment variable:')
    print('     Windows (PowerShell): $Env:GROQ_API_KEY = "your_key_here"')
    print('     Linux/macOS (bash):   export GROQ_API_KEY="your_key_here"')

print()
print("="*70)
