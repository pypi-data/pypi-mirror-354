import streamlit as st
import requests
import json
from typing import Dict, Any, Optional

from openapi_helper import parse_spec, get_operations, parse_security
from credential_store import load_credentials, save_credentials
from auth_manager import handle_api_key_auth, handle_oauth1_auth, handle_oauth2_auth, handle_basic_auth, prepare_auth, prepare_auth_from_spec, refresh_oauth2_token
from utils import show_error, show_success

def render_operation_form(operation: Dict[str, Any], api_name: str) -> Optional[Dict[str, Any]]:
    """Render form for operation parameters and execute request."""
    st.write(f"**Method:** {operation['method']}")
    st.write(f"**Path:** {operation['path']}")
    st.write(f"**Summary:** {operation['summary']}")
    credentials = load_credentials()
    stored_creds = credentials.get(api_name, {})

    def param_widget(param, widget_key_prefix):
        name = param.get('name')
        typ = param.get('schema', {}).get('type', 'string')
        required = param.get('required', False)
        help_text = param.get('description', '')
        label = name + (" *" if required else "")
        key = f"{widget_key_prefix}_{name}_{operation['method']}_{operation['path']}"
        if typ == 'integer':
            return st.number_input(label, step=1, key=key, help=help_text)
        elif typ == 'number':
            return st.number_input(label, key=key, help=help_text)
        elif typ == 'boolean':
            return st.checkbox(label, key=key, help=help_text)
        else:
            placeholder = "Required" if required else "Optional"
            return st.text_input(label, key=key, help=help_text, placeholder=placeholder)

    params = {}
    if operation['parameters']:
        path_params = [p for p in operation['parameters'] if p.get('in') == 'path']
        if path_params:
            st.subheader("🔑 Path Parameters (Required)")
            for param in path_params:
                value = param_widget(param, "path")
                if value:
                    params[param['name']] = value
        query_params = [p for p in operation['parameters'] if p.get('in') == 'query']
        if query_params:
            st.subheader("🔍 Query Parameters")
            for param in query_params:
                if param.get('name') == 'key' and 'key' in stored_creds:
                    params[param['name']] = stored_creds['key']
                else:
                    value = param_widget(param, "query")
                    if value or param.get('required', False):
                        params[param['name']] = value
    else:
        st.info("No parameters required for this operation.")

    request_body = {}
    if operation.get('requestBody'):
        st.subheader("Request Body")
        content_type = next(iter(operation['requestBody'].get('content', {})), 'application/json')
        if content_type == 'application/json':
            json_str = st.text_area("JSON Body", "{}", key=f"{operation['method']}_{operation['path']}_body_input")
            try:
                request_body = json.loads(json_str)
            except json.JSONDecodeError:
                show_error("Invalid JSON")
                return None
    return {"params": params, "body": request_body}

def execute_request(operation, inputs, spec, api_name):
    """Execute an API request based on the operation and inputs."""
    # Load credentials
    credentials = load_credentials()
    if api_name not in credentials or not credentials[api_name]:
        st.warning(f"No credentials found for {api_name}. Please enter credentials as required by the API spec.")
        # Always show the credential input UI, do not return before displaying it
        new_creds = prepare_auth_from_spec(api_name, spec)
        if new_creds:
            credentials[api_name] = new_creds
            save_credentials(credentials)
            st.success("Credentials saved. Please re-run the request.")
        else:
            st.info("Waiting for credentials input...")
        # Always return after displaying the UI, so the input box is visible
        return
    # Set up authentication
    auth = None
    headers = {}
    api_creds = credentials[api_name]
    auth, headers = prepare_auth(api_creds)
    try:
        # Load credentials
        credentials = load_credentials()
        if api_name not in credentials:
            st.error(f"No credentials found for {api_name}")
            return
        
        # Get base URL from spec
        base_url = spec.get('servers', [{}])[0].get('url', '')
        
        # Build URL
        path = operation['path']
        for param_name, param_value in inputs['params'].items():
            path = path.replace(f"{{{param_name}}}", str(param_value))
        
        url = f"{base_url}{path}"
        
        # Set up authentication
        auth = None
        headers = {}
        if api_name in credentials:
            api_creds = credentials[api_name]
            # Handle basic auth
            if 'username' in api_creds and 'password' in api_creds:
                auth = (api_creds['username'], api_creds['password'])
            else:
                # Handle other auth types (OAuth, API Key)
                auth, headers = prepare_auth(api_creds)
        
        # Extract query parameters and body
        query_params = {}
        body_params = inputs.get('body')
        
        # Only send JSON body for POST/PUT/PATCH, never for GET/DELETE
        method = operation['method'].upper()
        req_kwargs = dict(
            method=method,
            url=url,
            headers=headers,
            params=query_params,
            auth=auth
        )
        if method in ('POST', 'PUT', 'PATCH') and body_params:
            req_kwargs['json'] = body_params
        # Debug logging (redact sensitive info)
        debug_headers = dict(headers)
        if 'Authorization' in debug_headers:
            if debug_headers['Authorization'].startswith('Bearer '):
                debug_headers['Authorization'] = 'Bearer ***'
            else:
                debug_headers['Authorization'] = '***'
        st.code(f"Request URL: {url}\nHeaders: {debug_headers}\nParams: {query_params}\nBody: {body_params if method in ('POST', 'PUT', 'PATCH') else None}", language='text')
        response = requests.request(**req_kwargs)
        
        # Universal OAuth2 token refresh/retry logic for any API (no hardcoding)
        if response.status_code in [401, 403]:
            # Detect if OAuth2 is used for this API
            security_schemes = spec.get('components', {}).get('securitySchemes', {})
            uses_oauth2 = any(
                scheme.get('type') == 'oauth2'
                for scheme in security_schemes.values()
            )
            if uses_oauth2:
                st.info("Access token may be expired. Attempting to refresh token...")
                if refresh_oauth2_token(api_name, credentials, spec):
                    credentials = load_credentials()  # Reload to get new token
                    new_token = credentials.get(api_name, {}).get('access_token')
                    if new_token:
                        headers['Authorization'] = f"Bearer {new_token}"
                    response = requests.request(
                        method=operation['method'],
                        url=url,
                        params=query_params,
                        json=body_params if method in ('POST', 'PUT', 'PATCH') else None,
                        headers=headers,
                        auth=auth
                    )
                    if response.status_code in [401, 403]:
                        st.error("Still getting authorization error after token refresh. Please try re-authenticating.")
                else:
                    st.error("Token refresh failed. Please re-authenticate.")
            else:
                st.error("Authorization error. Please check credentials or re-authenticate.")
        # Display response
        st.subheader("Response")
        st.write(f"Status: {response.status_code}")
        # (If you want a universal token info display, let me know!)
        try:
            st.json(response.json())
        except Exception:
            st.text(response.text)
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

