# canonmap/services/artifact_generator.py
from pathlib import Path
from typing import List, Optional, Union
import json
import numpy as np

import spacy
import torch
from transformers import AutoTokenizer, AutoModel

from canonmap.utils.get_cpu_count import get_cpu_count
from canonmap.utils.load_spacy_model import load_spacy_model
from canonmap.services._from_csv_helper import convert_csv_to_df
from canonmap.services._run_pipeline import run_artifact_generation_pipeline
from canonmap.utils.logger import get_logger

logger = get_logger()

class ArtifactGenerator:
    def __init__(
        self,
        nlp: Optional[spacy.Language] = None,
        embedding_model_name: str = "intfloat/e5-base-v2",
        batch_size: int = 64
    ):
        self.num_cores = get_cpu_count()
        self.nlp = nlp or load_spacy_model()
        self.embedding_model_name = embedding_model_name
        self.batch_size = batch_size
        logger.info(f"Initializing ArtifactGenerator with {self.num_cores} cores")
        self._init_embedding_model()

    def _init_embedding_model(self):
        import torch
        from transformers import AutoTokenizer, AutoModel

        self.device = torch.device("cuda" if torch.cuda.is_available()
                                   else "mps" if torch.backends.mps.is_available()
                                   else "cpu")
        logger.info(f"Loading embedding model {self.embedding_model_name} on {self.device}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.embedding_model_name)
        model = AutoModel.from_pretrained(self.embedding_model_name)
        model.to(self.device)
        model.eval()
        self.embed_model = model
        logger.info("Embedding model loaded successfully")

    def _embed_texts(self, texts: List[str]) -> np.ndarray:
        import torch
        import numpy as np

        logger.info(f"Generating embeddings for {len(texts)} texts in batches of {self.batch_size}")
        all_embs = []
        total_batches = (len(texts) + self.batch_size - 1) // self.batch_size
        
        for i in range(0, len(texts), self.batch_size):
            batch_num = i // self.batch_size + 1
            logger.info(f"Processing batch {batch_num}/{total_batches}")
            batch = texts[i : i + self.batch_size]
            inputs = self.tokenizer(batch, padding=True, truncation=True, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                out = self.embed_model(**inputs)
            cls_emb = out.last_hidden_state[:, 0, :].cpu().numpy()
            all_embs.append(cls_emb)
        
        logger.info("Embedding generation complete")
        return np.vstack(all_embs)

    def generate_artifacts_from_csv(
        self,
        csv_path: str,
        output_path: Union[str, Path],
        name: str,
        entity_fields: Optional[List[str]] = None,
        use_other_fields_as_metadata: bool = False,
        num_rows: Optional[int] = None
    ):
        logger.info(f"Starting artifact generation from {csv_path}")
        if num_rows:
            logger.info(f"Processing {num_rows} rows from CSV")
        
        # run the existing pipeline (cleans, infers schema, extracts entities)
        df = convert_csv_to_df(csv_path=csv_path, num_rows=num_rows)
        logger.info(f"CSV loaded successfully with {len(df)} rows")
        
        result = run_artifact_generation_pipeline(
            num_cores=self.num_cores,
            df=df,
            output_path=output_path,
            name=name,
            entity_fields=entity_fields,
            use_other_fields_as_metadata=use_other_fields_as_metadata,
            nlp=self.nlp,
        )

        # now compute and save embeddings in the same order as metadata
        logger.info("Starting embedding generation for metadata")
        metadata = result["metadata"]
        paths = result["paths"]
        flat_records = [
            {item["_field_name_"]: item["_canonical_entity_"]} for item in metadata
        ]
        texts = [json.dumps(r, default=str) for r in flat_records]
        embeddings = self._embed_texts(texts)
        
        logger.info(f"Saving embeddings to {paths['embeddings']}")
        np.savez_compressed(paths["embeddings"], embeddings=embeddings)

        logger.info("Artifact generation complete")
        result["embeddings"] = embeddings
        return result