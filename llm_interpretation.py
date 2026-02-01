"""LLM-based interpretation using Groq API"""
import json
import os


def prepare_analysis_data(human_id, bact_id, alignments, human_chunks, bact_chunks,
                         human_descriptors, bact_descriptors, similarity_matrix):
    """
    Prepare comprehensive data for LLM analysis
    
    Args:
        human_id (str): Human protein ID
        bact_id (str): Bacterial protein ID
        alignments (list): List of (score, alignment) tuples
        human_chunks (pd.DataFrame): Human chunks
        bact_chunks (pd.DataFrame): Bacterial chunks
        human_descriptors (pd.DataFrame): Human descriptors
        bact_descriptors (pd.DataFrame): Bacterial descriptors
        similarity_matrix (np.ndarray): Similarity matrix
        
    Returns:
        dict: Prepared data for LLM
    """
    if not alignments:
        return None
    
    # Get the best alignment
    score, alignment = alignments[0]
    
    # Extract aligned chunk indices
    human_indices = [a[0] for a in alignment]
    bact_indices = [a[1] for a in alignment]
    
    # Get aligned regions
    h_start = human_chunks.iloc[human_indices[0]]['start']
    h_end = human_chunks.iloc[human_indices[-1]]['end']
    b_start = bact_chunks.iloc[bact_indices[0]]['start']
    b_end = bact_chunks.iloc[bact_indices[-1]]['end']
    
    # Get descriptors for aligned regions
    h_desc = human_descriptors[human_descriptors['chunk_index'].isin(human_indices)]
    b_desc = bact_descriptors[bact_descriptors['chunk_index'].isin(bact_indices)]
    
    # Prepare data
    data = {
        'proteins': {
            'human': {
                'id': human_id,
                'total_length': len(human_chunks) * 5,  # Approximate
                'aligned_region': f"{h_start}-{h_end}",
                'num_chunks': len(human_indices)
            },
            'bacteria': {
                'id': bact_id,
                'total_length': len(bact_chunks) * 5,  # Approximate
                'aligned_region': f"{b_start}-{b_end}",
                'num_chunks': len(bact_indices)
            }
        },
        'alignment': {
            'score': float(score),
            'length': len(alignment),
            'avg_similarity': float(similarity_matrix[human_indices, :][:, bact_indices].mean())
        },
        'biochemical_comparison': {}
    }
    
    # Add biochemical properties
    if not h_desc.empty and not b_desc.empty:
        properties = ['gravy', 'aromaticity', 'helix_fraction', 'sheet_fraction', 
                     'charge_at_pH7', 'instability_index']
        
        for prop in properties:
            if prop in h_desc.columns and prop in b_desc.columns:
                data['biochemical_comparison'][prop] = {
                    'human': float(h_desc[prop].mean()),
                    'bacteria': float(b_desc[prop].mean()),
                    'difference': float(h_desc[prop].mean() - b_desc[prop].mean())
                }
    
    return data


def generate_llm_prompt(data):
    """
    Generate a comprehensive prompt for LLM analysis
    
    Args:
        data (dict): Prepared analysis data
        
    Returns:
        str: Formatted prompt
    """
    prompt = f"""You are an expert protein bioinformatician. Analyze this protein alignment systematically.

**PROTEINS ANALYZED:**
- Human: {data['proteins']['human']['id']} (Length: ~{data['proteins']['human']['total_length']} aa)
- Bacteria: {data['proteins']['bacteria']['id']} (Length: ~{data['proteins']['bacteria']['total_length']} aa)

**ALIGNMENT RESULTS:**
- Alignment Score: {data['alignment']['score']:.2f}
- Aligned Region (Human): positions {data['proteins']['human']['aligned_region']}
- Aligned Region (Bacteria): positions {data['proteins']['bacteria']['aligned_region']}
- Number of aligned chunks: {data['alignment']['length']}
- Average similarity: {data['alignment']['avg_similarity']:.3f}

**BIOCHEMICAL PROPERTIES COMPARISON:**
"""
    
    for prop, values in data['biochemical_comparison'].items():
        prompt += f"\n{prop.replace('_', ' ').title()}:"
        prompt += f"\n  Human: {values['human']:.3f}"
        prompt += f"\n  Bacteria: {values['bacteria']:.3f}"
        prompt += f"\n  Difference: {values['difference']:.3f}"
    
    prompt += """

**ANALYSIS TASKS:**
1. Evaluate the biological significance of this alignment
2. Interpret the biochemical property differences
3. Discuss potential functional implications
4. Assess whether this suggests:
   - Convergent evolution
   - Horizontal gene transfer
   - Conserved functional domain
   - Random similarity
5. Provide specific insights about the aligned regions

Please provide a clear, scientific interpretation in 3-4 paragraphs.
"""
    
    return prompt


