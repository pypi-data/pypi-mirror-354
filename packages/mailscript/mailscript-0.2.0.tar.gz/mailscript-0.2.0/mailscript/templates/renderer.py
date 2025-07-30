"""
Template rendering implementation for MailScript.

This module provides the TemplateRenderer class for rendering templates with Jinja2.
"""

try:
    import jinja2
except ImportError:
    raise ImportError(
        "The jinja2 package is required for template rendering. "
        "Please install it with: pip install jinja2"
    )

from typing import Dict, Any, Optional, Callable, Union


class TemplateRenderer:
    """
    A template renderer class using Jinja2.
    
    This class provides methods to render templates from strings or files,
    with support for custom filters and global variables.
    """
    
    def __init__(self, template_folder: Optional[str] = None):
        """
        Initialize a new TemplateRenderer instance.
        
        Args:
            template_folder: Path to template folder (optional)
        """
        # Create Jinja2 environment
        if template_folder:
            self.env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(template_folder),
                autoescape=True
            )
        else:
            self.env = jinja2.Environment(autoescape=True)
            
    def add_filter(self, name: str, func: Callable) -> None:
        """
        Add a custom filter to the template environment.
        
        Args:
            name: Name of the filter
            func: Filter function
        """
        self.env.filters[name] = func
        
    def add_global(self, name: str, value: Any) -> None:
        """
        Add a global variable to the template environment.
        
        Args:
            name: Variable name
            value: Variable value
        """
        self.env.globals[name] = value
        
    def render_from_string(
        self, 
        template_string: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render a template from a string.
        
        Args:
            template_string: Template string to render
            context: Template context variables (optional)
            
        Returns:
            str: Rendered template
        """
        template = self.env.from_string(template_string)
        return template.render(**(context or {}))
        
    def render_from_file(
        self, 
        template_name: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render a template from a file.
        
        Args:
            template_name: Name of the template file
            context: Template context variables (optional)
            
        Returns:
            str: Rendered template
            
        Raises:
            jinja2.exceptions.TemplateNotFound: If template file not found
        """
        template = self.env.get_template(template_name)
        return template.render(**(context or {}))
