# Basic LiteLLM Example

from litellm import Completion

# Define a simple function to generate text completions
def generate_completion(prompt):
    # Use LiteLLM to generate a completion for the given prompt
    response = Completion.create(model="gpt-3.5-turbo", prompt=prompt, max_tokens=50)
    return response["choices"][0]["text"]

# Example usage
if __name__ == "__main__":
    prompt = "Once upon a time in a small village, there was a"
    completion = generate_completion(prompt)
    print("Prompt:", prompt)
    print("Completion:", completion)
