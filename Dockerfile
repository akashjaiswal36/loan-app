FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]

EXPOSE 5000

# This Dockerfile sets up a Python environment for a web application.
# It installs dependencies from requirements.txt, copies the application code,