
from typing import Dict, List, Union, Set

from authlibps.constants import PROVIDER_CONFIGS


# Helper function to get supported providers
def get_supported_providers() -> List[str]:
    """
    Get a list of all supported OAuth providers.
    
    Returns:
        List[str]: List of supported provider names
    """
    provider_names = sorted(list(PROVIDER_CONFIGS.keys()))
    return provider_names


# Helper function to get provider requirements
def get_provider_requirements(provider: str) -> Dict[str, Union[str, Set[str]]]:
    """
    Get the parameter requirements for a specific provider.
    
    Args:
        provider (str): The OAuth provider name
        
    Returns:
        dict: Provider configuration requirements
        
    Raises:
        ValueError: If provider is not supported
    """
    provider = provider.lower().strip()
    
    if provider not in PROVIDER_CONFIGS:
        supported_providers = ', '.join(sorted(PROVIDER_CONFIGS.keys()))
        raise ValueError(f"Unsupported provider: '{provider}'. Supported: {supported_providers}")
    
    config = PROVIDER_CONFIGS[provider]
    return {
        'provider_type': config['type'],
        'required_parameters': config['required'],
        'optional_parameters': config.get('optional', set()),
        'defaults': config.get('defaults', {}),
        'recommended_scope': config.get('recommended_scope', ''),
        'notes': config.get('notes', '')
    }


class ProviderConfigValidationResult:
    """
        Class to encapsulate validation results for OAuth provider configurations.
        
        Attributes:
            valid (bool): Whether the configuration is valid
            missing_required (List[str]): List of missing required parameters
            missing_optional (List[str]): List of missing optional parameters
            warnings (List[str]): List of warnings related to the configuration
            provider_type (str): Type of the OAuth provider ('oauth1', 'oauth2', 'oidc')
    """
    
    def __init__(self, *, valid: bool, missing_required: List[str], 
                 missing_optional: List[str], warnings: List[str], 
                 provider_type: str):
        self.valid = valid
        self.missing_required = missing_required
        self.missing_optional = missing_optional
        self.warnings = warnings
        self.provider_type = provider_type



def validate_oauth_config(provider: str, provider_config: Dict[str, Union[str, Dict]]) -> ProviderConfigValidationResult:
    """
    Validate OAuth provider configuration against required parameters.
    
    Args:
        provider (str): The OAuth provider name (e.g., 'google', 'github', 'twitter')
        provider_config (dict): Dictionary containing the provider configuration
        
    Returns:
        dict: Validation result with structure:
            {
                'valid': bool,
                'missing_required': List[str],
                'missing_optional': List[str],
                'warnings': List[str],
                'provider_type': str  # 'oauth1', 'oauth2', or 'oidc'
            }
            
    Raises:
        ValueError: If provider is not supported

    """
    
    # Normalize provider name
    provider = provider.lower().strip()
    
    # Check if provider is supported
    if provider not in PROVIDER_CONFIGS:
        supported_providers = ', '.join(sorted(PROVIDER_CONFIGS.keys()))
        raise ValueError(f"Unsupported provider: '{provider}'. Supported providers: {supported_providers}")
    
    config = PROVIDER_CONFIGS[provider]

    valid_parameters = True,
    warnings = []
    provider_type = config['type']
    
    # Check required parameters
    config_keys = set(provider_config.keys())
    required_params = config['required']
    missing_required = sorted(list(required_params - config_keys))
    
    if missing_required:
        valid_parameters = False
    
    # Check optional parameters
    optional_params = config.get('optional', set())
    missing_optional = sorted(list(optional_params - config_keys))

    # Validate client_id and client_secret are not empty
    for param in ['client_id', 'client_secret']:
        if param in provider_config:
            value = provider_config[param]
            if not value or (isinstance(value, str) and not value.strip()):
                result['valid'] = False
                warnings.append(f"{param} is empty or contains only whitespace")
    
    # Check for scope configuration
    client_kwargs = provider_config.get('client_kwargs', {})
    recommended_scope = config.get('recommended_scope')
    
    if recommended_scope and isinstance(client_kwargs, dict):
        if 'scope' not in client_kwargs:
            warnings.append(f"No scope specified. Recommended scope: '{recommended_scope}'")
        elif not client_kwargs['scope']:
            warnings.append(f"Empty scope specified. Recommended scope: '{recommended_scope}'")
    
    # Provider-specific validations
    if provider == 'microsoft':
        # Check for tenant placeholder in URLs
        for url_param in ['access_token_url', 'authorize_url']:
            if url_param in provider_config:
                url = provider_config[url_param]
                if isinstance(url, str) and '{tenant}' in url:
                    warnings.append(f"{url_param} contains {{tenant}} placeholder - replace with actual tenant ID")
    
    elif provider == 'apple':
        # Check for JWT client_secret
        client_secret = provider_config.get('client_secret', '')
        if isinstance(client_secret, str) and not client_secret.startswith('eyJ'):
            warnings.append("Apple client_secret should be a JWT signed with your private key")
    
    elif provider == 'twitter':
        # Remind about OAuth 1.0 session management
        warnings.append("Twitter uses OAuth 1.0 - ensure proper session management for request tokens")
    
    # Check for HTTPS URLs (security best practice)
    url_params = ['access_token_url', 'authorize_url', 'request_token_url', 'server_metadata_url']
    for param in url_params:
        if param in provider_config:
            url = provider_config[param]
            if isinstance(url, str) and url.startswith('http://'):
                warnings.append(f"{param} uses HTTP instead of HTTPS - consider security implications")

    result = ProviderConfigValidationResult(valid=valid_parameters,
                                              missing_required=missing_required,
                                              missing_optional=missing_optional,
                                              warnings=warnings,
                                              provider_type=provider_type)

    return result

