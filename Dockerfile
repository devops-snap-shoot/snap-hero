# app/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Copy the local directory contents into the container.
COPY . /app

RUN pip install -r requirements.txt

# Make port variable available at runtime
ARG PORT=8501
ENV PORT $PORT
EXPOSE $PORT

CMD ["sh", "-c", "streamlit run --server.port $PORT snap-app/1_🏠_Home.py"]
