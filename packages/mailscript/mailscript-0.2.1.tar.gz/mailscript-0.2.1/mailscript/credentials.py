"""
Credentials loader for MailScript.

This module provides a simple way to load credentials from configuration files
while keeping sensitive information outside the package.
"""
import os
import importlib.util
from typing import Dict, Any, Optional

# Default locations to look for configuration
CONFIG_LOCATIONS = [
    os.path.join(os.getcwd(), "config", "mailscript_config.py"),
    os.path.expanduser("~/.config/mailscript/config.py"),
    os.path.join(os.getcwd(), "mailscript_config.py"),
]

# Default empty configurations
DEFAULT_SMTP_CONFIG = {
    "username": "",
    "password": "",
    "host": "smtp.example.com",
    "port": 587,
    "use_tls": True
}

DEFAULT_IMAP_CONFIG = {
    "username": "",
    "password": "",
    "host": "imap.example.com",
    "port": 993
}


def load_config() -> Dict[str, Any]:
    """
    Load configuration from available config files.
    
    Returns:
        Dict containing SMTP and IMAP configurations
    """
    smtp_config = DEFAULT_SMTP_CONFIG.copy()
    imap_config = DEFAULT_IMAP_CONFIG.copy()
    default_recipient = None
    
    # Check for custom config path from environment
    custom_config_path = os.environ.get("MAILSCRIPT_CONFIG_PATH")
    if custom_config_path and os.path.exists(custom_config_path):
        config_module = _load_module_from_path(custom_config_path)
        if config_module:
            return _extract_config_from_module(config_module, smtp_config, imap_config)
    
    # Check default locations
    for location in CONFIG_LOCATIONS:
        if os.path.exists(location):
            config_module = _load_module_from_path(location)
            if config_module:
                return _extract_config_from_module(config_module, smtp_config, imap_config)
    
    # If no config file found, return defaults
    return {
        "smtp": smtp_config,
        "imap": imap_config,
        "default_recipient": default_recipient
    }


def _load_module_from_path(path: str) -> Optional[Any]:
    """Load a Python module from a file path."""
    try:
        module_name = os.path.basename(path).replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, path)
        if not spec or not spec.loader:
            return None
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception:
        return None


def _extract_config_from_module(module, smtp_config, imap_config):
    """Extract configuration from the loaded module."""
    # Extract SMTP config
    if hasattr(module, "smtp_config"):
        for key, value in module.smtp_config.items():
            smtp_config[key] = value
            
    # Extract IMAP config
    if hasattr(module, "imap_config"):
        for key, value in module.imap_config.items():
            imap_config[key] = value
            
    # Extract default recipient
    default_recipient = getattr(module, "default_recipient", None)
    
    return {
        "smtp": smtp_config,
        "imap": imap_config,
        "default_recipient": default_recipient
    }


def get_smtp_config() -> Dict[str, Any]:
    """Get SMTP configuration."""
    return load_config()["smtp"]


def get_imap_config() -> Dict[str, Any]:
    """Get IMAP configuration."""
    return load_config()["imap"]


def get_default_recipient() -> Optional[str]:
    """Get default recipient email."""
    return load_config().get("default_recipient")
