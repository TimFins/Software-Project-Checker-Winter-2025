from flask import Flask, jsonify, request
from evaluation import evaluate_list_sorting_task, evaluate_avl_tree_task, evaluate_priority_queue_task

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return """<h1>Connection Established</h1><p>The HTTP Server is running. Please note, that in order to actually use this service, you have to send POST requests to the implemented routes.</p><p>This page serves no functional purpose.</p>"""


@app.route("/example-list-evaluation", methods=["POST"])
def example_route():
    """Example route showcasing how a route should be handled.
    It takes the inputs, passes them to an evaluation function elsewhere and then answers with an example score and feedback.
    """
    print("A request has arrived!")
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    try:
        score, feedback, solution = evaluate_list_sorting_task(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"score": score, "feedback": feedback, "solution": solution})


@app.route("/avl-tree-evaluation", methods=["POST"])
def evaluate_avl_tree_route():
    print("A request has arrived!")
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    try:
        score, feedback, solution = evaluate_avl_tree_task(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"score": score, "feedback": feedback, "solution": solution})


@app.route("/priority-queue-evaluation", methods=["POST"])
def evaluate_priority_queue_route():
    print("A request has arrived!")
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    try:
        score, feedback, solution = evaluate_priority_queue_task(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"score": score, "feedback": feedback, "solution": solution})


if __name__ == "__main__":
    app.run()