def generate_llm_prompt_full(data):
    """
    Generate comprehensive prompt matching notebook structure exactly
    
    Args:
        data (dict): Prepared analysis data with functional annotations
        
    Returns:
        str: Formatted prompt
    """
    # Extract data
    human_info = data['proteins']['human']
    bact_info = data['proteins']['bacteria']
    alignment_info = data['alignment']
    biochem = data.get('biochemical_comparison', {})
    human_func = data.get('human_functional', {})
    bact_func = data.get('bact_functional', {})
    domain_overlap = data.get('domain_overlap', {})
    
    # Format Pfam domains
    human_domains = human_func.get('pfam_domains', [])
    bact_domains = bact_func.get('pfam_domains', [])
    shared_domains = domain_overlap.get('shared_domains', [])
    
    # Build prompt matching notebook structure
    prompt = f"""You are an expert protein bioinformatician. Analyze this ESM2 embedding alignment systematically.

ANALYSIS FRAMEWORK - Weigh ALL evidence fairly:
1. Domain analysis is IMPORTANT but not the only factor
2. Alignment coverage and continuity are SIGNIFICANT signals
3. Biochemical similarity provides FUNCTIONAL context
4. Consider ALL evidence before concluding

=== PROTEIN PAIR ===
Human: {human_info['id']}
  - Length: ~{human_info.get('total_length', 'N/A')} aa
  - Pfam domains: {', '.join(human_domains) if human_domains else 'None detected'}
  - Prosite motifs: {', '.join(human_func.get('prosite_motifs', [])) if human_func.get('prosite_motifs') else 'None'}
  - Signal peptide: {'Yes' if human_func.get('has_signal_peptide') else 'No'}
  - TM helices: {human_func.get('tm_helix_count', 0)}

Bacteria: {bact_info['id']}
  - Length: ~{bact_info.get('total_length', 'N/A')} aa
  - Pfam domains: {', '.join(bact_domains) if bact_domains else 'None detected'}
  - Prosite motifs: {', '.join(bact_func.get('prosite_motifs', [])) if bact_func.get('prosite_motifs') else 'None'}
  - Signal peptide: {'Yes' if bact_func.get('has_signal_peptide') else 'No'}
  - TM helices: {bact_func.get('tm_helix_count', 0)}

=== DOMAIN OVERLAP ===
Shared Pfam domains: {', '.join(shared_domains) if shared_domains else 'NONE'}
Domain overlap detected: {'YES - SIGNIFICANT' if shared_domains else 'NO'}

=== ALIGNMENT SUMMARY ===
- Alignment score: {alignment_info['score']:.2f}
- Aligned chunks: {alignment_info['length']}
- Human aligned region: {human_info.get('aligned_region', 'N/A')}
- Bacteria aligned region: {bact_info.get('aligned_region', 'N/A')}
- Average similarity: {alignment_info.get('avg_similarity', 0):.3f}

=== BIOCHEMICAL DESCRIPTORS COMPARISON ===
"""
    
    # Add biochemical comparisons
    for prop, values in biochem.items():
        prop_name = prop.replace('_', ' ').title()
        prompt += f"\n{prop_name}:"
        prompt += f"\n  Human: {values['human']:.4f}"
        prompt += f"\n  Bacteria: {values['bacteria']:.4f}"
        prompt += f"\n  Difference: {values['difference']:.4f}"
    
    prompt += """

=== ANALYSIS REQUIRED ===

Based on ALL the evidence above, provide:

1. **BIOLOGICAL SIGNIFICANCE** (2-3 sentences)
   - Is this alignment biologically meaningful?
   - What does the alignment score and coverage suggest?

2. **DOMAIN ANALYSIS** (2-3 sentences)
   - Interpret the Pfam domain overlap (or lack thereof)
   - What does this suggest about functional relationship?

3. **BIOCHEMICAL INTERPRETATION** (2-3 sentences)
   - Compare the biochemical properties
   - What do the similarities/differences suggest?

4. **EVOLUTIONARY HYPOTHESIS** (2-3 sentences)
   - Most likely explanation: convergent evolution, horizontal gene transfer, conserved domain, or random similarity?
   - Justify your conclusion based on the evidence

5. **CONFIDENCE ASSESSMENT** (1-2 sentences)
   - Rate confidence: HIGH, MEDIUM, or LOW
   - What additional evidence would strengthen the conclusion?

Provide a balanced, evidence-based analysis. Do not over-interpret weak signals.
"""
    
    return prompt


