import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple

import numpy as np
import torch
import faiss
from PIL import Image
from IPython.display import display
import open_clip

BASE_DIR = Path("./data/indexed_data")
INDEX_DIR = BASE_DIR / "index"
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
TOP_K = 15
HYBRID_CANDIDATES = 300

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("visual-rag-v2")

clip_model, _, _ = open_clip.create_model_and_transforms(
    "ViT-L-14", pretrained="laion2b_s32b_b82k")

clip_model = clip_model.to(DEVICE)
clip_model.eval()
clip_tokenizer = open_clip.get_tokenizer("ViT-B-32")


def function_1(query: str) -> np.ndarray:
    tokens = clip_tokenizer([query]).to(DEVICE)
    with torch.no_grad():
        feats = clip_model.encode_text(tokens)
        feats = feats / feats.norm(dim=-1, keepdim=True)
    return feats.cpu().numpy().astype(np.float32)

class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)
        self.metadata: List[Dict] = []

    def function_2(self, query_vec: np.ndarray, k: int) -> List[Tuple[Dict, float]]:
        query_vec = np.ascontiguousarray(query_vec, dtype=np.float32)
        faiss.normalize_L2(query_vec)
        scores, idxs = self.index.search(query_vec, k)
        out = []
        for j, i in enumerate(idxs[0]):
            if i < 0:
                continue
            out.append((self.metadata[i], float(scores[0][j])))
        return out

def function_3(path: Path) -> VectorStore:
    index = faiss.read_index(str(path / "faiss.index"))
    with open(path / "metadata.json") as f:
        metadata = json.load(f)
    if not isinstance(metadata, list):
        raise TypeError
    store = VectorStore(index.d)
    store.index = index
    store.metadata = metadata
    return store

def function_4(store: VectorStore, query: str, k: int) -> List[Tuple[Dict, float]]:
    q = function_1(query)
    candidates = store.function_2(
        q,
        min(max(HYBRID_CANDIDATES, k * 2), len(store.metadata))
    )
    candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
    return candidates[:k]

def function_5(results, k: int):
    out = []
    i = 1
    for meta, score in results:
        path = Path(meta["path"])
        #if not path.exists():
         #   logger.warning(f"Missing file on disk, skipping: {path}")
          #  continue
        item = {
            "rank" : i,
            "filename" : path.name,
           # "path" : str(path),
            "score" : round(float(score), 6),
            "caption" : meta.get("caption"),
        }
        out.append(item)
        i += 1
        if i > k:
            break
    return out
        
