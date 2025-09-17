# Basic LiteLLM Example

from litellm import Completion

# Define a simple function to generate text completions
def generate_completion(prompt):
    # Use LiteLLM to generate a completion for the given prompt
    response = Completion.create(model="gpt-3.5-turbo", prompt=prompt, max_tokens=50)
    return response["choices"][0]["text"]

# Define a function to generate multiple completions
def generate_multiple_completions(prompt, num_completions=3):
    # Use LiteLLM to generate multiple completions for the given prompt
    response = Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=50,
        n=num_completions
    )
    return [choice["text"] for choice in response["choices"]]

# Define a function to generate completions with temperature control
def generate_with_temperature(prompt, temperature=0.7):
    # Use LiteLLM to generate a completion with a specified temperature
    response = Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=50,
        temperature=temperature
    )
    return response["choices"][0]["text"]

# Example usage
if __name__ == "__main__":
    prompt = "Once upon a time in a small village, there was a"
    
    # Single completion
    completion = generate_completion(prompt)
    print("Single Completion:")
    print("Prompt:", prompt)
    print("Completion:", completion)
    
    # Multiple completions
    print("\nMultiple Completions:")
    multiple_completions = generate_multiple_completions(prompt, num_completions=3)
    for i, comp in enumerate(multiple_completions, 1):
        print(f"Completion {i}:", comp)
    
    # Completion with temperature control
    print("\nCompletion with Temperature Control:")
    temp_completion = generate_with_temperature(prompt, temperature=0.9)
    print("Prompt:", prompt)
    print("Completion:", temp_completion)
