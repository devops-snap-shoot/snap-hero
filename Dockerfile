#Base Image to use
ARG PYTHON_IMAGE=python:<python-version>-slim

FROM ${PYTHON_IMAGE}

#Change Working Directory to app directory
WORKDIR /app

#Copy Requirements.txt file into app directory
COPY requirements.txt .

#install all requirements in requirements.txt
RUN python -m pip install -r requirements.txt --no-cache-dir

#Copy all files in current directory into app directory
COPY . .
COPY index.html /usr/local/lib/python3.11/site-packages/streamlit/static/index.html

#Expose port 8080
EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

#Run the application on port 8080
CMD ["streamlit", "run", "snap_app/Home.py"]