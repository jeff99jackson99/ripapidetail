"""
Predefined configurations for common gated API patterns
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from .advanced_extractor import GatedAPIConfig

@dataclass
class CommonGatedAPIConfig:
    """Common gated API configurations"""
    name: str
    description: str
    config: GatedAPIConfig
    example_credentials: Dict[str, str]
    target_selectors: List[str]
    notes: str

class GatedAPIConfigManager:
    """Manager for gated API configurations"""
    
    def __init__(self):
        self.configs = self._initialize_configs()
    
    def _initialize_configs(self) -> Dict[str, CommonGatedAPIConfig]:
        """Initialize common gated API configurations"""
        configs = {}
        
        # Salesforce configuration
        configs["salesforce"] = CommonGatedAPIConfig(
            name="Salesforce",
            description="Salesforce CRM and API platform",
            config=GatedAPIConfig(
                login_url="https://login.salesforce.com/",
                username_field="username",
                password_field="pw",
                submit_button="input[type='submit']",
                success_indicator=".profile-link",
                wait_time=5
            ),
            example_credentials={
                "username": "your_email@company.com",
                "password": "your_password"
            },
            target_selectors=[
                ".api-content",
                ".endpoint-list",
                ".swagger-ui",
                "[data-api]"
            ],
            notes="Salesforce uses OAuth 2.0 and has extensive API documentation behind the login."
        )
        
        # HubSpot configuration
        configs["hubspot"] = CommonGatedAPIConfig(
            name="HubSpot",
            description="HubSpot marketing and CRM platform",
            config=GatedAPIConfig(
                login_url="https://app.hubspot.com/login",
                username_field="username",
                password_field="password",
                submit_button="button[type='submit']",
                success_indicator=".nav-container",
                wait_time=5
            ),
            example_credentials={
                "username": "your_email@company.com",
                "password": "your_password"
            },
            target_selectors=[
                ".api-docs",
                ".endpoint-container",
                "[data-testid='api-doc']",
                ".swagger-section"
            ],
            notes="HubSpot has comprehensive API documentation and developer tools behind authentication."
        )
        
        # Stripe configuration
        configs["stripe"] = CommonGatedAPIConfig(
            name="Stripe",
            description="Stripe payment processing platform",
            config=GatedAPIConfig(
                login_url="https://dashboard.stripe.com/login",
                username_field="email",
                password_field="password",
                submit_button="button[type='submit']",
                success_indicator=".dashboard-header",
                wait_time=5
            ),
            example_credentials={
                "username": "your_email@company.com",
                "password": "your_password"
            },
            target_selectors=[
                ".api-docs",
                ".endpoint-list",
                "[data-testid='api-reference']",
                ".stripe-docs"
            ],
            notes="Stripe has excellent API documentation with live examples and testing tools."
        )
        
        # Twilio configuration
        configs["twilio"] = CommonGatedAPIConfig(
            name="Twilio",
            description="Twilio communication platform",
            config=GatedAPIConfig(
                login_url="https://www.twilio.com/login",
                username_field="email",
                password_field="password",
                submit_button="button[type='submit']",
                success_indicator=".dashboard-nav",
                wait_time=5
            ),
            example_credentials={
                "username": "your_email@company.com",
                "password": "your_password"
            },
            target_selectors=[
                ".api-docs",
                ".endpoint-list",
                "[data-testid='api-reference']",
                ".twilio-docs"
            ],
            notes="Twilio provides comprehensive API documentation with code examples in multiple languages."
        )
        
        # AWS configuration
        configs["aws"] = CommonGatedAPIConfig(
            name="AWS",
            description="Amazon Web Services platform",
            config=GatedAPIConfig(
                login_url="https://signin.aws.amazon.com/",
                username_field="username",
                password_field="password",
                submit_button="input[type='submit']",
                success_indicator=".nav-menu",
                wait_time=5
            ),
            example_credentials={
                "username": "your_aws_username",
                "password": "your_aws_password"
            },
            target_selectors=[
                ".api-docs",
                ".endpoint-list",
                "[data-testid='api-reference']",
                ".aws-docs"
            ],
            notes="AWS has extensive API documentation for all services behind authentication."
        )
        
        # Google Cloud configuration
        configs["google_cloud"] = CommonGatedAPIConfig(
            name="Google Cloud",
            description="Google Cloud Platform",
            config=GatedAPIConfig(
                login_url="https://console.cloud.google.com/",
                username_field="identifier",
                password_field="password",
                submit_button="button[type='submit']",
                success_indicator=".cloud-console-header",
                wait_time=5
            ),
            example_credentials={
                "username": "your_email@gmail.com",
                "password": "your_password"
            },
            target_selectors=[
                ".api-docs",
                ".endpoint-list",
                "[data-testid='api-reference']",
                ".gcp-docs"
            ],
            notes="Google Cloud has comprehensive API documentation and client libraries."
        )
        
        # Microsoft Azure configuration
        configs["azure"] = CommonGatedAPIConfig(
            name="Microsoft Azure",
            description="Microsoft Azure cloud platform",
            config=GatedAPIConfig(
                login_url="https://portal.azure.com/",
                username_field="loginfmt",
                password_field="passwd",
                submit_button="input[type='submit']",
                success_indicator=".fxs-portal-header",
                wait_time=5
            ),
            example_credentials={
                "username": "your_email@company.com",
                "password": "your_password"
            },
            target_selectors=[
                ".api-docs",
                ".endpoint-list",
                "[data-testid='api-reference']",
                ".azure-docs"
            ],
            notes="Azure provides extensive API documentation and SDKs for all services."
        )
        
        # Custom/Generic configuration
        configs["custom"] = CommonGatedAPIConfig(
            name="Custom/Generic",
            description="Custom authentication configuration",
            config=GatedAPIConfig(
                login_url="",
                username_field="",
                password_field="",
                submit_button="",
                success_indicator="",
                wait_time=5
            ),
            example_credentials={
                "username": "your_username",
                "password": "your_password"
            },
            target_selectors=[
                ".api-content",
                ".endpoint-list",
                "[data-api]",
                ".swagger-ui"
            ],
            notes="Use this for custom authentication flows. Fill in the specific selectors and URLs."
        )
        
        return configs
    
    def get_config(self, name: str) -> CommonGatedAPIConfig:
        """Get a specific configuration by name"""
        return self.configs.get(name, self.configs["custom"])
    
    def list_configs(self) -> List[str]:
        """List all available configuration names"""
        return list(self.configs.keys())
    
    def get_config_info(self, name: str) -> Dict[str, Any]:
        """Get detailed information about a configuration"""
        config = self.get_config(name)
        return {
            "name": config.name,
            "description": config.description,
            "login_url": config.config.login_url,
            "username_field": config.config.username_field,
            "password_field": config.config.password_field,
            "submit_button": config.config.submit_button,
            "success_indicator": config.config.success_indicator,
            "target_selectors": config.target_selectors,
            "notes": config.notes
        }
    
    def create_custom_config(self, name: str, login_url: str, username_field: str,
                           password_field: str, submit_button: str, 
                           success_indicator: str = "", target_selectors: List[str] = None) -> str:
        """Create a custom configuration"""
        if target_selectors is None:
            target_selectors = [".api-content", ".endpoint-list", "[data-api]"]
        
        custom_config = CommonGatedAPIConfig(
            name=name,
            description=f"Custom configuration for {name}",
            config=GatedAPIConfig(
                login_url=login_url,
                username_field=username_field,
                password_field=password_field,
                submit_button=submit_button,
                success_indicator=success_indicator,
                wait_time=5
            ),
            example_credentials={
                "username": "your_username",
                "password": "your_password"
            },
            target_selectors=target_selectors,
            notes=f"Custom configuration for {name}. Update credentials as needed."
        )
        
        # Add to configs with a unique key
        key = f"custom_{name.lower().replace(' ', '_')}"
        self.configs[key] = custom_config
        
        return key
    
    def get_common_selectors(self) -> List[str]:
        """Get common CSS selectors for API content"""
        return [
            ".api-docs",
            ".endpoint-list",
            ".swagger-ui",
            "[data-api]",
            ".api-content",
            ".endpoint-container",
            "[data-testid='api-reference']",
            ".api-reference",
            ".endpoint-details",
            ".method-list",
            ".parameter-table",
            ".response-example"
        ]
    
    def get_authentication_patterns(self) -> Dict[str, List[str]]:
        """Get common authentication patterns"""
        return {
            "form_fields": [
                "username", "user", "email", "login", "account",
                "password", "pass", "pwd", "secret",
                "submit", "login", "signin", "authenticate"
            ],
            "success_indicators": [
                ".dashboard", ".profile", ".nav-menu", ".user-menu",
                ".main-content", ".authenticated", ".logged-in"
            ],
            "failure_indicators": [
                ".error", ".alert", ".warning", ".invalid",
                ".login-failed", ".authentication-error"
            ]
        }
