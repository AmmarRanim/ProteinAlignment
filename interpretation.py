"""Result interpretation and reporting"""


def interpret_alignment(human_id, bact_id, alignments, human_chunks, bact_chunks, 
                       human_descriptors, bact_descriptors):
    """
    Generate human-readable interpretation of alignment results
    
    Args:
        human_id (str): Human protein ID
        bact_id (str): Bacterial protein ID
        alignments (list): List of (score, alignment) tuples
        human_chunks (pd.DataFrame): Human chunks dataframe
        bact_chunks (pd.DataFrame): Bacterial chunks dataframe
        human_descriptors (pd.DataFrame): Human descriptors dataframe
        bact_descriptors (pd.DataFrame): Bacterial descriptors dataframe
        
    Returns:
        str: Formatted interpretation text
    """
    if not alignments:
        return "⚠️ No significant alignments found between the proteins."
    
    lines = []
    lines.append(f"📊 ALIGNMENT ANALYSIS REPORT")
    lines.append("=" * 70)
    lines.append(f"Human Protein:     {human_id}")
    lines.append(f"Bacterial Protein: {bact_id}")
    lines.append("=" * 70)
    
    # Explanation section
    lines.append(f"\n❓ WHAT IS A 'SIGNIFICANT REGION'?\n")
    lines.append(f"   A significant region is a continuous stretch of protein sequence where")
    lines.append(f"   the human and bacterial proteins show strong structural/functional")
    lines.append(f"   similarity based on ESM-2 embeddings (AI protein language model).")
    lines.append(f"")
    lines.append(f"   How it's determined:")
    lines.append(f"   • Proteins are split into overlapping chunks (10 aa, stride 5)")
    lines.append(f"   • Each chunk gets a 1280-dimensional embedding from ESM-2")
    lines.append(f"   • Smith-Waterman alignment finds regions with similarity > 0.5")
    lines.append(f"   • Only regions with alignment score ≥ 1.0 and ≥ 3 chunks are kept")
    lines.append(f"")
    lines.append(f"   These regions may indicate:")
    lines.append(f"   ✓ Conserved functional domains")
    lines.append(f"   ✓ Similar 3D structure")
    lines.append(f"   ✓ Shared evolutionary origin")
    lines.append(f"   ✓ Potential horizontal gene transfer")
    
    lines.append(f"\n" + "=" * 70)
    lines.append(f"🎯 ALIGNMENT SUMMARY\n")
    lines.append(f"   Number of significant regions found: {len(alignments)}")
    
    for idx, (score, alignment) in enumerate(alignments, 1):
        if not alignment:
            continue
        
        # Get aligned chunk indices
        human_indices = [a[0] for a in alignment]
        bact_indices = [a[1] for a in alignment]
        
        # Get sequence positions
        h_start = human_chunks.iloc[human_indices[0]]['start']
        h_end = human_chunks.iloc[human_indices[-1]]['end']
        b_start = bact_chunks.iloc[bact_indices[0]]['start']
        b_end = bact_chunks.iloc[bact_indices[-1]]['end']
        
        lines.append(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🔬 REGION {idx}")
        lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"   Alignment Score: {score:.2f}")
        lines.append(f"   (Higher = stronger similarity; Score ≥ 15 is very strong)")
        lines.append(f"\n   📍 Aligned Positions:")
        lines.append(f"      Human:    {h_start:4d} → {h_end:4d}  ({len(human_indices)} chunks ≈ {len(human_indices)*5} aa)")
        lines.append(f"      Bacteria: {b_start:4d} → {b_end:4d}  ({len(bact_indices)} chunks ≈ {len(bact_indices)*5} aa)")
        lines.append(f"")
        lines.append(f"      → These specific parts of the two proteins are similar!")
        
        # Get descriptor statistics for aligned regions
        h_desc = human_descriptors[human_descriptors['chunk_index'].isin(human_indices)]
        b_desc = bact_descriptors[bact_descriptors['chunk_index'].isin(bact_indices)]
        
        if not h_desc.empty and not b_desc.empty:
            lines.append(f"\n   🧪 Biochemical Properties Comparison:")
            lines.append(f"   {'─' * 60}")
            
            # Hydrophobicity (GRAVY)
            if 'GRAVY' in h_desc.columns and 'GRAVY' in b_desc.columns:
                h_gravy = h_desc['GRAVY'].mean()
                b_gravy = b_desc['GRAVY'].mean()
                diff = h_gravy - b_gravy
                indicator = "⬆️" if diff > 0.5 else "⬇️" if diff < -0.5 else "≈"
                lines.append(f"      Hydrophobicity (GRAVY):")
                lines.append(f"         Human: {h_gravy:7.3f}  │  Bacteria: {b_gravy:7.3f}  │  Δ: {diff:+7.3f} {indicator}")
            
            # Aromaticity
            if 'aromaticity' in h_desc.columns and 'aromaticity' in b_desc.columns:
                h_arom = h_desc['aromaticity'].mean()
                b_arom = b_desc['aromaticity'].mean()
                diff = h_arom - b_arom
                indicator = "⬆️" if diff > 0.05 else "⬇️" if diff < -0.05 else "≈"
                lines.append(f"      Aromaticity:")
                lines.append(f"         Human: {h_arom:7.3f}  │  Bacteria: {b_arom:7.3f}  │  Δ: {diff:+7.3f} {indicator}")
            
            # Hydrophobic fraction
            if 'hydrophobic_fraction' in h_desc.columns and 'hydrophobic_fraction' in b_desc.columns:
                h_hydro = h_desc['hydrophobic_fraction'].mean()
                b_hydro = b_desc['hydrophobic_fraction'].mean()
                diff = h_hydro - b_hydro
                indicator = "⬆️" if diff > 0.1 else "⬇️" if diff < -0.1 else "≈"
                lines.append(f"      Hydrophobic Fraction:")
                lines.append(f"         Human: {h_hydro:7.3f}  │  Bacteria: {b_hydro:7.3f}  │  Δ: {diff:+7.3f} {indicator}")
            
            # Polar fraction
            if 'polar_fraction' in h_desc.columns and 'polar_fraction' in b_desc.columns:
                h_polar = h_desc['polar_fraction'].mean()
                b_polar = b_desc['polar_fraction'].mean()
                diff = h_polar - b_polar
                indicator = "⬆️" if diff > 0.1 else "⬇️" if diff < -0.1 else "≈"
                lines.append(f"      Polar Fraction:")
                lines.append(f"         Human: {h_polar:7.3f}  │  Bacteria: {b_polar:7.3f}  │  Δ: {diff:+7.3f} {indicator}")
            
            # Charge
            if 'charge_at_pH7' in h_desc.columns and 'charge_at_pH7' in b_desc.columns:
                h_charge = h_desc['charge_at_pH7'].mean()
                b_charge = b_desc['charge_at_pH7'].mean()
                diff = h_charge - b_charge
                indicator = "⬆️" if diff > 2 else "⬇️" if diff < -2 else "≈"
                lines.append(f"      Charge at pH 7:")
                lines.append(f"         Human: {h_charge:7.3f}  │  Bacteria: {b_charge:7.3f}  │  Δ: {diff:+7.3f} {indicator}")
            
            # Shannon entropy
            if 'shannon_entropy' in h_desc.columns and 'shannon_entropy' in b_desc.columns:
                h_entropy = h_desc['shannon_entropy'].mean()
                b_entropy = b_desc['shannon_entropy'].mean()
                diff = h_entropy - b_entropy
                indicator = "⬆️" if diff > 0.2 else "⬇️" if diff < -0.2 else "≈"
                lines.append(f"      Shannon Entropy:")
                lines.append(f"         Human: {h_entropy:7.3f}  │  Bacteria: {b_entropy:7.3f}  │  Δ: {diff:+7.3f} {indicator}")
            
            # Instability
            if 'instability_index' in h_desc.columns and 'instability_index' in b_desc.columns:
                h_instab = h_desc['instability_index'].mean()
                b_instab = b_desc['instability_index'].mean()
                diff = h_instab - b_instab
                indicator = "⬆️" if diff > 10 else "⬇️" if diff < -10 else "≈"
                lines.append(f"      Instability Index:")
                lines.append(f"         Human: {h_instab:7.3f}  │  Bacteria: {b_instab:7.3f}  │  Δ: {diff:+7.3f} {indicator}")
    
    # Summary
    lines.append("\n" + "=" * 70)
    lines.append("📈 OVERALL SUMMARY")
    lines.append("=" * 70)
    total_aligned_chunks = sum(len(alignment) for _, alignment in alignments)
    avg_score = sum(score for score, _ in alignments) / len(alignments)
    max_score = max(score for score, _ in alignments)
    
    lines.append(f"   Total regions found:        {len(alignments)}")
    lines.append(f"   Total aligned chunk pairs:  {total_aligned_chunks}")
    lines.append(f"   Average alignment score:    {avg_score:.2f}")
    lines.append(f"   Maximum alignment score:    {max_score:.2f}")
    
    # Interpretation hint
    lines.append("\n   💡 Interpretation Guide:")
    if avg_score > 15:
        lines.append("      ✅ Strong similarity detected - High confidence alignment")
    elif avg_score > 10:
        lines.append("      ✓  Moderate similarity - Potential functional relationship")
    elif avg_score > 5:
        lines.append("      ⚠️  Weak similarity - Consider with caution")
    else:
        lines.append("      ❌ Very weak similarity - Likely not functionally related")
    
    lines.append("=" * 70)
    
    return "\n".join(lines)


def generate_summary_stats(human_chunks, bact_chunks, alignments, 
                          human_descriptors, bact_descriptors):
    """
    Generate summary statistics for the analysis
    
    Args:
        human_chunks (pd.DataFrame): Human chunks
        bact_chunks (pd.DataFrame): Bacterial chunks
        alignments (list): List of alignments
        human_descriptors (pd.DataFrame): Human descriptors
        bact_descriptors (pd.DataFrame): Bacterial descriptors
        
    Returns:
        dict: Summary statistics
    """
    stats = {
        'num_human_chunks': len(human_chunks),
        'num_bact_chunks': len(bact_chunks),
        'num_alignments': len(alignments),
        'total_aligned_chunks': sum(len(alignment) for _, alignment in alignments),
        'max_score': max((score for score, _ in alignments), default=0),
        'avg_score': sum(score for score, _ in alignments) / len(alignments) if alignments else 0,
    }
    
    return stats
