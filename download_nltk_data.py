import nltk

# Ensure NLTK packages are downloaded
nltk_packages = ['wordnet', 'pros_cons', 'reuters']
for package in nltk_packages:
    nltk.download(package)
