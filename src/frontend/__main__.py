"""Entry point for running the Streamlit frontend."""

import sys
import os

# Add the parent directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit.web.cli as stcli

if __name__ == "__main__":
    # Run Streamlit app
    sys.argv = ["streamlit", "run", os.path.join(os.path.dirname(__file__), "app.py")]
    stcli.main()