# Serving Local Hugging Face Models with FastAPI and LangChain Integration

## Abstract

This project demonstrates a robust and scalable architecture for serving local Hugging Face transformer models via a FastAPI-based REST API. It further showcases the integration of these local endpoints as custom Language Learning Models (LLMs) within the LangChain framework. This approach enables the creation of powerful, self-hosted NLP applications that can leverage the extensive capabilities of both Hugging Face for model deployment and LangChain for building complex LLM-powered workflows. The system is designed with a clear separation of concerns, where FastAPI handles efficient model inference and LangChain provides a high-level abstraction for interacting with the models.

## System Architecture

The system is composed of two primary components:

1.  **FastAPI Server (`localhostLLM.py`)**: This server is responsible for loading and managing the Hugging Face models. It exposes two endpoints:
    *   `/generate/`: Accepts a text prompt and returns generated text using a text-generation model (e.g., `distilgpt2`).
    *   `/summarize/`: Accepts a block of text and returns a summarized version using a summarization model (e.g., `sshleifer/distilbart-cnn-12-6`).

2.  **LangChain Integration (`langchain_integration.py`)**: This module provides a client-side implementation for interacting with the FastAPI server. It defines two custom LLM classes that inherit from LangChain's `LLM` base class:
    *   `CustomLLM`: A wrapper for the `/generate/` endpoint.
    *   `CustomSummarizer`: A wrapper for the `/summarize/` endpoint.

This decoupled architecture allows for independent development, scaling, and maintenance of the model-serving API and the LangChain application logic.

```
+--------------------------------+      +--------------------------------+
|      LangChain Application     |      |         FastAPI Server         |
| (langchain_integration.py)     |      |        (localhostLLM.py)       |
+--------------------------------+      +--------------------------------+
|                                |      |                                |
|  CustomLLM (for generation)    |----->|  POST /generate/               |
|                                |      |  (distilgpt2)                  |
+--------------------------------+      +--------------------------------+
|                                |      |                                |
|  CustomSummarizer              |----->|  POST /summarize/              |
|  (for summarization)           |      |  (distilbart-cnn-12-6)         |
+--------------------------------+      +--------------------------------+
```

## Setup and Installation

1.  **Clone the repository or download the files.**

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the FastAPI Server:**
    Open a terminal and run the following command from the `localhostLLM` directory:
    ```bash
    uvicorn localhostLLM:app --host 0.0.0.0 --port 8000
    ```
    The server will start and load the Hugging Face models into memory.

2.  **Run the LangChain Integration Script:**
    In a separate terminal, run the `langchain_integration.py` script:
    ```bash
    python langchain_integration.py
    ```
    This script will demonstrate how to use the custom LLM classes to interact with the FastAPI server for both text generation and summarization.

## Code Explanation

### `localhostLLM.py`

This script sets up the FastAPI server and the Hugging Face model pipelines.

-   **FastAPI App Initialization**: An instance of `FastAPI` is created.
-   **Model Loading**: The `transformers.pipeline` function is used to load the `distilgpt2` model for text generation and the `sshleifer/distilbart-cnn-12-6` model for summarization. These models are loaded once when the application starts, ensuring efficient inference.
-   **Pydantic Models**: `GenerationRequest` and `SummarizationRequest` are Pydantic models that define the expected request body for the API endpoints, providing data validation and serialization.
-   **API Endpoints**:
    -   `@app.post("/generate/")`: This endpoint handles text generation. It takes a `GenerationRequest` object, passes the text to the `generator` pipeline, and returns the generated text. The `return_full_text=False` parameter is used to ensure that only the newly generated text is returned.
    -   `@app.post("/summarize/")`: This endpoint handles text summarization. It takes a `SummarizationRequest` object, passes the text to the `summarizer` pipeline, and returns the summarized text.

### `langchain_integration.py`

This script demonstrates how to integrate the local FastAPI endpoints with LangChain.

-   **Custom LLM Classes**:
    -   `CustomLLM` and `CustomSummarizer` inherit from `langchain.llms.base.LLM`.
    -   The `_call` method is implemented to make a POST request to the respective FastAPI endpoint (`/generate/` or `/summarize/`). It handles the request payload and parses the JSON response.
    -   The `_llm_type` property provides a unique identifier for the custom LLM class.
-   **Example Usage (`if __name__ == "__main__":`)**:
    -   Instances of `CustomLLM` and `CustomSummarizer` are created.
    -   The `invoke` method is called on each instance to send a prompt to the local LLM server and receive the response.

## Conclusion and Future Work

This project provides a foundational framework for serving and integrating local Hugging Face models within a modern Python application stack. The combination of FastAPI and LangChain offers a powerful and flexible solution for building sophisticated NLP-driven services.

Potential areas for future work include:

-   **Model Caching**: Implement a caching mechanism to store the results of frequent requests, reducing inference time.
-   **Asynchronous Processing**: For longer-running generation or summarization tasks, consider using FastAPI's background tasks or a dedicated task queue (e.g., Celery) to handle requests asynchronously.
-   **Scalability**: Deploy the FastAPI server using a production-ready ASGI server like Gunicorn with multiple worker processes to handle concurrent requests.
-   **Error Handling**: Enhance the error handling in both the client and server to provide more informative error messages.
-   **Model Management**: Develop a system for dynamically loading and unloading different Hugging Face models without restarting the server.
