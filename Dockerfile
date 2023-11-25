# First Stage (Builder Stage)
FROM python:3.8-slim


# Install build tools or dependencies
RUN apt-get update && apt-get install -y build-essential git && apt-get install tesseract-ocr -y

# Set working directory
WORKDIR /app

# Copy only files needed for the build
COPY requirements.txt .

# Install Python dependencies
RUN pip install uvicorn && pip install python-multipart && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && pip install --no-cache-dir -r requirements.txt

# Download necessary files
#RUN wget -O /app/layoutlmv2_model.pth https://example.com/path/to/your/model_files/layoutlmv2_model.pth

# Expose the port
EXPOSE 8080

# Copy the rest of your application code
COPY . .

# Command to run your application
CMD ["python", "-m", "uvicorn", "fast_api_app:app", "--reload","--host", "0.0.0.0", "--port", "8080"]
