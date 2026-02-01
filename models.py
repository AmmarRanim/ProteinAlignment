"""ESM-2 model loading and management"""
import torch
import esm

# Global model cache
_esm_model = None
_esm_alphabet = None
_esm_batch_converter = None


def get_esm2_model():
    """
    Load ESM-2 model (cached globally to avoid reloading)
    
    Returns:
        tuple: (model, alphabet, batch_converter)
    """
    global _esm_model, _esm_alphabet, _esm_batch_converter
    
    if _esm_model is None:
        print("Loading ESM-2 model...")
        _esm_model, _esm_alphabet = esm.pretrained.esm2_t33_650M_UR50D()
        _esm_batch_converter = _esm_alphabet.get_batch_converter()
        _esm_model.eval()
        
        # Move to GPU if available
        if torch.cuda.is_available():
            _esm_model = _esm_model.cuda()
            print("Model loaded on GPU")
        else:
            print("Model loaded on CPU")
    
    return _esm_model, _esm_alphabet, _esm_batch_converter


def compute_embeddings(sequences):
    """
    Compute ESM-2 embeddings for a list of sequences
    
    Args:
        sequences (list): List of protein sequences
        
    Returns:
        numpy.ndarray: Embeddings matrix (n_sequences x embedding_dim)
    """
    model, alphabet, batch_converter = get_esm2_model()
    
    # Prepare batch
    data = [(f"seq_{i}", seq) for i, seq in enumerate(sequences)]
    batch_labels, batch_strs, batch_tokens = batch_converter(data)
    
    # Move to GPU if available
    if torch.cuda.is_available():
        batch_tokens = batch_tokens.cuda()
    
    # Compute embeddings
    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[33], return_contacts=False)
        embeddings = results["representations"][33]
    
    # Mean pooling over sequence length (excluding start/end tokens)
    embeddings = embeddings[:, 1:-1, :].mean(dim=1)
    
    return embeddings.cpu().numpy()
