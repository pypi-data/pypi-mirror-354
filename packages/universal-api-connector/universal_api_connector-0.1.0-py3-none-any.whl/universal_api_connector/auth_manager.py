"""
Authentication management for different API auth methods.
"""
from typing import Dict, Any, Optional, Tuple
from requests_oauthlib import OAuth1
import streamlit as st
import base64
from credential_store import load_credentials, save_credentials
from utils import extract_code_from_url, show_error, show_success

def handle_api_key_auth() -> Optional[Dict[str, str]]:
    """Handle API Key authentication input."""
    key = st.text_input("API Key", type="password")
    if st.button("Save API Key"):
        return {"key": key}
    return None

def handle_bearer_token_auth() -> Optional[Dict[str, str]]:
    """Handle HTTP Bearer Token authentication input (for e.g., Twitter v2)."""
    token = st.text_input("Access Token (Bearer Token)", type="password")
    if st.button("Save Bearer Token"):
        return {"access_token": token}
    return None

def handle_oauth1_auth() -> Optional[Dict[str, str]]:
    """Handle OAuth1 authentication input."""
    with st.form("oauth1_form"):
        client_key = st.text_input("Client Key", type="password")
        client_secret = st.text_input("Client Secret", type="password")
        resource_owner_key = st.text_input("Resource Owner Key", type="password")
        resource_owner_secret = st.text_input("Resource Owner Secret", type="password")
        
        if st.form_submit_button("Save OAuth1 Credentials"):
            return {
                "client_key": client_key,
                "client_secret": client_secret,
                "resource_owner_key": resource_owner_key,
                "resource_owner_secret": resource_owner_secret
            }
    return None

import requests
from urllib.parse import urlparse, parse_qs

def _extract_code_from_url(url: str) -> Optional[str]:
    """Extract 'code' param from a URL (OAuth2)."""
    try:
        parsed = urlparse(url.strip())
        query = parse_qs(parsed.query)
        return query.get('code', [None])[0]
    except Exception:
        return None

def handle_oauth2_auth(scheme, api_name=None) -> Optional[Dict[str, str]]:
    """Universal OAuth2 UI and credential handler, spec-driven."""
    flows = scheme.get('flows', {})
    flow = next((flows[f] for f in ['authorizationCode', 'implicit', 'clientCredentials', 'password'] if f in flows), None)
    if not flow:
        show_error("No supported OAuth2 flows found in the OpenAPI spec.")
        return None
    client_id = st.text_input("Client ID", key=f"{api_name}_client_id")
    client_secret = st.text_input("Client Secret", type="password", key=f"{api_name}_client_secret")
    redirect_uri = st.text_input("Redirect URI", key=f"{api_name}_redirect_uri") if flow.get('authorizationUrl') else None
    auth_url = flow.get('authorizationUrl')
    token_url = flow.get('tokenUrl')
    if auth_url and client_id and (not redirect_uri or redirect_uri):
        url = f"{auth_url}?client_id={client_id}&response_type=code"
        if redirect_uri:
            url += f"&redirect_uri={redirect_uri}"
        st.markdown(f"[Authorize via OAuth2]({url})")
        st.caption("Open this link, authorize, and paste the FULL REDIRECTED URL you land on after authorizing.")
    redirect_response = st.text_area("Paste the full redirected URL here after authorizing:", key=f"{api_name}_redirect_response")
    save_error = None
    if st.button("Save OAuth2 Credentials"):
        code = extract_code_from_url(redirect_response)
        if not redirect_response.strip():
            save_error = "Please paste the full redirected URL before saving."
        elif not code:
            save_error = "No code found in URL."
        elif not token_url or not client_id or not client_secret:
            save_error = "Missing token endpoint or credentials."
        else:
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
            }
            if redirect_uri:
                data['redirect_uri'] = redirect_uri
            try:
                resp = requests.post(token_url, data=data, headers={'Accept': 'application/json'})
                if resp.ok:
                    tokens = resp.json()
                    show_success("Token exchange successful! Credentials saved.")
                    creds = {
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "access_token": tokens.get('access_token'),
                    }
                    if tokens.get('refresh_token'):
                        creds["refresh_token"] = tokens.get('refresh_token')
                    if redirect_uri:
                        creds["redirect_uri"] = redirect_uri
                    if token_url:
                        creds["token_url"] = token_url
                    return creds
                else:
                    save_error = f"Token exchange failed: {resp.text}"
            except Exception as e:
                save_error = f"Error exchanging code for tokens: {e}"
    if save_error:
        show_error(save_error)
    return None


