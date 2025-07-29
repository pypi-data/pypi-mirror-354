# 🏛️ Deep Civics

> Open Data + Policy Tools for the People 

Deep Civics helps you turn public data into civic insight for the Public, Policy makers and Investment professionals.

It's an open-source Python library and Jupyter interface to let anyone:

- 🗂️ Load and analyze public datasets
- 💬 Ask questions in your language using an LLM
- 📊 Visualize trends, disparities, and impacts
- 🧭 Share findings or use it your applications

## 🌍 Example Use Cases

- 📉 Understand budget allocation by region
- 🌡️ Compare climate or emissions data over time
- 🏥 Track healthcare data by district
- 🏭 Explore industrial safety or infrastructure trends
- 🏦 Monitor financial and digital inclusion metrics

## Quickstart

Let’s use Deep Civics to explore how South Africa has improved **digital financial access** over time, using World Bank data.

```bash
pip install deepcivics

```
```bash
from deepcivics import generate_config_from_url

# Use a real CSV from the World Bank
generate_config_from_url(
    csv_url="https://databankfiles.worldbank.org/public/ddpext_download/ICT/Series/FS.DSR.DIGS.ZS.csv",
    country="South Africa"
)

from deepcivics import CivicLLM
from deepcivics.config import load_config
from deepcivics import ingestion

cfg = load_config()
df = ingestion.fetch_csv(cfg["source"])

llm = CivicLLM(cfg["model"])
context = df.to_csv(index=False)[:cfg["truncate_context"]]
question = "Which countries in Africa have improved digital finance access the most?"
answer = llm.ask(question, context)
print("✅ LLM Answer:", answer)
```



##📓 Try in Your Browser

[![Launch on Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pkbythebay29/deepcivics/HEAD?filepath=notebooks%2Fdigital_finance_africa_real.ipynb)


##🧠 Architecture

    deepcivics/ – Core Python package

    notebooks/ – Civic data demos

    datasets/ – YAML registry of reusable datasets

    docs/ – GitHub Pages documentation
	
##🤝 Contributing

Y'all are welcome to contribute and provide feedback via PR!

##📜 License

MIT. Use freely, cite responsibly, act respectfully.