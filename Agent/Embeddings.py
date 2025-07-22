import os
from typing import List, Dict, Any
from matplotlib.style.core import available
from torch.version import cuda
from transformers import DPRContextEncoder, DPRContextEncoderTokenizer
import torch
import numpy as np

class EmbeddingEncoder:

    def __init__(self,):
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")
        print(self.device)
        self.tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
        self.model = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base").to(self.device)


    def get_embedding(self, text: str) -> List[float]:
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True,
                           max_length=512).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.pooler_output[0].cpu().numpy().tolist()