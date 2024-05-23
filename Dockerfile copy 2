# app/Dockerfile

# Base Image to use
FROM python:3.11-slim

# Change Working Directory to app directory
WORKDIR /snap_app

# Copy Requirements.txt file into app directory
COPY requirements.txt .

# Install all requirements in requirements.txt
RUN python -m pip install -r requirements.txt --no-cache-dir

# Copy all files in current directory into app directory
COPY . .

# Copy the specific index.html from the virtual environment to the appropriate place
COPY .venv/lib/python3.11/site-packages/streamlit/static/index.html /usr/local/lib/python3.11/site-packages/streamlit/static/index.html

# Expose port 8080
EXPOSE 8080

# Run the application on port 8080
CMD ["streamlit", "run", "--server.port", "8080", "snap_app/1_🏠_Home.py"]
