from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI()

# Load Hugging Face models
# Using a small GPT-2 model for text generation
generator = pipeline("text-generation", model="distilgpt2")
# Using a small BART model for summarization
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Request body for text generation
class GenerationRequest(BaseModel):
    text: str

# Request body for text summarization
class SummarizationRequest(BaseModel):
    text: str

@app.post("/generate/")
async def generate_text(request: GenerationRequest):
    """
    Generates text based on a given prompt using a Hugging Face model.
    """
    # Generate text, limiting to 50 new tokens for simplicity and speed
    # You can adjust max_new_tokens as needed
    generated_output = generator(request.text, max_new_tokens=50, num_return_sequences=1, return_full_text=False)

    # The output is a list of dictionaries, extract the generated text
    generated_text = generated_output[0]['generated_text'].strip()

    return {"generated_text": generated_text}

@app.post("/summarize/")
async def summarize_text(request: SummarizationRequest):
    """
    Summarizes text using a Hugging Face summarization model.
    """
    # Summarize text, limiting min_length and max_length for simplicity
    # You can adjust these parameters as needed
    summary_output = summarizer(request.text, max_length=150, min_length=30, do_sample=False)

    # The output is a list of dictionaries, extract the summary text
    summary_text = summary_output[0]['summary_text'].strip()

    return {"summary_text": summary_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