def main():
    """Main function for the Streamlit app."""
    st.title("Universal API Connector")
    
    # File uploader
    st.header("Upload OpenAPI Specification")
    # Track uploaded file and API name in session state
    if 'last_uploaded_filename' not in st.session_state:
        st.session_state['last_uploaded_filename'] = None
    if 'api_name' not in st.session_state:
        st.session_state['api_name'] = ''

    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=['json', 'yaml', 'yml'],
        help="Limit 200MB per file"
    )
    # Reset API name when a new file is uploaded
    if uploaded_file and uploaded_file.name != st.session_state['last_uploaded_filename']:
        st.session_state['last_uploaded_filename'] = uploaded_file.name
        st.session_state['api_name'] = ''

    if not uploaded_file:
        return
    
    # Parse OpenAPI spec
    try:
        spec = parse_spec(uploaded_file)
        security = parse_security(spec)
    except Exception as e:
        st.error(f"Error parsing specification: {e}")
        return
    
    # Get API name
    api_name = st.text_input("Enter API Name", key="api_name_input", value=st.session_state['api_name'])
    st.session_state['api_name'] = api_name
    if not api_name:
        return
    credentials = load_credentials()
    if api_name not in credentials:
        # Check OpenAPI spec for auth type
        security_schemes = spec.get('components', {}).get('securitySchemes', {})
        # Pick the first security scheme (most APIs only have one)
        if security_schemes:
            scheme = next(iter(security_schemes.values()))
            scheme_type = scheme.get('type', '').lower()
            scheme_name = next(iter(security_schemes.keys()))
            st.subheader(f"Please provide credentials for {api_name}")
            auth_result = None
            if scheme_type == 'http' and scheme.get('scheme') == 'basic':
                auth_result = handle_basic_auth()
            elif scheme_type == 'apikey':
                auth_result = handle_api_key_auth()
            elif scheme_type == 'oauth2':
                auth_result = handle_oauth2_auth(scheme, api_name)
            # Add more handlers here if needed
            if auth_result:
                credentials[api_name] = auth_result
                save_credentials(credentials)
                st.success("Credentials saved!")
                st.experimental_rerun()
            else:
                st.stop()
        else:
            st.warning("No supported authentication scheme found in spec.")
            st.stop()
    else:
        # Credentials exist, show operations
        operations = get_operations(spec)
        if not operations:
            st.warning("No operations found in the API specification.")
            return
        st.subheader("Available Operations")
        operation_names = [f"{op['method']} {op['path']} - {op['summary']}" for op in operations]
        selected_op_index = st.selectbox("Select Operation", range(len(operation_names)), format_func=lambda x: operation_names[x])
        selected_op = operations[selected_op_index]
        inputs = render_operation_form(selected_op, api_name)
        if inputs and st.button("Execute", key=f"{selected_op['method']}_{selected_op['path']}_execute"):
            execute_request(selected_op, inputs, spec, api_name)

if __name__ == "__main__":
    main()
