# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# install uv
RUN pip install uv

# install deps
RUN uv pip install -r pyproject.toml --system

# run the project
CMD ["python", "worker/main.py"]