
from typing import Any, Dict

PROVIDER_CONFIGS : Dict[str, Any] = {
        'google': {
            'type': 'oidc',
            'required': {'client_id', 'client_secret'},
            'optional': {'server_metadata_url', 'client_kwargs'},
            'defaults': {
                'server_metadata_url': 'https://accounts.google.com/.well-known/openid-configuration'
            },
            'recommended_scope': 'openid email profile'
        },
        'github': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs'},
            'defaults': {
                'access_token_url': 'https://github.com/login/oauth/access_token',
                'authorize_url': 'https://github.com/login/oauth/authorize',
                'api_base_url': 'https://api.github.com/'
            },
            'recommended_scope': 'user:email'
        },
        'twitter': {
            'type': 'oauth1',
            'required': {'client_id', 'client_secret', 'request_token_url', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs'},
            'defaults': {
                'request_token_url': 'https://api.twitter.com/oauth/request_token',
                'access_token_url': 'https://api.twitter.com/oauth/access_token',
                'authorize_url': 'https://api.twitter.com/oauth/authenticate',
                'api_base_url': 'https://api.twitter.com/1.1/'
            }
        },
        'facebook': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs', 'compliance_fix'},
            'defaults': {
                'access_token_url': 'https://graph.facebook.com/oauth/access_token',
                'authorize_url': 'https://www.facebook.com/dialog/oauth',
                'api_base_url': 'https://graph.facebook.com/'
            },
            'recommended_scope': 'email'
        },
        'microsoft': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs'},
            'defaults': {
                'api_base_url': 'https://graph.microsoft.com/'
            },
            'recommended_scope': 'openid email profile',
            'notes': 'Replace {tenant} in URLs with your tenant ID'
        },
        'apple': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'client_kwargs', 'token_endpoint_auth_method'},
            'defaults': {
                'access_token_url': 'https://appleid.apple.com/auth/token',
                'authorize_url': 'https://appleid.apple.com/auth/authorize',
                'token_endpoint_auth_method': 'client_secret_post'
            },
            'recommended_scope': 'email name'
        },
        'linkedin': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs'},
            'defaults': {
                'access_token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
                'authorize_url': 'https://www.linkedin.com/oauth/v2/authorization',
                'api_base_url': 'https://api.linkedin.com/'
            },
            'recommended_scope': 'r_liteprofile r_emailaddress'
        },
        'discord': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs'},
            'defaults': {
                'access_token_url': 'https://discord.com/api/oauth2/token',
                'authorize_url': 'https://discord.com/api/oauth2/authorize',
                'api_base_url': 'https://discord.com/api/'
            },
            'recommended_scope': 'identify email'
        },
        'slack': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs', 'compliance_fix'},
            'defaults': {
                'access_token_url': 'https://slack.com/api/oauth.v2.access',
                'authorize_url': 'https://slack.com/oauth/v2/authorize',
                'api_base_url': 'https://slack.com/api/'
            },
            'recommended_scope': 'users:read'
        },
        'dropbox': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs'},
            'defaults': {
                'access_token_url': 'https://api.dropbox.com/oauth2/token',
                'authorize_url': 'https://www.dropbox.com/oauth2/authorize',
                'api_base_url': 'https://api.dropbox.com/'
            },
            'recommended_scope': 'account_info.read'
        },
        'reddit': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs', 'token_endpoint_auth_method'},
            'defaults': {
                'access_token_url': 'https://www.reddit.com/api/v1/access_token',
                'authorize_url': 'https://www.reddit.com/api/v1/authorize',
                'api_base_url': 'https://oauth.reddit.com/',
                'token_endpoint_auth_method': 'client_secret_basic'
            },
            'recommended_scope': 'identity'
        },
        'gitlab': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs'},
            'defaults': {
                'access_token_url': 'https://gitlab.com/oauth/token',
                'authorize_url': 'https://gitlab.com/oauth/authorize',
                'api_base_url': 'https://gitlab.com/api/v4/'
            },
            'recommended_scope': 'read_user'
        },
        'spotify': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs', 'token_endpoint_auth_method'},
            'defaults': {
                'access_token_url': 'https://accounts.spotify.com/api/token',
                'authorize_url': 'https://accounts.spotify.com/authorize',
                'api_base_url': 'https://api.spotify.com/',
                'token_endpoint_auth_method': 'client_secret_basic'
            },
            'recommended_scope': 'user-read-email user-read-private'
        },
        'twitch': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs'},
            'defaults': {
                'access_token_url': 'https://id.twitch.tv/oauth2/token',
                'authorize_url': 'https://id.twitch.tv/oauth2/authorize',
                'api_base_url': 'https://api.twitch.tv/helix/'
            },
            'recommended_scope': 'user:read:email'
        },
        'instagram': {
            'type': 'oauth2',
            'required': {'client_id', 'client_secret', 'access_token_url', 'authorize_url'},
            'optional': {'api_base_url', 'client_kwargs'},
            'defaults': {
                'access_token_url': 'https://api.instagram.com/oauth/access_token',
                'authorize_url': 'https://api.instagram.com/oauth/authorize',
                'api_base_url': 'https://graph.instagram.com/'
            },
            'recommended_scope': 'user_profile,user_media'
    }
}
