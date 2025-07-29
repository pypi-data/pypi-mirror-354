# Config loader
def load_config(path="deepcivics.yaml"):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No config file found at {path}. "
            f"Please generate one using generate_config_from_url()."
        )
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
