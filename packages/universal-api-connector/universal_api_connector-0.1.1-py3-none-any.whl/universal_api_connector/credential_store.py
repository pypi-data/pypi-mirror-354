"""
Credential management module for storing and retrieving API credentials.
"""
import json
from typing import Dict, Any, Optional

CREDENTIALS_FILE = 'credentials.json'

def load_credentials() -> Dict[str, Any]:
    """Load credentials from the JSON file."""
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_credentials(credentials: Dict[str, Any]) -> None:
    """Save credentials to the JSON file."""
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f, indent=2)

def get_api_credentials(api_name: str) -> Optional[Dict[str, Any]]:
    """Get credentials for a specific API."""
    return load_credentials().get(api_name)
