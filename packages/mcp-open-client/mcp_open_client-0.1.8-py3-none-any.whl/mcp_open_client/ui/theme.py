# Theme UI components

from nicegui import ui
from mcp_open_client import state
import json
import os
from datetime import datetime

# Global reference to the CSS editor
css_editor = None

def render_theme_page(container):
    """Renders the theme page with CSS editor"""
    with container:
        # Page header with save button
        with ui.row().classes('app-flex-row app-full-width app-space-between'):
            ui.label('Tema').classes('app-page-title')
            ui.button('Guardar cambios', icon='save', on_click=lambda: save_theme_changes()).classes('app-primary-button')
        
        ui.separator().classes('app-separator')
        
        # Theme editor card
        with ui.card().classes('app-card'):
            with ui.row().classes('app-card-header app-custom-header'):
                ui.label('Editor de Tema CSS').classes('app-card-title')
                ui.icon('brush').classes('app-icon-large')
            
            with ui.column().classes('app-container'):
                ui.label('Edite los estilos globales de la aplicación:').classes('app-form-label')
                
                # Get current theme CSS or use default
                current_css = get_current_theme_css()
                
                # CSS code editor
                global css_editor
                css_editor = ui.codemirror(
                    current_css,
                    language='css',
                    theme='basicLight',
                    line_wrapping=True
                ).classes('app-code-editor app-editor-large')
                
                # Preview section
                ui.label('Vista previa:').classes('app-section-title')
                
                # Preview container with live update button
                with ui.row().classes('app-flex-row app-full-width app-space-between'):
                    ui.label('Vea cómo se verán los cambios').classes('app-help-text')
                    ui.button('Actualizar vista previa', icon='refresh',
                             on_click=lambda: update_preview(css_editor.value)).classes('app-secondary-button')
                
                # Preview area
                preview_container = ui.column().classes('app-preview-container')
                
                # Initial preview
                with preview_container:
                    create_preview_elements()
                
                # Function to update preview
                def update_preview(css_content):
                    preview_container.clear()
                    
                    # Add the CSS to the preview
                    ui.html(f'<style>{css_content}</style>')
                    
                    # Create preview elements
                    with preview_container:
                        create_preview_elements()
                    
                    ui.notify('Vista previa actualizada')

def create_preview_elements():
    """Creates preview elements to show theme changes"""
    ui.label('Elementos de muestra').classes('app-preview-title')
    
    # Sample buttons
    with ui.row().classes('app-preview-row'):
        ui.button('Botón primario').classes('app-primary-button')
        ui.button('Botón secundario').classes('app-secondary-button')
        ui.button('Botón normal').classes('app-button')
    
    # Sample cards
    with ui.row().classes('app-preview-row'):
        with ui.card().classes('app-preview-card'):
            ui.label('Tarjeta de ejemplo').classes('app-card-title')
            ui.label('Contenido de la tarjeta').classes('app-card-content')
        
        with ui.card().classes('app-preview-card app-primary-card'):
            ui.label('Tarjeta primaria').classes('app-card-title')
            ui.label('Contenido de la tarjeta').classes('app-card-content')
    
    # Sample form elements
    with ui.column().classes('app-preview-form'):
        ui.label('Elementos de formulario:').classes('app-form-label')
        ui.input(label='Campo de texto').classes('app-input')
        ui.select(['Opción 1', 'Opción 2', 'Opción 3'], label='Selector').classes('app-select')
        ui.checkbox('Casilla de verificación').classes('app-checkbox')

