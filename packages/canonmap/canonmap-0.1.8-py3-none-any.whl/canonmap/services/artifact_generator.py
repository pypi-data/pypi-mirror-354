# canonmap/services/artifact_generator.py

from pathlib import Path
from typing import List, Optional, Union

import spacy

from canonmap.utils.get_cpu_count import get_cpu_count
from canonmap.utils.load_spacy_model import load_spacy_model
from canonmap.services._from_csv_helper import convert_csv_to_df
from canonmap.services._run_pipeline import run_artifact_generation_pipeline

class ArtifactGenerator:
    def __init__(
        self,
        nlp: Optional[spacy.Language] = None,
    ):
        self.num_cores = get_cpu_count()
        self.nlp = nlp or load_spacy_model()

    def generate_artifacts_from_csv(
        self,
        csv_path: str,
        output_path: Union[str, Path],
        name: str,
        entity_fields: Optional[List[str]] = None,
        use_other_fields_as_metadata: bool = False,
        num_rows: Optional[int] = None
    ):
        df = convert_csv_to_df(csv_path=csv_path, num_rows=num_rows)
        return run_artifact_generation_pipeline(
            num_cores=self.num_cores,
            df=df,
            output_path=output_path,
            name=name,
            entity_fields=entity_fields,
            use_other_fields_as_metadata=use_other_fields_as_metadata,
            nlp=self.nlp,
        )

    