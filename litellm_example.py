"""
LiteLLM Example - A comprehensive guide to using LiteLLM for multi-provider LLM interactions.

LiteLLM provides a unified interface to interact with various LLM providers (OpenAI, Anthropic, 
Google, Azure, Bedrock, etc.) using a consistent API.
"""

import os
from typing import List, Dict, Any
import litellm
from litellm import completion, acompletion


def basic_completion_example():
    """
    Basic example of making a completion request.
    Works with any provider - just change the model name.
    """
    print("=== Basic Completion Example ===")
    
    # OpenAI example
    response = completion(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say hello in 3 different languages"}
        ]
    )
    print(f"Response: {response.choices[0].message.content}\n")


def multi_provider_example():
    """
    Demonstrate calling different providers with the same interface.
    """
    print("=== Multi-Provider Example ===")
    
    models = [
        "gpt-3.5-turbo",           # OpenAI
        "claude-3-haiku-20240307",  # Anthropic
        "gemini/gemini-pro",       # Google
    ]
    
    message = "What is 2+2? Answer in one sentence."
    
    for model in models:
        try:
            response = completion(
                model=model,
                messages=[{"role": "user", "content": message}]
            )
            print(f"{model}: {response.choices[0].message.content}")
        except Exception as e:
            print(f"{model}: Error - {str(e)}")
    print()


def streaming_example():
    """
    Example of streaming responses for real-time output.
    """
    print("=== Streaming Example ===")
    
    response = completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Count from 1 to 5"}],
        stream=True
    )
    
    print("Streaming response: ", end="")
    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")


async def async_completion_example():
    """
    Asynchronous completion for better performance in async applications.
    """
    print("=== Async Completion Example ===")
    
    response = await acompletion(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
    print(f"Async Response: {response.choices[0].message.content}\n")


def conversation_example():
    """
    Example of maintaining conversation context.
    """
    print("=== Conversation Example ===")
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that speaks like a pirate."},
        {"role": "user", "content": "Hello!"}
    ]
    
    # First turn
    response = completion(model="gpt-3.5-turbo", messages=messages)
    assistant_message = response.choices[0].message.content
    print(f"Assistant: {assistant_message}")
    
    # Add to conversation history
    messages.append({"role": "assistant", "content": assistant_message})
    messages.append({"role": "user", "content": "What's the weather like?"})
    
    # Second turn
    response = completion(model="gpt-3.5-turbo", messages=messages)
    print(f"Assistant: {response.choices[0].message.content}\n")


def function_calling_example():
    """
    Example of using function calling (tool use) with LiteLLM.
    """
    print("=== Function Calling Example ===")
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]
    
    messages = [{"role": "user", "content": "What's the weather like in Boston?"}]
    
    response = completion(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        print(f"Function called: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}\n")
    else:
        print(f"Response: {response.choices[0].message.content}\n")


def error_handling_example():
    """
    Example of proper error handling with LiteLLM.
    """
    print("=== Error Handling Example ===")
    
    try:
        response = completion(
            model="invalid-model-name",
            messages=[{"role": "user", "content": "Hello"}]
        )
    except litellm.exceptions.BadRequestError as e:
        print(f"Bad Request: {e}")
    except litellm.exceptions.AuthenticationError as e:
        print(f"Authentication Error: {e}")
    except litellm.exceptions.RateLimitError as e:
        print(f"Rate Limit Error: {e}")
    except Exception as e:
        print(f"General Error: {e}")
    print()


def configuration_example():
    """
    Example of configuring LiteLLM settings.
    """
    print("=== Configuration Example ===")
    
    # Set timeout
    litellm.request_timeout = 60
    
    # Enable/disable debug logging
    litellm.set_verbose = False
    
    # Set default retry configuration
    litellm.num_retries = 3
    
    # Custom callbacks for logging
    def custom_callback(kwargs, completion_response, start_time, end_time):
        print(f"Request took {end_time - start_time} seconds")
    
    litellm.success_callback = [custom_callback]
    
    print("Configuration applied\n")


def cost_tracking_example():
    """
    Example of tracking API costs with LiteLLM.
    """
    print("=== Cost Tracking Example ===")
    
    response = completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    # LiteLLM automatically calculates costs
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Completion tokens: {response.usage.completion_tokens}")
    print(f"Total tokens: {response.usage.total_tokens}")
    
    # Calculate cost (example - actual costs vary by provider)
    cost = litellm.completion_cost(completion_response=response)
    print(f"Estimated cost: ${cost:.6f}\n")


def main():
    """
    Run all examples. Make sure to set appropriate API keys as environment variables:
    - OPENAI_API_KEY for OpenAI
    - ANTHROPIC_API_KEY for Anthropic/Claude
    - GEMINI_API_KEY (or GOOGLE_API_KEY) for Google
    """
    print("LiteLLM Examples\n")
    print("=" * 50)
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Some examples may fail.\n")
    
    try:
        basic_completion_example()
        # multi_provider_example()  # Uncomment if you have multiple provider keys
        streaming_example()
        conversation_example()
        function_calling_example()
        error_handling_example()
        configuration_example()
        cost_tracking_example()
        
        # Uncomment to run async example
        # import asyncio
        # asyncio.run(async_completion_example())
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("\nMake sure you have set your API keys as environment variables.")


if __name__ == "__main__":
    main()
