"""
Utility functions for Universal API Connector
"""
from typing import Optional
from urllib.parse import urlparse, parse_qs
import streamlit as st

def extract_code_from_url(url: str) -> Optional[str]:
    """Extract the 'code' parameter from a URL (OAuth2)."""
    try:
        parsed = urlparse(url.strip())
        query = parse_qs(parsed.query)
        return query.get('code', [None])[0]
    except Exception:
        return None

def show_error(msg: str):
    """Show an error message in the UI."""
    st.error(msg)

def show_success(msg: str):
    """Show a success message in the UI."""
    st.success(msg)
