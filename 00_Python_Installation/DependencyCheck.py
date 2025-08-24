def test_graphviz():
    import base64
    from io import BytesIO
    dot: graphviz.Digraph = graphviz.Digraph()
    dot.attr("graph", center="True", dpi="300",
             label="If you are seeing this,\nThen GraphViz is correctly installed.", labelloc="t")
    dot.format = "png"
    # Get image as binary
    tree_binary = dot.pipe()
    # Encode binary image as Base64
    b64_image = base64.b64encode(tree_binary).decode("utf-8")
    img = Image.open(BytesIO(base64.b64decode(b64_image)))
    img.show()


try:
    import flask
    import graphviz
    from PIL import Image
    test_graphviz()
    print("Everything was successfully installed.")
except:
    try:
        import flask
        print("Flask package was installed successfully.")
    except:
        print("Flask package is not installed. Please run:")
        print("pip install Flask")

    try:
        import graphviz
        print("Graphviz package was installed successfully.")
        try:
            test_graphviz()
            print("The Graphviz program works.")
        except:
            print("The Graphviz program was not properly installed. Please visit:")
            print("https://graphviz.org/download/")
    except:
        print("Graphviz package is not installed. Please run:")
        print("pip install graphviz")

    try:
        import PIL
        print("Pillow package was installed successfully.")
    except:
        print("Pillow package is not installed. Please run:")
        print("pip install Pillow")
