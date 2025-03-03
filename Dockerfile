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

# Command to start the backend and frontend
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run app/frontend/app.py --server.port 8501 --server.address 0.0.0.0