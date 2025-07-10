from flask import Flask ,request,jsonify
from jsonschema import validate,ValidationError

app = Flask(__name__)
@app.route("/")
def home():
    return "Welcome to the Flask JSON API!"


books=[]

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

@app.route('/books',methods = ["GET"])

def get_books():
    return jsonify({"books":books}),2000

@app.route('/books',methods=["POST"])

def add_books():
  
 data = request.get_json()
 try:
      validate(instance=data,schema=book_schema)
 except ValidationError as e:
     return jsonify({"error":f"inavalid input:{e.message}"}),404
 
 books.append(data)
 return jsonify({"message":"Book added","book":data})

@app.route('/books/<int:index>',methods=["PUT"])
def update_book(index):
    if index >= len(books):
        return jsonify({"error":"book not found"}),404
    
    try:
        validate(instance=data,schema=book_schema)
    except ValidationError as e:
        return jsonify({"error":f"invalid input:{e.message}"})
    
    books[index] = data
    return jsonify({"message":"Book updated","book":data})

@app.route('/books/<int:index>',methods=["DELETE"])
def delete_book(index):
    if index>=len(books):
        return jsonify({"error":"book not found"}),404
    
  
    deleted = books.pop(index)
    return jsonify({"message":"book deleted","book":deleted})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)



