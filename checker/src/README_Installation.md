# Installation and starting the server

The goal of this project is to build a Python microservice, which provides detailed feedback to students solving exercises.

## Setup
Please set your working directory to the same directory as this file.

### Prerequisites
#### Software
The programming language [Python](https://www.python.org/downloads/) and the package manager [pip](https://pip.pypa.io/en/stable/installation/) (or alternatively [Anaconda](https://www.anaconda.com/download)) is required.

The Python version should not really matter as long as it is a relatively new one. This project was created with Python version 3.11.5. You should use a Python version >= 3.11.5.

In order to be able to display images, you additionally have to install [Graphviz](https://graphviz.org/) (on top having to install its Python library below).
You can find information on how to install it for your operating system at the [Graphviz download page](https://graphviz.org/download/).

#### Install packages
This project requires the following Python packages:
- Flask (for running the HTTP server)
- Graphviz (for generating PNG images of graphs)
- Pillow (for opening generated PNG images in an image viewer)

The dependencies and exact versions are present in `requirements.txt`
They can be installed directly using pip:
> pip install -r requirements.txt

### Flask Server

#### HTTP Routing

The `app.py` file serves as the main entry point for handling requests in the Flask application. It defines the available endpoints, processes incoming data, and returns a response. You should implement your endpoints as HTTP POST endpoints.

#### Start server

You can use Flask to start the HTTP server. We recommend running in debug mode, because this way the server automatically restarts when the code changes, so that you do not have to restart the server manually.
To start the HTTP server run the following command in the command line:
> flask run --debug

If the `flask` command cannot be located correctly, then you can also try:
> python -m flask run --debug

Upon success, an HTTP server starts on localhost. You can terminate it using CTRL+C in the terminal.

Since flask usually takes localhost port 5000, you will probably find your HTTP server there. Alternatively, look for the address in the terminal output. Usually it will look like this:
> * Running on http://127.0.0.1:5000

#### Send request to server
If the server runs you can send a request to the given server by e.g., using command line tools like CURL or other API tools like Postman/Insomnia. We will be talking later on about Postman/Insomnia.
You will have to perform a post request to the endpoint and pass the contents as a JSON body. More information to the specific requests can be found in the specific descriptions (README.md) for the ExampleList and your topic.