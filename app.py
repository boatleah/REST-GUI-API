from flask import Flask, jsonify
from flask import Flask, request, jsonify, abort
 
books = [
    {"id": 1, "title": "1984", "author": "George Orwell",  "rating": 4.9},
    {"id": 2, "title": "Brave New World","author": "Aldous Huxley",  "rating": 4.3},
    {"id": 3, "title": "Fahrenheit 451","author": "Ray Bradbury",   "rating": 4.7},
    #My favorite book
    {"id": 4, "title": "Harry Potter and the Chamber of Secrets", "author": "J.K. Rowling", "rating": 4.8}
]

app = Flask(__name__)
 
@app.route('/')
def welcome():
    return jsonify(message='Welcome to Tiny REST App!')

#TODO add remaining code here when instructed below…

@app.route('/goodbooks', methods=['GET'])
def get_books():
    return jsonify(books) , 200

from flask import abort
 
@app.route('/goodbooks/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        abort(404, description="Book not found")
    return jsonify(book) , 200

from flask import request
 
@app.route('/goodbooks', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data or "title" not in data or "author" not in data:
        abort(400, description="Missing required fields")
    new_id = max(b["id"] for b in books) + 1 if books else 1
    book = {
        "id": new_id,
        "title": data["title"],
        "author": data["author"],
        "rating": data.get("rating", 0)
    }
    books.append(book)
    return jsonify(book), 201


@app.route('/goodbooks/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        abort(404, description="Book not found")
    book.update({k: v for k, v in data.items() if k in ["title", "author", "rating"]})
    return jsonify(book)

@app.route('/goodbooks/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    if not any(b["id"] == book_id for b in books):
        abort(404, description="Book not found")
    books = [b for b in books if b["id"] != book_id]
    return '', 204

from flask import render_template_string
 
TABLE_TEMPLATE = """
<!doctype html>
<title>Book List</title>
<h1>Books</h1>
<table border=1 cellpadding=5 cellspacing=0>
  <tr><th>ID</th><th>Title</th><th>Author</th><th>Rating</th></tr>
  {% for book in books %}
	<tr style="background-color: {{ 'lightgreen' if book.rating >= 4.8 else 'white' }}">
  	<td>{{ book.id }}</td>
  	<td>{{ book.title }}</td>
  	<td>{{ book.author }}</td>
  	<td>{{ book.rating }}</td>
	</tr>
  {% endfor %}
</table>
"""
 
@app.route('/goodbooks/html')
def books_html():
	return render_template_string(TABLE_TEMPLATE, books=books)



if __name__ == '__main__':
    app.run(debug=True)


