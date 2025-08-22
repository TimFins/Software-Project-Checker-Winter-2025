# Setup
Please set your working directory to the same directory as this file.

## Prerequisites
### Software
The programming language [Python](https://www.python.org/downloads/) and the package manager [pip](https://pip.pypa.io/en/stable/installation/) (or alternatively [Anaconda](https://www.anaconda.com/download)) is required.

The Python version should not really matter as long as it is a relatively new one. This project was created with Python version 3.11.5. You should use a Python version >= 3.11.5.

In order to be able to display images, you additionally have to install [Graphviz](https://graphviz.org/) (on top having to install its Python library below).
You can find information on how to install it for your operating system at the [Graphviz download page](https://graphviz.org/download/).

### Install packages
This project requires the following Python packages:
- Flask (for running the HTTP server)
- Graphviz (for generating PNG images of graphs)
- Pillow (for opening generated PNG images in an image viewer)

The dependencies and exact versions are present in `requirements.txt`
They can be installed directly using pip:
> pip install -r requirements.txt