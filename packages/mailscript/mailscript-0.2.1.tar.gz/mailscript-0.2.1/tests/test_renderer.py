"""
Test module for the mailscript.templates.renderer module.
"""
import pytest
from mailscript.templates import TemplateRenderer

@pytest.fixture
def renderer():
    """Create a TemplateRenderer instance for testing."""
    return TemplateRenderer()

def test_render_from_string(renderer):
    """Test rendering a template from a string."""
    template = "Hello, {{ name }}!"
    context = {"name": "World"}
    
    result = renderer.render_from_string(template, context)
    
    assert result == "Hello, World!"

def test_render_with_filter(renderer):
    """Test rendering with a custom filter."""
    def uppercase(value):
        return value.upper()
    
    renderer.add_filter("uppercase", uppercase)
    
    template = "{{ name | uppercase }}"
    context = {"name": "world"}
    
    result = renderer.render_from_string(template, context)
    
    assert result == "WORLD"

def test_render_with_global(renderer):
    """Test rendering with a global variable."""
    renderer.add_global("app_name", "MailScript")
    
    template = "Welcome to {{ app_name }}!"
    
    result = renderer.render_from_string(template)
    
    assert result == "Welcome to MailScript!"

def test_html_template(renderer):
    """Test rendering an HTML template."""
    html_template = """
    <html>
    <body>
        <h1>Hello, {{ name }}!</h1>
        <p>This is a test email.</p>
    </body>
    </html>
    """
    
    context = {"name": "User"}
    
    result = renderer.render_from_string(html_template, context)
    
    assert "<h1>Hello, User!</h1>" in result
