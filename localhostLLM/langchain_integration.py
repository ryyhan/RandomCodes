from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional
import requests

class LocalFastAPI_LLM(LLM):
    """
    A custom LangChain LLM that interacts with a local FastAPI server.
    This class is generalized to handle different endpoints and JSON response keys.
    """

    endpoint: str
    response_key: str

    @property
    def _llm_type(self) -> str:
        return "local_fastapi_llm"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Make a POST request to the specified FastAPI endpoint and return the response.
        """
        payload = {"text": prompt}

        try:
            response = requests.post(self.endpoint, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            result = response.json()
            return result.get(self.response_key, "")

        except requests.exceptions.RequestException as e:
            return f"Error from API: {e}"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"endpoint": self.endpoint, "response_key": self.response_key}

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Make sure your FastAPI server is running in a separate terminal:
    #    uvicorn localhostLLM:app --host 0.0.0.0 --port 8000

    print("--- Testing Text Generation ---")
    # 2. Instantiate the LLM for generation
    llm_generator = LocalFastAPI_LLM(
        endpoint="http://127.0.0.1:8000/generate/",
        response_key="generated_text"
    )

    # 3. Send a prompt to the LLM for generation
    prompt_gen = "In a world where AI rules,"
    response_gen = llm_generator.invoke(prompt_gen)

    print(f"Prompt (Generation): {prompt_gen}")
    print(f"Response (Generation): {response_gen}")

    print("\n--- Testing Text Summarization ---")
    # 4. Instantiate the LLM for summarization
    llm_summarizer = LocalFastAPI_LLM(
        endpoint="http://127.0.0.1:8000/summarize/",
        response_key="summary_text"
    )

    # 5. Send a prompt to the LLM for summarization
    prompt_sum = """The quick brown fox jumps over the lazy dog. This is a classic pangram, a sentence that contains every letter of the alphabet at least once. Pangrams are often used to display typefaces or to test typing skills. They are also a fun linguistic exercise. Another famous pangram is "Pack my box with five dozen liquor jugs.""""
    response_sum = llm_summarizer.invoke(prompt_sum)

    print(f"Prompt (Summarization): {prompt_sum}")
    print(f"Response (Summarization): {response_sum}")