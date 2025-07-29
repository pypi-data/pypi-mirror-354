import yaml
import os
from pathlib import Path

def load_model_registry(path: str = None) -> dict:
    """Load model registry from models.yaml"""
    path = path or Path(__file__).parent / "models.yaml"
    if not os.path.exists(path):
        raise FileNotFoundError("models.yaml not found in deepcivics package")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_model_name(alias_or_fullname: str) -> str:
    """
    Return a full model name from a preset alias, or accept full names directly.
    """
    registry = load_model_registry()

    if alias_or_fullname in registry:
        return registry[alias_or_fullname]
    else:
        return alias_or_fullname  # Assume user passed a full model name
