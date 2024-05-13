Snap : Hosted on Heroku

Python Streamlit Heroku pre-commit Code style: browser

https://www.snap-shoot.com

A social search web application that uses the Openai to search internet. also include a creative section so people can create and make content findable. The application is built with Streamlit and deployed on Heroku using a GitHub action and Docker.


Requirements:

To run this app you need to have:

an OpenAI API key
an Exa API key (there is a free tier available)

Instalation

Set up a virtual environment and install the requirements:
# $ python3 -m venv .venv

To activate this environment, use:
# $ source .venv/bin/activate

# $ pip install -r requirements.txt
(Nota: en caso de  ERROR: Failed building wheel for chroma-hnswliben caso de export HNSWLIB_NO_NATIVE=1 despues  pip install HNSWLIB )
To run the app, use: 
# $ streamlit run streamlit_app.py
# $ streamlit run snap_app/home.py
# $ sh run.sh

To deactivate this environment, use:
# $ source deactivate
To Remove

Setup the streamlit secrets int the .streamlit/secrets.toml file:

EXA_API_KEY=""
OPENAI_API_KEY=""
Usage

streamlit run main.py
This will open a new tab in your default browser with the app running.

Hosted version

We deployed this app using streamlit community cloud, you can access it here.
# Text summarization web application

[![Python](https://img.shields.io/badge/Python-3.8-3776AB.svg?style=flat&logo=python&logoColor=FFDB4D)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B.svg?style=flat)](https://www.streamlit.io)
[![Heroku](https://img.shields.io/badge/Heroku-deployed-430098.svg?style=flat&logo=heroku)](https://www.heroku.com)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[**https://textrank-summarizer.herokuapp.com/**](https://textrank-summarizer.herokuapp.com/)

A web application that Discover and Create content using AI algorithms.
The application is built with [Streamlit](https://www.streamlit.io) and deployed on Heroku using a GitHub action and Docker.

---

[![jhc github](https://img.shields.io/badge/GitHub-jhrcook-181717.svg?style=flat&logo=github)](https://github.com/jhrcook)
[![jhc twitter](https://img.shields.io/badge/Twitter-@JoshDoesA-00aced.svg?style=flat&logo=twitter)](https://twitter.com/JoshDoesa)
[![jhc website](https://img.shields.io/badge/Website-Joshua_Cook-5087B2.svg?style=flat&logo=telegram)](https://joshuacook.netlify.com)
