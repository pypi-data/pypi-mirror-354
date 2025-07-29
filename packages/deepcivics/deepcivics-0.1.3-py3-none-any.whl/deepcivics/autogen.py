# Auto-generate YAML from URL
import pandas as pd
import yaml
from urllib.parse import urlparse
import os

def infer_domain_from_keywords(columns):
    keywords = {
        "Health": ["death", "hospital", "case", "vaccin"],
        "Financial": ["income", "revenue", "budget", "expenditure", "cost"],
        "Environmental": ["pollution", "pm2", "co2", "climate", "temperature"],
        "Industrial Safety": ["fire", "incident", "accident", "safety", "injury"]
    }
    for domain, terms in keywords.items():
        for col in columns:
            for term in terms:
                if term.lower() in col.lower():
                    return domain
    return "Unknown"

def generate_config_from_url(csv_url: str, country: str = "Unknown", save_path="deepcivics.yaml") -> str:
    try:
        df = pd.read_csv(csv_url)
    except Exception as e:
        raise RuntimeError(f"Failed to load CSV: {e}")

    columns = df.columns.tolist()[:5]
    domain = infer_domain_from_keywords(columns)
    parsed_url = urlparse(csv_url)
    dataset_name = os.path.basename(parsed_url.path).replace(".csv", "").replace("_", " ").title()

    config = {
        "dataset_name": dataset_name,
        "continent": "Unknown",
        "country": country,
        "domain": domain,
        "source": csv_url,
        "language": "en",
        "columns_of_interest": columns,
        "model": "deepset/xlm-roberta-base-squad2",
        "truncate_context": 4000
    }

    with open(save_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f)

    return f"✅ Config generated at {save_path}\n🧠 Domain: {domain}\n📊 Columns: {columns}"
