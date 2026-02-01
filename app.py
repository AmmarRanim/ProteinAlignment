"""
Flask application for protein alignment analysis
"""
from flask import Flask, render_template, request, jsonify

# Import custom modules
from protein_utils import fetch_protein_sequence
from chunking import get_or_create_chunks
from embeddings import get_or_create_embeddings, compute_similarity_matrix
from alignment import smith_waterman_chunks
from descriptors import get_or_create_descriptors
from interpretation import interpret_alignment
from llm_interpretation import get_llm_interpretation
from functional_annotations import compute_functional_annotations, check_domain_overlap
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, GROQ_API_KEY

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Main endpoint for protein analysis
    
    Expects JSON with:
        - human_protein_id: UniProt ID for human protein
        - bacteria_protein_id: UniProt ID for bacterial protein
    
    Returns JSON with analysis results
    """
    try:
        # Parse request
        data = request.json
        human_id = data.get('human_protein_id', '').strip()
        bact_id = data.get('bacteria_protein_id', '').strip()
        
        if not human_id or not bact_id:
            return jsonify({'error': 'Please provide both protein IDs'}), 400
        
        print(f"\n{'='*70}")
        print(f"Starting analysis: {human_id} vs {bact_id}")
        print(f"{'='*70}\n")
        
        # Step 1: Fetch sequences
        print("Step 1: Fetching protein sequences...")
        human_seq = fetch_protein_sequence(human_id)
        bact_seq = fetch_protein_sequence(bact_id)
        print(f"  Human: {len(human_seq)} aa")
        print(f"  Bacteria: {len(bact_seq)} aa\n")
        
        # Step 2: Get or create chunks
        print("Step 2: Chunking sequences...")
        human_chunks = get_or_create_chunks(human_id, human_seq, 'human')
        bact_chunks = get_or_create_chunks(bact_id, bact_seq, 'bacteria')
        print(f"  Human chunks: {len(human_chunks)}")
        print(f"  Bacteria chunks: {len(bact_chunks)}\n")
        
        # Step 3: Get or create embeddings
        print("Step 3: Computing embeddings...")
        human_emb = get_or_create_embeddings(human_chunks, human_id)
        bact_emb = get_or_create_embeddings(bact_chunks, bact_id)
        print(f"  Embeddings computed\n")
        
        # Step 4: Compute similarity matrix
        print("Step 4: Computing similarity matrix...")
        similarity_matrix = compute_similarity_matrix(human_emb, bact_emb)
        print(f"  Similarity matrix shape: {similarity_matrix.shape}\n")
        
        # Step 5: Smith-Waterman alignment
        print("Step 5: Running Smith-Waterman alignment...")
        score, alignment, _ = smith_waterman_chunks(similarity_matrix)
        print(f"  Alignment score: {score:.2f}")
        print(f"  Aligned chunks: {len(alignment)}\n")
        
        # Step 6: Get or create descriptors
        print("Step 6: Computing biochemical descriptors...")
        human_descriptors = get_or_create_descriptors(human_chunks, human_id)
        bact_descriptors = get_or_create_descriptors(bact_chunks, bact_id)
        print(f"  Descriptors computed\n")
        
        # Step 6b: Compute functional annotations (Pfam, Prosite, Signal peptide, TM)
        print("Step 6b: Computing functional annotations...")
        human_functional = compute_functional_annotations(human_seq, human_id)
        bact_functional = compute_functional_annotations(bact_seq, bact_id)
        domain_overlap = check_domain_overlap(
            human_functional.get('pfam_domains', []),
            bact_functional.get('pfam_domains', [])
        )
        print(f"  Functional annotations computed\n")
        
        # Step 7: Generate interpretation
        print("Step 7: Generating interpretation...")
        alignments = [(score, alignment)] if alignment else []
        interpretation = interpret_alignment(
            human_id, bact_id, alignments,
            human_chunks, bact_chunks,
            human_descriptors, bact_descriptors
        )
        print(f"  Basic interpretation generated\n")
        
        # Step 8: Get LLM interpretation (if API key available)
        print("Step 8: Generating LLM interpretation...")
        llm_interpretation = get_llm_interpretation(
            human_id, bact_id, alignments,
            human_chunks, bact_chunks,
            human_descriptors, bact_descriptors,
            similarity_matrix,
            human_functional=human_functional,
            bact_functional=bact_functional,
            domain_overlap=domain_overlap,
            api_key=GROQ_API_KEY
        )
        print(f"  LLM interpretation generated\n")
        
        print(f"{'='*70}")
        print("Analysis complete!")
        print(f"{'='*70}\n")
        
        # Return results
        return jsonify({
            'success': True,
            'human_protein': human_id,
            'bacteria_protein': bact_id,
            'human_length': len(human_seq),
            'bacteria_length': len(bact_seq),
            'num_human_chunks': len(human_chunks),
            'num_bacteria_chunks': len(bact_chunks),
            'alignment_score': float(score),
            'num_aligned_chunks': len(alignment),
            'interpretation': interpretation,
            'llm_interpretation': llm_interpretation,
            'functional_annotations': {
                'human': human_functional,
                'bacteria': bact_functional,
                'domain_overlap': domain_overlap
            }
        })
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("Starting Protein Alignment Analysis Server")
    print("="*70)
    print(f"Host: {FLASK_HOST}")
    print(f"Port: {FLASK_PORT}")
    print(f"Debug: {FLASK_DEBUG}")
    print("="*70 + "\n")
    
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)
