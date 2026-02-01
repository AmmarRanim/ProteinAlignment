# LLM Interpretation Setup Guide

## Overview

The application now includes **AI-powered interpretation** using Groq's Llama 3.3 70B model. This provides expert-level analysis of your protein alignment results.

## Features

The LLM provides:
- Biological significance evaluation
- Biochemical property interpretation
- Functional implications discussion
- Evolutionary insights (convergent evolution, HGT, conserved domains)
- Specific insights about aligned regions

## Setup 

### Step 1: Get a Free Groq API Key

1. Go to: https://console.groq.com/keys
2. Sign up (free account)
3. Create a new API key
4. Copy the key (starts with `gsk_...`)

### Step 2: Configure the API Key

**Option A: Edit config.py**
```python
# In config.py, change this line:
GROQ_API_KEY = "gsk_your_api_key_here"
```

**Option B: Use Environment Variable**
```bash
# Windows
set GROQ_API_KEY=gsk_your_api_key_here

# Linux/Mac
export GROQ_API_KEY=gsk_your_api_key_here
```

### Step 3: Install Groq Library

```bash
pip install groq
```

Or reinstall all requirements:
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

Now when you analyze proteins, you'll get both:
1. **Basic Interpretation** - Statistical analysis
2. **🤖 AI-Powered Interpretation** - Expert LLM analysis


## Troubleshooting

### "groq module not found"
**Fix:**
```bash
pip install groq
```

### "Invalid API key"
**Fix:**
- Check the key is correct
- Make sure it starts with `gsk_`
- Regenerate key at https://console.groq.com/keys

### "Rate limit exceeded"
**Fix:**
- Wait a minute
- Free tier: 30 requests/minute

### LLM interpretation shows error message
**Fix:**
- Check API key is set correctly
- Check internet connection
- Verify groq library is installed

## Privacy & Security

- API key should be kept private
- Don't commit API keys to git
- Use environment variables for production
- Groq processes data securely

## Cost

**FREE!** Groq provides free API access with generous limits.

## Disabling LLM

To disable LLM interpretation:

**Option 1:** Don't set API key (it will show a message)

**Option 2:** Set to None in config.py:
```python
GROQ_API_KEY = None
```


## Summary

- ✅ Free API key from Groq
- ✅ Easy setup (one line in config.py)
- ✅ Expert-level interpretation
- ✅ Fast responses
- ✅ Privacy-focused

Get your free API key and enhance your protein analysis with AI! 🚀
