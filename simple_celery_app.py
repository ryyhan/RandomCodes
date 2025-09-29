from celery import Celery

# Create a Celery instance
app = Celery('simple_app', broker='redis://localhost:6379/0')

# Define a simple task
@app.task
def add(x, y):
    return x + y

if __name__ == "__main__":
    # Example usage
    result = add.delay(4, 6)
    print(f"Task submitted. Task ID: {result.id}")
