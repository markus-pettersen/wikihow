# wikiHow Article Network Explorer

A Natural Language Processing Project that clusters wikiHow articles into broad topics and builds a topic map using semantic similarity and network analysis.

This project combines **clustering**, **topic modelling** and **network analysis** to explore wikiHow articles.

## Features

### Overview

- **TF-IDF vectorization** and **SVD** for dimensionality reduction.
- **K-means clustering** to group articles by topic.
- **NMF** to extract topic keywords for interpretation.
- **Cosine similarity** to connect semantically similar articles into a network.
- **NetworkX** and **Pyvis** to analyse and visualize relationships.

### Key Features

- Explores relationships between articles to identify redundant articles.
- Creates either a balanced or specialised corpus by selecting a wide range of articles or from a cluster.
- Helps create user-guides or LLM training data.
- Fully interactive dashboard to enable deeper exploration.

## Skills Demonstrated

- Text preprocessing and feature extraction.
- Unsupervised machine learning.
- Graph theory and network analysis.
- Dashboard creation with **Streamlit** and **Pyvis**.
- Data storytelling and modularization.

## Limitations & Future work

- No synonyms detection (from spaCy for example).
- In the future, I will identify the prototypical article from each topic/cluster.
- Future improved dashboard features.
- **Agglutinative clustering** to create a topic hierarchy for the articles.

## Links

- [First Jupyter Notebook](https://github.com/markus-pettersen/wikihow/blob/main/notebooks/01_intro_and_vectorization.ipynb) 
- [Dashboard](https://wikihow-network.streamlit.app/)
- [wikiHow](https://www.wikihow.com/Main-Page)
- [Kaggle Dataset](https://www.kaggle.com/datasets/elfarouketawil/wikihow-featured-articles/)

 ### Author

**Markus Saint-Pettersen**

[Github](http://github.com/markus-pettersen) [LinkedIn](linkedin.com/in/m-saint-pettersen)
