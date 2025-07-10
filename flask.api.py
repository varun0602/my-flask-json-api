from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
import os

app = Flask(__name__)
@app.route("/")
def home():
    return "Welcome to the Flask JSON API!"


books = []

# JSON schema validation
book_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "author": {"type": "string"},
        "price": {"type": "number"},
        "in_stock": {"type": "boolean"}
    },
    "required": ["title", "author", "price"],
    "additionalProperties": False
}

@app.route("/")
def home():
    return "✅ Flask JSON API is running!"

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify({"books": books}), 200

@app.route("/books", methods=["POST"])
def add_books():
    data = request.get_json()
    try:
        validate(instance=data, schema=book_schema)
    except ValidationError as e:
        return jsonify({"error": f"invalid input: {e.message}"}), 400

    books.append(data)
    return jsonify({"message": "Book added", "book": data}), 201

@app.route("/books/<int:index>", methods=["PUT"])
def update_book(index):
    if index >= len(books):
        return jsonify({"error": "book not found"}), 404

    data = request.get_json()
    try:
        validate(instance=data, schema=book_schema)
    except ValidationError as e:
        return jsonify({"error": f"invalid input: {e.message}"}), 400

    books[index] = data
    return jsonify({"message": "Book updated", "book": data}), 200

@app.route("/books/<int:index>", methods=["DELETE"])
def delete_book(index):
    if index >= len(books):
        return jsonify({"error": "book not found"}), 404

    deleted = books.pop(index)
    return jsonify({"message": "book deleted", "book": deleted}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)




