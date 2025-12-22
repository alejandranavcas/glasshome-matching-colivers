import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel

# Cache model globally to avoid reloading
_tokenizer = None
_model = None

def load_model():
    """Load ME2-BERT model and tokenizer (cached)."""
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained("lorenzozan/ME2-BERT", trust_remote_code=True)
        _model = AutoModel.from_pretrained("lorenzozan/ME2-BERT", trust_remote_code=True)
    return _tokenizer, _model

def get_embeddings(texts):
    """
    Generate embeddings for a list of texts (or a single text) using ME2-BERT.
    Returns: numpy array shape (n_texts, hidden_dim)
    Robust to models that return either a model output object, a list/tuple of tensors,
    or a list of dicts with label scores (e.g., {'CH':..., 'FC':..., ...}).
    """
    # Normalize single-string input to list
    if isinstance(texts, str):
        texts = [texts]
    if not isinstance(texts, (list, tuple)):
        raise ValueError("texts must be a string or a list/tuple of strings")

    tokenizer, model = load_model()

    inputs = tokenizer(texts, padding="max_length", truncation=True, return_tensors="pt")
    model.eval()

    with torch.no_grad():
        outputs = model(**inputs, return_dict=True)

    # 1) Standard case: object with last_hidden_state
    if hasattr(outputs, "last_hidden_state"):
        last_hidden = outputs.last_hidden_state
        embeddings = last_hidden[:, 0, :].cpu().numpy()
        return embeddings

    # 2) If outputs is a dict-like (but not having last_hidden_state), try common keys
    if isinstance(outputs, dict):
        # check for pooled output or logits
        if "pooler_output" in outputs and isinstance(outputs["pooler_output"], torch.Tensor):
            return outputs["pooler_output"].cpu().numpy()
        if "logits" in outputs and isinstance(outputs["logits"], torch.Tensor):
            return outputs["logits"].cpu().numpy()
        # fallthrough to debug
        raise ValueError(f"Model returned dict without recognizable tensor outputs. keys: {list(outputs.keys())}")

    # 3) If outputs is a list/tuple
    if isinstance(outputs, (list, tuple)):
        # 3a) list of dicts -> treat as label scores (e.g., ME2-BERT returns [{'CH':...}, ...])
        first = outputs[0] if len(outputs) > 0 else None
        if isinstance(first, dict):
            # Use a fixed column order consistent with downstream code/notebook
            cols = ['CH', 'FC', 'LB', 'AS', 'PD']
            try:
                arr = np.array([[float(d.get(c, 0.0)) for c in cols] for d in outputs], dtype=float)
                return arr
            except Exception as e:
                raise ValueError(f"Failed to convert list-of-dicts outputs to array: {e}")

        # 3b) list of tensors: look for 3-D last_hidden_state or 2-D pooled outputs
        for elem in outputs:
            if isinstance(elem, torch.Tensor):
                if elem.dim() == 3:
                    return elem[:, 0, :].cpu().numpy()
                if elem.dim() == 2:
                    return elem.cpu().numpy()

    # If we reach here, we couldn't extract embeddings
    raise ValueError(
        f"Could not extract embeddings from model outputs. outputs type: {type(outputs)}; "
        f"outputs repr (truncated): {str(outputs)[:1000]}"
    )



