# canonmap/services/artifact_generator/artifact_generator.py

from pathlib import Path
from typing import List, Optional, Union, Dict, Any
import json
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

from canonmap.utils.get_cpu_count import get_cpu_count
from canonmap.utils.load_spacy_model import load_spacy_model
from canonmap.services.artifact_generator._from_csv_helper import convert_csv_to_df
from canonmap.services.artifact_generator._run_pipeline import run_artifact_generation_pipeline


class ArtifactGenerator:
    def __init__(
        self,
        nlp: Optional[Any] = None,
        embedding_model_name: str = "intfloat/e5-base-v2",
        batch_size: int = 64,
    ):
        self.num_cores = get_cpu_count()
        self.nlp = nlp or load_spacy_model()
        self.embedding_model_name = embedding_model_name
        self.batch_size = batch_size
        self._init_embedding_model()

    def _init_embedding_model(self):
        # set device
        self.device = torch.device(
            "cuda" if torch.cuda.is_available()
            else "mps" if torch.backends.mps.is_available()
            else "cpu"
        )
        # load tokenizer & model
        self.tokenizer = AutoTokenizer.from_pretrained(self.embedding_model_name)
        model = AutoModel.from_pretrained(self.embedding_model_name)
        model.to(self.device)
        model.eval()
        self.embed_model = model

    def _embed_texts(self, texts: List[str]) -> np.ndarray:
        all_embs = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            inputs = self.tokenizer(batch, padding=True, truncation=True, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                out = self.embed_model(**inputs)
            cls_emb = out.last_hidden_state[:, 0, :].cpu().numpy()
            all_embs.append(cls_emb)
        return np.vstack(all_embs)

    def generate_artifacts_from_csv(
        self,
        csv_path: str,
        output_path: Union[str, Path],
        name: str,
        entity_fields: Optional[List[str]] = None,
        use_other_fields_as_metadata: bool = False,
        num_rows: Optional[int] = None,
        embed: bool = True,
    ) -> Dict[str, Any]:
        # existing pipeline for metadata & schema
        df = convert_csv_to_df(csv_path=csv_path, num_rows=num_rows)
        result = run_artifact_generation_pipeline(
            num_cores=self.num_cores,
            df=df,
            output_path=output_path,
            name=name,
            entity_fields=entity_fields,
            use_other_fields_as_metadata=use_other_fields_as_metadata,
            nlp=self.nlp,
        )
        # optionally embed
        if embed:
            metadata = result["metadata"]
            paths = result["paths"]
            flat = [ {m["_field_name_"]: m["_canonical_entity_"]} for m in metadata ]
            texts = [json.dumps(r, default=str) for r in flat]
            embeddings = self._embed_texts(texts)
            np.savez_compressed(paths["embeddings"], embeddings=embeddings)
            result["embeddings"] = embeddings
        return result