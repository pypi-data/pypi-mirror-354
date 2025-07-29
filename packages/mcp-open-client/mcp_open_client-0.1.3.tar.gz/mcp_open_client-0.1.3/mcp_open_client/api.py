from openai import AsyncOpenAI
import logging
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
        
    def validate_messages(self, messages):
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
        
    async def get_available_models(self) -> tuple[bool, list]:
        """Fetches available models from the API"""
        try:
            response = await self.client.models.list()
            models = [model.id for model in response.data]
            return True, models
        except Exception as e:
            error_msg = f"Error fetching models: {type(e).__name__}: {str(e)}"
            return False, []
        
    async def send_message(self, messages: list, model: str = None, temperature: float = 0.7, max_tokens: int = 2000, tools: list = None) -> tuple[bool, str, bool]:
        try:
            # Validate messages to ensure content is never null
            validated_messages = self.validate_messages(messages)
            
            # Create parameters for the API call
            params = {
                "model": model or self.model,
                "messages": validated_messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            
            # Check if we're using an Anthropic model
            current_model = model or self.model
            is_anthropic_model = "claude" in current_model.lower()
            
            # Add tools if provided
            # Note: For OpenAI-compatible API, tools must use the "function" format
            # Example format:
            # {
            #     "type": "function",
            #     "function": {
            #         "name": "tool_name",
            #         "description": "tool_description",
            #         "parameters": {
            #             "type": "object",
            #             "properties": {...},
            #             "required": [...],
            #             "additionalProperties": false
            #         }
            #     }
            # }
            
            # Always include tools parameter for Anthropic models, even if empty
            if (tools and len(tools) > 0) or is_anthropic_model:
                # Ensure function names follow the required pattern (no spaces, only a-zA-Z0-9_-)
                sanitized_tools = []
                
                # If tools are provided, sanitize them
                if tools and len(tools) > 0:
                    for tool in tools:
                        tool_copy = tool.copy()
                        if 'function' in tool_copy and 'name' in tool_copy['function']:
                            # Use the sanitize_function_name function
                            original_name = tool_copy['function']['name']
                            tool_copy['function']['name'] = sanitize_function_name(original_name)
                        sanitized_tools.append(tool_copy)
                
                # Always set the tools parameter (even if it's an empty list for Anthropic models)
                params["tools"] = sanitized_tools
            
            # Log the API request
            logger.debug(f"Sending request to API: {self.base_url}/chat/completions")
            logger.debug(f"Request params: model={params['model']}, tools={len(params.get('tools', []))}")
            logger.debug(f"Is Anthropic model: {'claude' in (model or self.model).lower()}")
            
            # Make the API call
            response = await self.client.chat.completions.create(**params)
            
            # Log the API response
            logger.debug(f"Received response from API")
            logger.debug(f"Response model: {response.model}")
            
            # Check if there's a tool call in the response
            if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                # Get the tool calls
                tool_calls = response.choices[0].message.tool_calls
                
                # Create a message for the tool call
                tool_call_message = {
                    "role": "assistant",
                    "content": "",  # Empty string instead of null
                    "tool_calls": []
                }
                
                # Process each tool call
                tool_results = []
                
                for tool_call in tool_calls:
                    # Extract tool information
                    tool_name = tool_call.function.name
                    tool_arguments = tool_call.function.arguments
                    tool_id = tool_call.id
                    
                    # Find the tool by name
                    import json
                    
                    # Find the tool in our tools list
                    app_state = get_app_state()
                    # First try exact match with the sanitized name (stored in 'name')
                    tool = next((t for t in app_state['tools'] if t['name'] == tool_name), None)
                    
                    # If not found, try matching with the original name
                    if not tool:
                        tool = next((t for t in app_state['tools'] if t.get('original_name') == tool_name), None)
                    
                    # If still not found, try sanitizing the original name for comparison
                    if not tool:
                        tool = next((t for t in app_state['tools']
                                    if 'original_name' in t and sanitize_function_name(t['original_name']) == tool_name), None)
                    
                    if tool:
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
                            args = json.loads(tool_arguments)
                        except:
                            args = {}
                        
                        # Execute the tool
                        success, result = execute_tool(tool['id'], args)
                        
                        # Format the result
                        tool_result = {
                            "tool_call_id": tool_id,
                            "role": "tool",
                            "name": tool_name,
                            "content": json.dumps(result) if isinstance(result, dict) else str(result)
                        }
                        
                        tool_results.append(tool_result)
                
                # Get the current conversation
                current_conv = get_current_conversation()
                
                if current_conv:
                    # Add the tool call message to the conversation
                    add_message_to_conversation(current_conv['id'], tool_call_message)
                    
                    # Add the tool results to the conversation
                    for result in tool_results:
                        add_message_to_conversation(current_conv['id'], result)
                    
                    # Save to user storage
                    save_conversations_to_storage()
                
                # Add the tool call message to the messages for the API
                messages.append(tool_call_message)
                
                # Add the tool results to the messages for the API
                for result in tool_results:
                    messages.append(result)
                
                # Make a second API call with the tool results
                # Validate messages again before the second API call
                validated_messages = self.validate_messages(messages)
                
                # Log the second API request for tool calls
                logger.debug(f"Sending follow-up request to API with tool results")
                logger.debug(f"Request params: model={model or self.model}, tools_results={len(tool_results)}")
                
                # Create parameters for the second API call
                second_params = {
                    "model": model or self.model,
                    "messages": validated_messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                # Check if we're using an Anthropic model
                current_model = model or self.model
                is_anthropic_model = "claude" in current_model.lower()
                
                # Always include tools parameter for Anthropic models, even if empty
                if is_anthropic_model:
                    second_params["tools"] = []
                
                response = await self.client.chat.completions.create(**second_params)
                
                # Log the API response
                logger.debug(f"Received follow-up response from API")
                
                # Return the final response with has_tool_calls=True
                return True, response.choices[0].message.content, True
            
            # Return normal message content with has_tool_calls=False
            return True, response.choices[0].message.content, False
        except Exception as e:
            error_msg = f"**Error:** {type(e).__name__}: {str(e)}"
            logger.error(f"API request failed: {error_msg}")
            return False, error_msg, False