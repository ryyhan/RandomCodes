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
            "exp": datetime.utcnow() + timedelta(hours=1),
            "role": "user",  # Example role
            "permissions": ["read", "write"]  # Example permissions
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"message": "Login successful", "token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/verify-token")
def verify_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"message": "Token is valid", "data": decoded_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/refresh-token")
def refresh_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        new_payload = {
            "sub": decoded_token["sub"],
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        new_token = jwt.encode(new_payload, SECRET_KEY, algorithm="HS256")
        return {"message": "Token refreshed successfully", "token": new_token}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/user-info")
def user_info(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"message": "User information retrieved successfully", "user": decoded_token["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/logout")
def logout(token: str):
    # Simulate token invalidation (e.g., by adding it to a blacklist)
    return {"message": "User logged out successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
