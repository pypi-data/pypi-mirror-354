# Settings UI components

from nicegui import ui
from mcp_open_client.state.core import app_state, get_app_state
from mcp_open_client.state import api as state_api
from mcp_open_client import state  # Keep this for other state functions
from typing import Optional
import asyncio
import logging

async def fetch_models():
    """Fetches available models from the API and returns them as options for the dropdown"""
    # Get the current model
    current_model = app_state['settings']['model']
    
    # Create a dictionary with only the current model
    current_model_dict = {current_model: f'Current: {current_model}'}
    
    # If API is not initialized, return only the current model
    if state.api is None:
        ui.notify('API no inicializada, solo se muestra el modelo actual', type='warning')
        return current_model_dict
    
    try:
        # Show ongoing notification
        ui.notify('Obteniendo modelos disponibles...', type='ongoing')
        success, models_dict = await state_api.get_available_models()
        
        if success and models_dict:
            # Return the models dictionary from the API
            return models_dict
        else:
            # This warning notification will replace the ongoing one
            ui.notify('No se pudieron obtener los modelos de la API, solo se muestra el modelo actual', type='warning')
            return current_model_dict
    except Exception as e:
        # This error notification will replace the ongoing one
        ui.notify(f'Error al obtener modelos: {str(e)}', type='negative')
        return current_model_dict

def render_settings_page(container):
    """Renders the settings page"""
    with container:
        ui.label('Configuración').classes('app-page-title')
        
        with ui.card().classes('app-card'):
            ui.label('System Prompt').classes('app-card-title')
            
            # System prompt text area
            ui.label('Prompt del sistema:')
            system_prompt_input = ui.textarea(
                value=app_state['settings']['system_prompt'],
                placeholder='Ingresa el prompt del sistema...'
            ).classes('app-textarea app-full-width')
            
            # Update system prompt on change
            def update_system_prompt():
                get_app_state()['settings']['system_prompt'] = system_prompt_input.value
            
            system_prompt_input.on('change', lambda _: update_system_prompt())
        
        with ui.card().classes('app-card'):
            ui.label('Modelo de IA').classes('app-card-title')
            
            # Get the current model
            current_model = app_state['settings']['model']
            
            # Initialize with only the current model (no default options)
            initial_options = {current_model: f'Current: {current_model}'}
            
            # Create the model dropdown with minimal initial options
            model_select = ui.select(
                options=initial_options,
                value=current_model,
                on_change=lambda e: get_app_state()['settings'].update({'model': e.value})
            ).classes('app-select app-full-width')
            
            # Function to update the model dropdown
            async def update_model_dropdown():
                # Use fetch_models directly which returns a dictionary
                # fetch_models will show its own notifications
                model_options = await fetch_models()
                
                # Update the dropdown options and force a UI refresh
                model_select.options = model_options
                model_select.update()
                
                # Make sure the current value is valid
                current_model = app_state['settings']['model']
                if current_model in model_options:
                    model_select.value = current_model
                elif model_options:
                    # Set to first option if current is not available
                    first_model = next(iter(model_options))
                    model_select.value = first_model
                    get_app_state()['settings']['model'] = first_model
                
                ui.notify('Lista de modelos actualizada', type='positive')
            
            # Add a refresh button with a more descriptive label
            ui.button('Actualizar lista de modelos', icon='refresh', on_click=update_model_dropdown).classes('app-button')
            
            # Initialize with only the current model without automatic fetching
            # This prevents the get_available_models function from being called too frequently
        
        with ui.card().classes('app-card'):
            ui.label('Parámetros de Generación').classes('app-card-title')
            
            # Temperature slider
            ui.label(f"Temperatura: {app_state['settings']['temperature']}")
            ui.slider(
                min=0, max=1, step=0.1,
                value=app_state['settings']['temperature'],
                on_change=lambda e: update_temperature(e.value)
            ).classes('app-slider app-full-width')
            
            # Max tokens slider
            ui.label(f"Tokens máximos: {app_state['settings']['max_tokens']}")
            ui.slider(
                min=100, max=4000, step=100,
                value=app_state['settings']['max_tokens'],
                on_change=lambda e: update_max_tokens(e.value)
            ).classes('app-slider app-full-width')
        
        with ui.card().classes('app-card'):
            ui.label('Configuración de API').classes('app-card-title')
            
            # Base URL input
            ui.label('URL Base:')
            base_url_input = ui.input(
                value=app_state['settings']['base_url'],
                on_change=lambda e: update_base_url(e.value)
            ).classes('app-input app-full-width')
            
            # API Key input
            ui.label('API Key:')
            api_key_input = ui.input(
                value=app_state['settings']['api_key'],
                password=True,
                on_change=lambda e: update_api_key(e.value)
            ).classes('app-input app-full-width')
            
            # Button to apply API changes
            ui.button('Aplicar cambios de API', on_click=apply_api_changes).classes('app-button app-full-width')
        
        with ui.card().classes('app-card'):
            ui.label('Opciones de Depuración').classes('app-card-title')
            
            # Debug logging toggle
            debug_enabled = ui.checkbox('Habilitar logs de depuración de API',
                                       value=app_state['settings'].get('debug_logging', False))
            
            ui.label('Muestra información detallada sobre las solicitudes y respuestas de la API').classes('app-text-caption')
            
            # Update debug logging setting on change
            def update_debug_logging():
                get_app_state()['settings']['debug_logging'] = debug_enabled.value
                
                # Update logger level based on setting
                if debug_enabled.value:
                    logging.getLogger('mcp_open_client.api').setLevel(logging.DEBUG)
                    ui.notify('Logs de depuración de API habilitados', type='positive')
                else:
                    logging.getLogger('mcp_open_client.api').setLevel(logging.INFO)
                    ui.notify('Logs de depuración de API deshabilitados', type='positive')
            
            debug_enabled.on('change', lambda _: update_debug_logging())

def update_temperature(value):
    """Updates the temperature setting and shows the current value"""
    get_app_state()['settings']['temperature'] = value
    ui.notify(f'Temperatura actualizada a: {value}')

def update_max_tokens(value):
    """Updates the max tokens setting and shows the current value"""
    get_app_state()['settings']['max_tokens'] = int(value)
    ui.notify(f'Tokens máximos actualizados a: {int(value)}')

def update_base_url(value):
    """Updates the base URL setting"""
    get_app_state()['settings']['base_url'] = value
    ui.notify(f'URL Base actualizada a: {value}')

def update_api_key(value):
    """Updates the API key setting"""
    get_app_state()['settings']['api_key'] = value
    ui.notify('API Key actualizada')

def apply_api_changes():
    """Applies API changes by reinitializing the API client"""
    state.save_settings()
    if state_api.reinitialize_api():
        ui.notify('Configuración de API aplicada correctamente', type='positive')
        
        # No need to refresh the entire page, just notify the user
        # The user can manually refresh the model list if needed
    else:
        ui.notify('Error al aplicar configuración de API', type='negative')