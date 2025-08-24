# Setting Everything Up

## Installing Python
In this project we will build an evaluation microservice using the programming language Python.

For this you will have to install Python along with some dependencies. Please perform the following steps:
1. Install the [Python interpreter](https://www.python.org/downloads/) for your operating system. The version has to be >= 3.11.5 but the newest version also works. If asked whether you would also like to install "pip", then please do so.
2. Next you require the Python package manager "pip". If you have not already done so while installing Python, then you can download pip afterwards by following the steps outlined [here](https://pip.pypa.io/en/stable/installation/).

To confirm, that the installation is working, you could try to run the `HelloWorld.py` program. Click run in your IDE or try commands like `python3 HelloWorld.py`, `python HelloWorld.py` or `py HelloWorld.py`.

## Installing The Dependencies

1. Pip is used to download Python packages. This project requires the following packages:
    - **Flask** (for running the HTTP server)
    - **Graphviz** (for generating PNG images of graphs)
    - **Pillow** (for opening generated PNG images in an image viewer)
2. You can install all the packages individually or you can directly install them by inputting the `requirements.txt` file into the pip command, which tells pip which packages and versions you need. For that please run:
> pip install -r requirements.txt

If you get an error, that pip cannot be resolved to a command even though you installed it,
then try to run this instead:
> python3 -m pip install -r requirements.txt
3. In order to be able to display images, you additionally have to install the [Graphviz program](https://graphviz.org/) (**on top having to install its Python package!**).
You can find information on how to install it for your operating system at the [Graphviz download page](https://graphviz.org/download/).

To confirm whether you have successfully installed the required dependencies, you can run `DependencyCheck.py`. That program tells you whether you have the necessary packages.
