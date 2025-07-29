from deepcivics.config import load_config
import yaml

def test_config_loader_reads_yaml(tmp_path):
    config_file = tmp_path / "test.yaml"
    config_file.write_text("model: english_default")
    cfg = load_config(str(config_file))
    assert cfg["model"] == "english_default"
