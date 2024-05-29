# SNAP-SHOOT
Hosted on Heroku

Python Streamlit Heroku pre-commit Code style: browser

https://www.snap-shoot.com

A social search web application that uses the Openai to search internet. also include a creative section so people can create and make content findable. The application is built with Streamlit and deployed on Heroku using a GitHub action and Docker.


# Requirements:
To run this app you need to have:
an OpenAI API key and others Search Keys

Setup the streamlit secrets int the .streamlit/secrets.toml file:
EXA_API_KEY=""
OPENAI_API_KEY=""


# Instalation
Set up a virtual environment and install the requirements 
$ python3 -m venv venv

# To activate this environment, use: 
$ source venv/bin/activate
$ pip install -r requirements.txt

# To deactivate this environment, use:
$ source deactivate

si se necesita recrear requirements:
$ pip freeze > requirements.txt

en caso de  ERROR: Failed building wheel for chroma-hnswliben caso de export HNSWLIB_NO_NATIVE=1 despues  
$ pip install HNSWLIB 

# To run the app, use: 
$ streamlit run snap_app/1_🏠_Home.py
$ sh run.sh

# 🐳 Run App using Docker
Build your Docker image and specify your custom tag for the image with this command:
docker build -t snap-heroku-web-app:latest .
$ docker build -t streamlit .
$ docker images

Run the Docker container directly
docker run -d --name snap-heroku-web-app -p 8080:8080 snap-heroku-web-app 
$ docker run -p 8080:8080 streamlit
to see
> http://localhost:8080

Run the docker container using docker-compose (Recommended)
docker-compose up

# Step 6: Log into Heroku and create a new app on Heroku:

$ heroku login
$ heroku container:login

$ docker ps

heroku create <your-app-name>
$ heroku create snap-app-1

# Step 7: Push your Docker image to Heroku Container Registry and deploy your app!

docker tag <your-docker-image_tag>:latest registry.heroku.com/<your-app-name>/web:latest
$ docker tag streamlit:latest registry.heroku.com/snap-app-1/web:latest

docker push registry.heroku.com/<your-app-name>/web:latest
$ docker push registry.heroku.com/snap-app-1/web:latest

heroku container:release web --app <your-app-name>
$ heroku container:release web --app snap-app-1


# Connect Heroku to GitHub repo
heroku git:remote -a <your-app-name>
$ heroku git:remote -a snap-app-1

$ git push heroku master:main

=====

# Usage
streamlit run main.py
This will open a new tab in your default browser with the app running.

# Hosted version
We deployed this app using streamlit community cloud, you can access it here.
##
# Snap-Shoot web application

[![Python](https://img.shields.io/badge/Python-3.8-3776AB.svg?style=flat&logo=python&logoColor=FFDB4D)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B.svg?style=flat)](https://www.streamlit.io)
[![Heroku](https://img.shields.io/badge/Heroku-deployed-430098.svg?style=flat&logo=heroku)](https://www.heroku.com)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[**https://www.snap-shoot.com/**](https://www.snap-shoot.com/)

A web application that Discover and Create content using AI algorithms.
The application is built with [Streamlit](https://www.streamlit.io) and deployed on Heroku using a GitHub action and Docker.

---
