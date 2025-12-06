from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/greet", methods=["GET"])
def greet():
    name = request.args.get("name", "stranger")
    message = f"Hello, {name}! 👋"
    return jsonify({"greeting": message})

@app.route("/add", methods=["GET"])
def add_numbers():
    a = request.args.get("a", type=float, default=0)
    b = request.args.get("b", type=float, default=0)
    result = a + b
    return jsonify({"a": a, "b": b, "sum": result})

if __name__ == "__main__":
    app.run(debug=True)
