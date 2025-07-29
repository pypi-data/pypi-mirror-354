from nicegui import ui
import json

def generate_preview(schema):
    """
    Generates UI elements based on the given JSON schema.
    
    Args:
        schema (dict): The JSON schema to generate UI elements from.
    
    Returns:
        list: A list of UI elements.
    """
    elements = []
    for name, props in schema.get('properties', {}).items():
        if props['type'] == 'string':
            elements.append(ui.input(label=name, placeholder=props.get('description', '')))
        elif props['type'] == 'number':
            elements.append(ui.number(label=name, placeholder=props.get('description', '')))
        elif props['type'] == 'boolean':
            elements.append(ui.checkbox(label=name, text=props.get('description', '')))
    return elements

def update_preview(schema, container):
    """
    Updates the preview container with UI elements based on the given JSON schema.
    
    Args:
        schema (dict): The JSON schema to generate UI elements from.
        container (ui.column): The container to update with the new UI elements.
    """
    container.clear()
    elements = generate_preview(schema)
    for element in elements:
        container.add(element)

def toggle_preview(json_editor, preview_container, preview_button):
    """
    Toggles the visibility of the parameter preview and updates the preview content.
    
    Args:
        json_editor (ui.codemirror): The JSON editor containing the schema.
        preview_container (ui.column): The container for the preview elements.
        preview_button (ui.button): The button to toggle the preview.
    
    Raises:
        json.JSONDecodeError: If the JSON in the editor is invalid.
    """
    try:
        schema = json.loads(json_editor.value)
        if preview_container.visible:
            preview_container.set_visibility(False)
            preview_button.set_text('Mostrar vista previa')
        else:
            update_preview(schema, preview_container)
            preview_container.set_visibility(True)
            preview_button.set_text('Ocultar vista previa')
    except json.JSONDecodeError:
        ui.notify('Error al analizar el JSON. Por favor, verifica la sintaxis.', color='negative')