def call_groq_api(prompt, api_key):
    """
    Call Groq API for LLM interpretation
    
    Args:
        prompt (str): The prompt to send
        api_key (str): Groq API key
        
    Returns:
        str: LLM response
    """
    try:
        from groq import Groq
        
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert protein bioinformatician specializing in sequence analysis and evolutionary biology."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000,
            top_p=0.9
        )
        
        return response.choices[0].message.content
        
    except ImportError:
        return "Error: Groq library not installed. Run: pip install groq"
    except Exception as e:
        return f"Error calling Groq API: {str(e)}"


def get_llm_interpretation(human_id, bact_id, alignments, human_chunks, bact_chunks,
                          human_descriptors, bact_descriptors, similarity_matrix, 
                          human_functional=None, bact_functional=None, domain_overlap=None,
                          api_key=None):
    """
    Get LLM-powered interpretation of alignment results
    
    Args:
        human_id (str): Human protein ID
        bact_id (str): Bacterial protein ID
        alignments (list): Alignment results
        human_chunks (pd.DataFrame): Human chunks
        bact_chunks (pd.DataFrame): Bacterial chunks
        human_descriptors (pd.DataFrame): Human descriptors
        bact_descriptors (pd.DataFrame): Bacterial descriptors
        similarity_matrix (np.ndarray): Similarity matrix
        human_functional (dict): Human functional annotations
        bact_functional (dict): Bacterial functional annotations
        domain_overlap (dict): Domain overlap information
        api_key (str): Groq API key (optional, can be set in environment)
        
    Returns:
        str: LLM interpretation or error message
    """
    # Check for API key
    if api_key is None:
        api_key = os.environ.get('GROQ_API_KEY')
    
    if not api_key:
        return """
LLM Interpretation Not Available

To enable AI-powered interpretation:
1. Get a free API key from: https://console.groq.com/keys
2. Set it in config.py or as environment variable GROQ_API_KEY
3. Install groq: pip install groq

The basic interpretation above provides the key findings.
"""
    
    # Prepare data
    data = prepare_analysis_data(
        human_id, bact_id, alignments, 
        human_chunks, bact_chunks,
        human_descriptors, bact_descriptors,
        similarity_matrix
    )
    
    if data is None:
        return "No alignment data available for LLM interpretation."
    
    # Add functional annotations to data
    data['human_functional'] = human_functional or {}
    data['bact_functional'] = bact_functional or {}
    data['domain_overlap'] = domain_overlap or {}
    
    # Generate prompt (matching notebook structure)
    prompt = generate_llm_prompt_full(data)
    
    # Call LLM
    print("Calling Groq API for LLM interpretation...")
    interpretation = call_groq_api(prompt, api_key)
    
    return interpretation