def handle_basic_auth(button_label="Save Basic Auth Credentials") -> Optional[Dict[str, str]]:
    """Handle Basic authentication input (for Basic or HTTP Basic)."""
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button(button_label):
        if username and password:
            return {"username": username, "password": password}
        else:
            st.error("Both username and password are required")
    return None

def prepare_auth(credentials: Dict[str, Any]) -> Tuple[Optional[Any], Dict[str, str]]:
    """Prepare authentication for requests based on credentials."""
    auth = None
    headers = {}
    
    if 'username' in credentials and 'password' in credentials:
        # Basic auth
        auth = (credentials['username'], credentials['password'])
    elif 'key' in credentials:
        # API Key auth
        headers['Authorization'] = f"Bearer {credentials['key']}"
    elif all(key in credentials for key in ['client_key', 'client_secret', 'resource_owner_key', 'resource_owner_secret']):
        # OAuth1
        auth = OAuth1(
            credentials['client_key'],
            credentials['client_secret'],
            credentials['resource_owner_key'],
            credentials['resource_owner_secret']
        )
    elif 'access_token' in credentials:
        # OAuth2
        headers['Authorization'] = f"Bearer {credentials['access_token']}"
    
    return auth, headers

def refresh_oauth2_token(api_name, credentials, spec):
    """
    Universal OAuth2 token refresh for any API defined by OpenAPI spec.
    - api_name: The API name (as used in credentials).
    - credentials: All saved credentials (dict).
    - spec: The OpenAPI spec (dict).
    """
    try:
        api_creds = credentials.get(api_name, {})
        if not api_creds.get('refresh_token'):
            st.error("No refresh token found. Please re-authenticate.")
            return False
        # Find OAuth2 security scheme in the spec
        security_schemes = spec.get('components', {}).get('securitySchemes', {})
        oauth2_scheme = None
        token_url = None
        for scheme_name, scheme in security_schemes.items():
            if scheme.get('type') == 'oauth2':
                flows = scheme.get('flows', {})
                # Prefer 'refreshToken' or 'authorizationCode' flow
                for flow_type in ['refreshToken', 'authorizationCode', 'password', 'clientCredentials']:  # order of preference
                    flow = flows.get(flow_type)
                    if flow and flow.get('tokenUrl'):
                        oauth2_scheme = scheme
                        token_url = flow.get('tokenUrl')
                        break
            if token_url:
                break
        if not token_url:
            st.error("OAuth2 token refresh endpoint not found in API spec.")
            return False
        # Prepare client credentials
        client_id = api_creds.get('client_id') or api_creds.get('client_key')
        client_secret = api_creds.get('client_secret')
        if not client_id or not client_secret:
            st.error("Client ID/Secret missing in credentials.")
            return False
        # Prepare refresh request
        auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': api_creds['refresh_token']
        }
        # Allow for additional fields from spec if needed
        if 'scope' in api_creds:
            data['scope'] = api_creds['scope']
        response = requests.post(
            token_url,
            headers={
                'Authorization': f'Basic {auth_header}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=data
        )
        if response.status_code == 200:
            token_data = response.json()
            api_creds['access_token'] = token_data['access_token']
            if 'refresh_token' in token_data:
                api_creds['refresh_token'] = token_data['refresh_token']
            credentials[api_name] = api_creds
            save_credentials(credentials)
            st.success("Successfully refreshed access token!")
            return True
        else:
            error_msg = response.json().get('error_description', 'Failed to refresh token')
            st.error(f"Token refresh failed: {error_msg}")
            return False
    except Exception as e:
        st.error(f"Error refreshing token: {str(e)}")
        return False

def prepare_auth_from_spec(api_name: str, spec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Prepare authentication based on API spec."""
    security = spec.get('security', [])
    if not security:
        return None
    
    # Load existing credentials
    credentials = load_credentials()
    stored_creds = credentials.get(api_name, {})
    
    # Check security requirements
    for requirement in security:
        # API Key auth
        if 'apiKey' in requirement:
            return handle_api_key_auth()
        
        # Bearer Token (HTTP Bearer)
        if 'BearerToken' in requirement:
            return handle_bearer_token_auth()
        
        # OAuth 1.0
        elif 'oauth1' in requirement:
            return handle_oauth1_auth()
        
        # OAuth 2.0
        elif 'oauth2' in requirement:
            return handle_oauth2_auth()
            
        # Basic Auth
        elif 'basic' in requirement:
            return handle_basic_auth()
    
    return None
