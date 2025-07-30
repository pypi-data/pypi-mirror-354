import spacy
import sys
import subprocess

from canonmap.utils.logger import get_logger

logger = get_logger()

def load_spacy_model(model_name: str = "en_core_web_sm"):
    try:
        return spacy.load(model_name)
    except OSError:
        logger.info(f"spaCy model '{model_name}' not found; downloading...")
        cmd = [sys.executable, "-m", "spacy", "download", model_name]
        subprocess.run(cmd, check=True)
        return spacy.load(model_name)