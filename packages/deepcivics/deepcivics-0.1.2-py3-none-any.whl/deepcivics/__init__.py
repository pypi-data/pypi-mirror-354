__version__ = '0.1.0'

# --- Config and YAML ---
from .config import load_config
from .autogen import generate_config_from_url

# --- LLM Core ---
from .llm import CivicLLM

# --- Dataset handling ---
from .datasets import load_starter_config

# --- Data ingestion ---
from .ingestion import fetch_csv, preview_columns

# --- Visualization ---
from .visualization import plot_bar_count

# --- Civic messaging ---
from .civic_action import generate_email

# --- Model registry ---
from .models import get_model_name