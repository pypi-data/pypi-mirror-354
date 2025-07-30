# app/services/artifact_generator.py

import multiprocessing
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Union

import spacy

from app.services._from_csv_helper import convert_csv_to_df
from app.services._run_pipeline import run_artifact_generation_pipeline
from app.utils.context._set_logger import set_logger

class ArtifactGenerator:
    def __init__(
        self,
        nlp,
    ):
        self.logger = set_logger()
        self.num_cores = multiprocessing.cpu_count()
        self.logger.info(f"Detected {self.num_cores} CPU cores for parallel processing.")
        self.nlp = nlp

    def generate_artifacts_from_csv(
        self,
        csv_path: str,
        output_path: Union[str, Path],
        name: str,
        entity_fields: Optional[List[str]] = None,
        use_other_fields_as_metadata: bool = False,
        num_rows: Optional[int] = None
    ):
        df = convert_csv_to_df(logger=self.logger, csv_path=csv_path, num_rows=num_rows)
        return run_artifact_generation_pipeline(
            logger=self.logger,
            num_cores=self.num_cores,
            df=df,
            output_path=output_path,
            name=name,
            entity_fields=entity_fields,
            use_other_fields_as_metadata=use_other_fields_as_metadata,
            nlp=self.nlp,
        )

    