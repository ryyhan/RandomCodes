from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

# Define a Pydantic model for the request body
class GenerateRequest(BaseModel):
    prompt: str
    max_length: int = 50

# Load tiny GPT-2 model and tokenizer
model_name = "sshleifer/tiny-gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.get("/")
async def root():
    return {"message": "LLM API is running"}

@app.post("/generate")
async def generate_text(request: GenerateRequest):
    try:
        prompt = request.prompt
        max_length = request.max_length

        # Tokenize the input prompt
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        # Generate a single response
        outputs = model.generate(
            inputs.input_ids,
            max_length=max_length,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            temperature=0.7
        )

        # Decode and return the generated text
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"generated_text": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