def get_current_theme_css():
    """Gets the current theme CSS from file or returns default"""
    try:
        print("DEBUG: get_current_theme_css() called")
        
        # First check user's home directory
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".mcp-open-client", "config")
        user_theme_path = os.path.join(config_dir, "user_theme.css")
        
        print(f"DEBUG: Checking user theme path: {user_theme_path}")
        print(f"DEBUG: User theme exists: {os.path.exists(user_theme_path)}")
        
        # If theme exists in user's directory, use it
        if os.path.exists(user_theme_path):
            print("DEBUG: Loading user theme file")
            with open(user_theme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"DEBUG: User theme loaded, length: {len(content)} characters")
                return content
        
        # If not in user's directory, check application settings directory
        app_theme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings", "default_theme.css")
        
        print(f"DEBUG: Checking app theme path: {app_theme_path}")
        print(f"DEBUG: App theme exists: {os.path.exists(app_theme_path)}")
        
        if os.path.exists(app_theme_path):
            print("DEBUG: Loading app default theme file")
            with open(app_theme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"DEBUG: App theme loaded, length: {len(content)} characters")
                return content
        
        # If neither exists, raise an error - the default theme must exist in settings directory
        print("DEBUG: No theme files found!")
        raise FileNotFoundError("No se encontró el archivo de tema por defecto en settings/default_theme.css")
    except Exception as e:
        print(f"DEBUG: Error in get_current_theme_css: {str(e)}")
        ui.notify(f"Error al cargar el tema: {str(e)}", type='negative')
        return "/* Error al cargar el tema. Aquí puede escribir su CSS personalizado. */"

async def save_theme_changes():
    """Saves the theme CSS to file and applies it"""
    try:
        global css_editor
        
        # Get the CSS content from the editor instance
        if css_editor:
            css_content = css_editor.value
        else:
            # Fallback in case the editor reference is not available
            ui.notify("Error: No se pudo acceder al editor", type='negative')
            return
        
        # Use user's home directory with ~/.mcp-open-client/config/
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".mcp-open-client", "config")
        
        # Create directory if it doesn't exist
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
        
        # Save CSS directly to file
        theme_path = os.path.join(config_dir, "user_theme.css")
        
        with open(theme_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        # Apply the CSS to the current page
        ui.run_javascript(f'''
            const styleElement = document.getElementById('custom-theme-style');
            if (styleElement) {{
                styleElement.textContent = `{css_content}`;
            }} else {{
                const newStyle = document.createElement('style');
                newStyle.id = 'custom-theme-style';
                newStyle.textContent = `{css_content}`;
                document.head.appendChild(newStyle);
            }}
        ''')
        
        ui.notify('Tema guardado y aplicado correctamente', type='positive')
    except Exception as e:
        ui.notify(f"Error al guardar el tema: {str(e)}", type='negative')

def apply_theme():
    """Applies the saved theme CSS to the page"""
    try:
        print("DEBUG: apply_theme() called")
        
        # Get the theme CSS from CSS file (this will check both user and app directories)
        css_content = get_current_theme_css()
        print(f"DEBUG: CSS content loaded, length: {len(css_content)} characters")
        print(f"DEBUG: CSS content preview (first 200 chars): {css_content[:200]}...")
        
        # Apply it using JavaScript
        js_code = f'''
            console.log("DEBUG: JavaScript theme application starting");
            const styleElement = document.getElementById('custom-theme-style');
            if (styleElement) {{
                console.log("DEBUG: Found existing style element, updating content");
                styleElement.textContent = `{css_content}`;
            }} else {{
                console.log("DEBUG: Creating new style element");
                const newStyle = document.createElement('style');
                newStyle.id = 'custom-theme-style';
                newStyle.textContent = `{css_content}`;
                document.head.appendChild(newStyle);
                console.log("DEBUG: New style element added to head");
            }}
            console.log("DEBUG: JavaScript theme application completed");
        '''
        
        print("DEBUG: About to execute JavaScript for theme application")
        ui.run_javascript(js_code)
        
        # Log success
        print("DEBUG: Theme applied successfully")
    except Exception as e:
        print(f"DEBUG: Error applying theme: {str(e)}")
        import traceback
        print(f"DEBUG: Full traceback: {traceback.format_exc()}")