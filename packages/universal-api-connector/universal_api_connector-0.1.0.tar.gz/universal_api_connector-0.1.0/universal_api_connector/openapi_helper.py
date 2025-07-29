"""
OpenAPI specification parser and helper functions.
"""
from typing import Dict, List, Any
import yaml
import json

def parse_spec(uploaded_file) -> Dict[str, Any]:
    """Parse OpenAPI specification file."""
    try:
        if uploaded_file.name.endswith('.json'):
            return json.load(uploaded_file)
        elif uploaded_file.name.endswith(('.yaml', '.yml')):    
            return yaml.safe_load(uploaded_file)
    except Exception as e:
        raise ValueError(f"Error parsing OpenAPI spec: {e}")

def parse_security(spec):
    """Parse security schemes from OpenAPI spec."""
    security_schemes = spec.get('components', {}).get('securitySchemes', {})
    security = []
    
    for scheme_name, scheme in security_schemes.items():
        scheme_type = scheme.get('type', '').lower()
        
        if scheme_type == 'apikey':
            security.append({'apiKey': scheme})
        elif scheme_type == 'oauth2':
            security.append({'oauth2': scheme})
        elif scheme_type == 'http':
            if scheme.get('scheme') == 'oauth':
                security.append({'oauth1': scheme})
            elif scheme.get('scheme') == 'basic':
                security.append({'basic': scheme})
    
    return security

def get_operations(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract operations from OpenAPI spec."""
    operations = []
    paths = spec.get('paths', {})
    for path, methods in paths.items():
        for method, details in methods.items():
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                operations.append({
                    'method': method.upper(),
                    'path': path,
                    'summary': details.get('summary', 'No summary'),
                    'operationId': details.get('operationId', f"{method}_{path}"),
                    'parameters': details.get('parameters', []),
                    'requestBody': details.get('requestBody', {})
                })
    return operations

def extract_parameters(operation: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize parameters by type (path, query, header)."""
    params = {
        'path': [],
        'query': [],
        'header': []
    }
    
    for param in operation.get('parameters', []):
        param_type = param.get('in')
        if param_type in params:
            params[param_type].append(param)
    
    return params