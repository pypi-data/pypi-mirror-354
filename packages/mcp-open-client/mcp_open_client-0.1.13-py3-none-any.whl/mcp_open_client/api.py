from openai import AsyncOpenAI
import asyncio
import logging
import json
from typing import List, Dict, Any, Tuple, Optional, Sequence, Union
from mcp_open_client.state import get_app_state, sanitize_function_name, execute_tool, get_current_conversation, add_message_to_conversation, save_conversations_to_storage

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Default to INFO level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mcp_open_client.api')

# Set logger level based on debug_logging setting
app_state = get_app_state()
if app_state['settings'].get('debug_logging', False):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# Provider-specific configurations
PROVIDER_CONFIGS = {
    'anthropic': {
        'model_patterns': ['claude'],
        'requires_tools_param': True,
        'supports_parallel_tools': True,
        'max_retries': 3,
        'retry_delay': 1.0,
        'tool_choice_options': ['auto', 'any', 'tool']
    },
    'openai': {
        'model_patterns': ['gpt', 'o1'],
        'requires_tools_param': False,
        'supports_parallel_tools': True,
        'max_retries': 3,
        'retry_delay': 0.5,
        'tool_choice_options': ['auto', 'none', 'required']
    },
    'google': {
        'model_patterns': ['gemini'],
        'requires_tools_param': False,
        'supports_parallel_tools': True,
        'max_retries': 3,
        'retry_delay': 0.5,
        'tool_choice_options': ['auto', 'none', 'any']
    }
}

def detect_provider(model_name: str) -> str:
    """Detect the provider based on model name"""
    model_lower = model_name.lower()
    for provider, config in PROVIDER_CONFIGS.items():
        for pattern in config['model_patterns']:
            if pattern in model_lower:
                return provider
    return 'unknown'

def validate_tool_format(tools: List[Dict[str, Any]], provider: str) -> List[Dict[str, Any]]:
    """Validate and normalize tool format for specific provider"""
    if not tools:
        return []
    
    validated_tools = []
    for tool in tools:
        # Ensure OpenAI-compatible format
        if 'type' not in tool:
            tool['type'] = 'function'
        
        if 'function' not in tool:
            logger.warning(f"Tool missing 'function' field: {tool}")
            continue
            
        function = tool['function']
        
        # Validate required fields
        if 'name' not in function:
            logger.warning(f"Tool function missing 'name' field: {function}")
            continue
            
        if 'description' not in function:
            function['description'] = f"Function {function['name']}"
            
        # Ensure parameters schema is valid
        if 'parameters' not in function:
            function['parameters'] = {
                "type": "object",
                "properties": {},
                "required": []
            }
        elif function['parameters'].get('type') != 'object':
            function['parameters']['type'] = 'object'
            
        # Provider-specific validations
        if provider == 'anthropic':
            # Claude requires additionalProperties: false for strict mode
            if 'additionalProperties' not in function['parameters']:
                function['parameters']['additionalProperties'] = False
                
        validated_tools.append(tool)
    
    return validated_tools

