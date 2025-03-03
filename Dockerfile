FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the ports
EXPOSE 8000 8501

# Install Ollama
RUN apt-get update && apt-get install -y wget
RUN wget https://apt.ollama.ai/key.txt -O - | apt-key add -
RUN echo "deb https://apt.ollama.ai/ stable main" > /etc/apt/sources.list.d/ollama.list
RUN apt-get update && apt-get install -y ollama

# Download the model
RUN ollama pull qwen2.5-coder:0.5b

# Command to start the backend and frontend
CMD ollama serve & uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run app/frontend/app.py --server.port 8501 --server.address 0.0.0.0