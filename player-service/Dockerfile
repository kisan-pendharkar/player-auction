# Use Python 3.12 base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set working directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN apt-get update -y && \
    apt-get install -y \
        net-tools procps vim
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Run the FastAPI app with Uvicorn
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD [ "tail","-f" ,"/dev/null"]