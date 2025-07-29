from deepcivics.autogen import generate_config_from_url

def test_generate_config_creates_yaml(tmp_path):
    out_file = tmp_path / "test_config.yaml"
    url = "https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
    result = generate_config_from_url(url, country="Testland", save_path=str(out_file))
    assert out_file.exists()
    assert "✅" in result
