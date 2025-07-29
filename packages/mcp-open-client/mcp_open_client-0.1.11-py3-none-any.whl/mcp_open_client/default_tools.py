"""Default tools for MCP Open Client"""

# Default tools that are included with the application
DEFAULT_TOOLS = [
    {
        'id': 'eval-python-code',
        'type': 'function',
        'name': 'eval python code',
        'description': 'Ejecuta código Python en el navegador usando Pyodide',
        'parameters': '''{
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Código Python a ejecutar"
                }
            },
            "required": ["code"],
            "additionalProperties": false
        }''',
        'code': '''def execute_tool(params):
    """Ejecuta código Python en el navegador usando Pyodide
    
    Args:
        params (dict): Parámetros recibidos según el esquema JSON definido
            - code (str): Código Python a ejecutar
        
    Returns:
        dict: Resultado de la ejecución del código
    """
    from nicegui import ui
    import uuid
    
    # Extraer el código a ejecutar
    code = params.get('code', '')
    
    if not code.strip():
        return {
            "success": False,
            "error": "No se proporcionó código para ejecutar",
            "result": None
        }
    
    # Crear un ID único para este elemento
    element_id = f"pyodide-result-{uuid.uuid4()}"
    
    # Crear un elemento para mostrar el resultado
    result_element = ui.html(f'<div id="{element_id}" class="w-full p-4 bg-gray-100 rounded overflow-auto"></div>')
    
    # Función para escapar el código Python para JavaScript
    def escape_for_js(code_str):
        # Escapar caracteres especiales para template literals de JS
        return (code_str.replace('`', '`+"`"+`')
                       .replace('${', '`+"${"+`')
                       .replace("'", "\\'")
                       .replace('"', '\\"'))
    
    # Código Python escapado para JS
    escaped_code = escape_for_js(code)
    
    # Asegurarse de que Pyodide esté disponible primero
    ui.add_head_html("""
    <script src="https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"></script>
    """)
    
    # Ejecutar el código Python usando Pyodide de forma silenciosa
    js_code = f"""
    (async () => {{
        try {{
            // Esperar a que loadPyodide esté disponible (sin mostrar mensajes)
            let retries = 0;
            while (typeof loadPyodide === 'undefined' && retries < 50) {{
                await new Promise(resolve => setTimeout(resolve, 100));
                retries++;
            }}
            
            if (typeof loadPyodide === 'undefined') {{
                throw new Error('Pyodide no disponible');
            }}
            
            // Cargar Pyodide si no está ya cargado
            if (!window.pyodide) {{
                window.pyodide = await loadPyodide({{
                    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/"
                }});
            }}
            
            // Redirigir stdout a una variable
            let stdout = "";
            window.pyodide.setStdout({{
                write: (text) => {{
                    stdout += text;
                }}
            }});
            
            // Ejecutar el código
            let result = await window.pyodide.runPythonAsync(`{escaped_code}`);
            
            // Formatear el resultado
            let resultStr = "";
            if (result !== undefined) {{
                if (typeof result === 'object' && result.toString) {{
                    resultStr = result.toString();
                }} else {{
                    resultStr = String(result);
                }}
            }}
            
            // Mostrar solo el resultado final
            let outputHtml = '<div class="font-mono">';
            
            // Mostrar stdout si hay algo
            if (stdout) {{
                outputHtml += '<div class="mb-2"><strong>Salida:</strong><pre class="bg-gray-200 p-2 rounded mt-1 overflow-auto">' +
                    stdout.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</pre></div>';
            }}
            
            // Mostrar el valor de retorno si hay algo
            if (resultStr) {{
                outputHtml += '<div><strong>Resultado:</strong><pre class="bg-gray-200 p-2 rounded mt-1 overflow-auto">' +
                    resultStr.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</pre></div>';
            }}
            
            outputHtml += '</div>';
            document.getElementById('{element_id}').innerHTML = outputHtml;
            
            return {{
                success: true,
                stdout: stdout,
                result: resultStr
            }};
        }} catch (error) {{
            // Mostrar error de forma simple
            document.getElementById('{element_id}').innerHTML =
                '<div class="text-red-500 font-mono"><strong>Error:</strong><pre class="bg-red-100 p-2 rounded mt-1">' +
                error.message.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</pre></div>';
            
            return {{
                success: false,
                error: error.message,
                result: null
            }};
        }}
    }})();
    """
    
    # Ejecutar el código JavaScript
    result = ui.run_javascript(js_code)
    
    return {
        "success": True,
        "message": "Código ejecutado en el navegador",
        "element_id": element_id
    }
''',
        'active': True
    }
]

def get_default_tools():
    """Returns a copy of the default tools"""
    import copy
    print("\n=== GET_DEFAULT_TOOLS CALLED ===")
    
    # Debug: Print the DEFAULT_TOOLS list
    print(f"DEFAULT_TOOLS contains {len(DEFAULT_TOOLS)} tools:")
    for i, tool in enumerate(DEFAULT_TOOLS):
        print(f"  {i+1}. ID: {tool.get('id', 'NO ID')}")
        print(f"     Name: {tool.get('name', 'NO NAME')}")
        print(f"     Type: {tool.get('type', 'NO TYPE')}")
        print(f"     Active: {tool.get('active', False)}")
    
    # Make a deep copy of the tools
    tools = copy.deepcopy(DEFAULT_TOOLS)
    
    # Debug: Print the copied tools
    print(f"get_default_tools() returning {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool['id']}: {tool['name']}")
    
    print("=== END OF GET_DEFAULT_TOOLS ===\n")
    return tools
