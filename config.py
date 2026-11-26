
import os
from pathlib import Path

from dotenv import load_dotenv


# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Load local .env file.
# Existing environment variables are not overwritten.
load_dotenv(BASE_DIR / ".env", override=False)


def load_streamlit_secrets():
    """Load API keys from Streamlit Cloud Secrets when available."""
    try:
        import streamlit as st

        for key in ("GROQ_API_KEY", "TAVILY_API_KEY"):
            if not os.getenv(key) and key in st.secrets:
                os.environ[key] = str(st.secrets[key])

    except Exception:
        # Streamlit Secrets may not exist when running locally.
        pass


def get_required_env(key: str) -> str:
    """Return a required environment variable or raise a clear error."""
    load_streamlit_secrets()

    value = os.getenv(key)

    if not value:
        raise RuntimeError(
            f"Missing {key}. Add it to your local .env file "
            "or Streamlit Cloud Secrets."
        )

    return value


# Load Streamlit Secrets when this module is imported.
load_streamlit_secrets()
