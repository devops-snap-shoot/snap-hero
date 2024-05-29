# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# These two environment variables prevent __pycache__/ files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /snap_app
COPY index.html /usr/local/lib/python:3.11/site-packages/streamlit/static/index.html

WORKDIR /snap_app

# Expose the port the app runs on
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

# Run the app
CMD ["streamlit", "run", "snap_app/1_🏠_Home.py", "--server.port=8501"]
