FROM python:3.13-slim

# Work directory inside container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code (this will include app/, model/, etc.)
COPY . .

# Expose port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app
# NOTE: inside container, our package is just "app", not "backend.app"
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
