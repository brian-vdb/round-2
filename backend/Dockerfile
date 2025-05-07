# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# If you have a requirements.txt
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

CMD ["python", "app.py"]