class ChatAPI:
    def __init__(self, base_url: str, model: str, api_key: str = "not-needed"):
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=30.0,
            max_retries=3,
        )
        self.model = model
        self.base_url = base_url
        
    def get_provider_for_model(self, model: str) -> str:
        """Determine the provider based on the model name."""
        for provider, config in PROVIDER_CONFIGS.items():
            for pattern in config['model_patterns']:
                if pattern in model.lower():
                    return provider
        return 'openai'  # Default to OpenAI if no match found
        
    def validate_messages(self, messages: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ensure all messages have valid content fields"""
        validated = []
        for msg in messages:
            # Create a copy to avoid modifying the original
            msg_copy = msg.copy()
            
            # Ensure content is never null
            if msg_copy.get('content') is None:
                msg_copy['content'] = ""
            
            # Ensure tool messages have tool_call_id
            if msg_copy.get('role') == 'tool' and 'tool_call_id' not in msg_copy:
                # If missing, try to find it in the original message
                if 'tool_call_id' in msg:
                    msg_copy['tool_call_id'] = msg['tool_call_id']
                
            validated.append(msg_copy)
        return validated
        
    async def get_available_models(self) -> Tuple[bool, List[str]]:
        """Fetches available models from the API"""
        try:
            response = await self.client.models.list()
            models = [model.id for model in response.data]
            return True, models
        except Exception as e:
            error_msg = f"Error fetching models: {type(e).__name__}: {str(e)}"
            return False, []
        
    async def send_message(self, messages: Sequence[Dict[str, Any]], model: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 2000, tools: Optional[List[Dict[str, Any]]] = None) -> Tuple[bool, str, bool]:
        try:
            # Validate messages to ensure content is never null
            validated_messages: List[Dict[str, Any]] = self.validate_messages(messages)
            
            # Create parameters for the API call
            params: Dict[str, Any] = {
                "model": model or self.model,
                "messages": validated_messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            
            # Get provider and config for proper tool handling
            current_model: str = model or self.model
            provider = self.get_provider_for_model(current_model)
            provider_config = PROVIDER_CONFIGS.get(provider, {})
            
            # Add tools if provided, using provider-specific validation
            if tools and len(tools) > 0:
                # Validate and format tools for the specific provider
                validated_tools = validate_tool_format(tools, provider)
                
                # Sanitize function names for all providers
                sanitized_tools: List[Dict[str, Any]] = []
                for tool in validated_tools:
                    tool_copy: Dict[str, Any] = tool.copy()
                    if 'function' in tool_copy and 'name' in tool_copy['function']:
                        # Use the sanitize_function_name function
                        original_name = tool_copy['function']['name']
                        tool_copy['function']['name'] = sanitize_function_name(original_name)
                    sanitized_tools.append(tool_copy)
                
                params["tools"] = sanitized_tools
                
            elif provider_config.get('requires_tools_param', False):
                # Some providers (like Anthropic) require tools parameter even if empty
                params["tools"] = []
            
            # Log the API request
            logger.debug(f"Sending request to API: {self.base_url}/chat/completions")
            logger.debug(f"Request params: model={params['model']}, tools={len(params.get('tools', []))}")
            logger.debug(f"Is Anthropic model: {'claude' in (model or self.model).lower()}")
            
            # Get provider and config for use throughout the method
            provider = self.get_provider_for_model(model or self.model)
            provider_config = PROVIDER_CONFIGS.get(provider, {})
            
            # Make the API call
            response = await self.client.chat.completions.create(**params)
            
            # Log the API response
            logger.debug(f"Received response from API")
            logger.debug(f"Response model: {response.model}")
            
            # Check if there's a tool call in the response
            if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                # Get the tool calls
                tool_calls: List[Any] = response.choices[0].message.tool_calls
                
                # Create a message for the tool call
                tool_call_message: Dict[str, Any] = {
                    "role": "assistant",
                    "content": "",  # Empty string instead of null
                    "tool_calls": []
                }
                
                # Process each tool call
                tool_results: List[Dict[str, Any]] = []
                
                for tool_call in tool_calls:
                    # Extract tool information
                    tool_name: str = tool_call.function.name
                    tool_arguments: str = tool_call.function.arguments
                    tool_id: str = tool_call.id
                    
                    # Find the tool by name
                    import json
                    
                    # Find the tool in our tools list
                    app_state = get_app_state()
                    # Try multiple matching strategies to find the tool
                    matched_tool: Optional[Dict[str, Any]] = None
                    
                    # Strategy 1: Match on sanitized_name field
                    if not matched_tool:
                        matched_tool = next((t for t in app_state['tools'] if t.get('sanitized_name') == tool_name), None)
                    
                    # Strategy 2: Match on original_name field
                    if not matched_tool:
                        matched_tool = next((t for t in app_state['tools'] if t.get('original_name') == tool_name), None)
                    
                    # Strategy 3: Match on name field (fallback for older structure)
                    if not matched_tool:
                        matched_tool = next((t for t in app_state['tools'] if t.get('name') == tool_name), None)
                    
                    # Strategy 4: Match on id field (for default tools)
                    if not matched_tool:
                        matched_tool = next((t for t in app_state['tools'] if t.get('id') == tool_name), None)
                    
                    if matched_tool:
                        # Add the tool call to the message
                        tool_call_message["tool_calls"].append({
                            "id": tool_id,
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "arguments": tool_arguments
                            }
                        })
                        
                        # Parse arguments
                        try:
                            args: Dict[str, Any] = json.loads(tool_arguments)
                        except:
                            args = {}
                        
                        # Execute the tool using the most reliable identifier
                        # Priority: id > sanitized_name > original_name > name > tool_name
                        execution_tool_name = (matched_tool.get('id') or
                                             matched_tool.get('sanitized_name') or
                                             matched_tool.get('original_name') or
                                             matched_tool.get('name') or
                                             tool_name)
                        logger.debug(f"Executing tool with identifier: {execution_tool_name}")
                        execution_result = execute_tool(execution_tool_name, args)
                        
                        # Format the result based on execution success
                        if execution_result['success']:
                            result_content = execution_result['result']
                            content = json.dumps(result_content) if isinstance(result_content, dict) else str(result_content)
                        else:
                            content = f"Error: {execution_result['error']}"
                        
                        # Format the result
                        tool_result: Dict[str, Any] = {
                            "tool_call_id": tool_id,
                            "role": "tool",
                            "name": tool_name,
                            "content": content
                        }
                        
                        tool_results.append(tool_result)
                    else:
                        # Tool not found - create error response
                        logger.warning(f"Tool not found or missing 'id': {tool_name}")
                        tool_result: Dict[str, Any] = {
                            "tool_call_id": tool_id,
                            "role": "tool",
                            "name": tool_name,
                            "content": f"Error: Tool '{tool_name}' not found or not available"
                        }
                        tool_results.append(tool_result)
                
                # Get the current conversation
                current_conv: Optional[Dict[str, Any]] = get_current_conversation()
                
                if current_conv:
                    # Add the tool call message to the conversation
                    add_message_to_conversation(current_conv['id'], tool_call_message)
                    
                    # Add the tool results to the conversation
                    for result in tool_results:
                        add_message_to_conversation(current_conv['id'], result)
                    
                    # Save to user storage
                    save_conversations_to_storage()
                
                # Add the tool call message to the messages for the API
                messages = list(messages)  # Convert Sequence to List
                messages.append(tool_call_message)
                
                # Add the tool results to the messages for the API
                for result in tool_results:
                    messages.append(result)
                
                # Make a second API call with the tool results
                # Validate messages again before the second API call
                validated_messages = self.validate_messages(messages)
                
                # Log the second API request for tool calls
                logger.debug(f"Sending follow-up request to {provider} API with tool results")
                logger.debug(f"Request params: model={model}, tools_results={len(tool_results)}")
                
                # Create parameters for the second API call with provider-specific handling
                second_params: Dict[str, Any] = {
                    "model": model,
                    "messages": validated_messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                # Include tools parameter based on provider requirements
                # Use the same sanitized tools from the first call for consistency
                if params.get("tools") is not None or provider_config.get('requires_tools_param', False):
                    second_params["tools"] = params.get("tools", [])
                
                # Add provider-specific tool_choice if configured
                if provider_config.get('tool_choice_options') and tools:
                    tool_choice_options = provider_config['tool_choice_options']
                    if 'auto' in tool_choice_options:
                        second_params["tool_choice"] = 'auto'
                
                # Ensure all parameters are of the correct type
                cleaned_params: Dict[str, Any] = {
                    k: v for k, v in second_params.items()
                    if k in ['model', 'messages', 'temperature', 'top_p', 'n', 'stream', 'stop', 'max_tokens', 'presence_penalty', 'frequency_penalty', 'logit_bias', 'user', 'tools', 'tool_choice']
                }
                
                # Implement retry logic for unreliable providers (like Claude)
                max_retries = provider_config.get('max_retries', 1)
                retry_delay = provider_config.get('retry_delay', 1.0)
                
                for attempt in range(max_retries):
                    try:
                        response = await self.client.chat.completions.create(**cleaned_params)
                        
                        # Log the API response
                        logger.debug(f"Received follow-up response from {provider} API (attempt {attempt + 1})")
                        
                        # Return the final response with has_tool_calls=True
                        return True, response.choices[0].message.content or "", True
                        
                    except Exception as retry_error:
                        if attempt < max_retries - 1:
                            logger.warning(f"Attempt {attempt + 1} failed for {provider}, retrying in {retry_delay}s: {retry_error}")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                        else:
                            # Final attempt failed, re-raise the error
                            raise retry_error
            
            # Return normal message content with has_tool_calls=False
            return True, response.choices[0].message.content, False
        except Exception as e:
            error_msg = f"**Error:** {type(e).__name__}: {str(e)}"
            logger.error(f"API request failed: {error_msg}")
            return False, error_msg, False