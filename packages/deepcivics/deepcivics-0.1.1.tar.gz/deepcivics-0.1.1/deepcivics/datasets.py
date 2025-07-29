# Load preset configs
import yaml
from pathlib import Path

def load_starter_config(domain: str, country: str) -> dict:
    domain = domain.lower()
    country = country.lower()
    path = Path(__file__).parent / "datasets" / f"{domain}.yaml"

    if not path.exists():
        raise FileNotFoundError(f"No preset file for domain: {domain}")

    with open(path, "r", encoding="utf-8") as f:
        configs = yaml.safe_load(f)

    for cfg in configs:
        if cfg['country'].lower() == country:
            return cfg

    raise ValueError(f"No dataset config found for {country} in {domain}")
