# Use a slim Python 3.9 image to minimize size
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Expose Streamlit port (default 8501)
EXPOSE 8501

# Run Streamlit app in foreground
CMD ["streamlit", "run", "app.py"]
