# Basic Authentication Implementation

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Hardcoded credentials for demonstration purposes
USERNAME = "admin"
PASSWORD = "password"

# Secret key for JWT encoding/decoding
SECRET_KEY = "mysecretkey"

class LoginRequest(BaseModel):
    username: str
    password: str

from datetime import datetime, timedelta
import jwt

@app.post("/login")
def login(request: LoginRequest):
    if request.username == USERNAME and request.password == PASSWORD:
        # Generate JWT token
        payload = {
            "sub": request.username,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"message": "Login successful", "token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
