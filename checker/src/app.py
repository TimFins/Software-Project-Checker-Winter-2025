from flask import Flask, jsonify, request
from binarytrees import BinaryTreeNode, RedBlackTreeNode, RedBlackTreeColor
from evaluation import evaluate_binary_tree_task
import json


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return """<h1>Connection Established</h1><p>The HTTP Server is running. Please note, that in order to actually use this service, you have to send POST requests to the implemented routes.</p><p>This page serves no functional purpose.</p>"""


@app.route("/example-route", methods=["POST"])
def example_route():
    """Example route showcasing how a route should be handled.
    It takes the inputs, passes them to an evaluation function elsewhere and then answers with an example score and feedback.
    """
    print("A request has arrived!")
    data = request.get_json()

    # The JSON is parsed back into an object to maintain a unified interface
    # for validation. This is necessary because Kafka requests return a
    # JSON string, not a JSON object.
    print(data)
    if data.get("existingTree") is not None:
        data["existingTree"] = json.dumps(data["existingTree"])
    if data.get("studentTree") is not None:
        data["studentTree"] = json.dumps(data["studentTree"])

    print(data)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    try:
        score, feedback, solution = evaluate_binary_tree_task(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"score": score, "feedback": feedback, "solution": solution})


if __name__ == "__main__":
    app.run()
