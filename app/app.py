import flask
import mysql.connector
from flask import request, jsonify
from typing import List, Dict
import json


app = flask.Flask(__name__)
app.config["DEBUG"] = True
books = [
    {
        "id": 1,
        "isbn": "9781593279509",
        "title": "Eloquent JavaScript, Third Edition",
        "subtitle": "A Modern Introduction to Programming",
        "author": "Marijn Haverbeke",
        "published": "2018-12-04T00:00:00.000Z",
        "publisher": "No Starch Press",
        "pages": 472,
        "description": "JavaScript lies at the heart of almost every modern web application, from social apps like Twitter to browser-based game frameworks like Phaser and Babylon. Though simple for beginners to pick up and play with, JavaScript is a flexible, complex language that you can use to build full-scale applications.",
        "website": "http://eloquentjavascript.net/"
    },
    {
        "id": 2,
        "isbn": "9781491943533",
        "title": "Practical Modern JavaScript",
        "subtitle": "Dive into ES6 and the Future of JavaScript",
        "author": "Nicolás Bevacqua",
        "published": "2017-07-16T00:00:00.000Z",
        "publisher": "O'Reilly Media",
        "pages": 334,
        "description": "To get the most out of modern JavaScript, you need learn the latest features of its parent specification, ECMAScript 6 (ES6). This book provides a highly practical look at ES6, without getting lost in the specification or its implementation details.",
        "website": "https://github.com/mjavascript/practical-modern-javascript"
    }
]


@app.route('/test', methods=['GET'])
def get_books():
    # Create a connection
    cnx = mysql.connector.connect(user='root', password='root', host='db', port='32000', database='mydatabase')

    # Create a cursor
    cursor = cnx.cursor()

    # Execute the SELECT query
    query = "SELECT * FROM books"
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Create a list to store the book data
    books = []

    # Process the fetched rows
    for row in rows:
        book_id = row[0]
        title = row[1]
        author = row[2]
        book = {
            'id': book_id,
            'title': title,
            'author': author
        }
        books.append(book)

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Return the book data as JSON response
    return jsonify(books)


@app.route('/', methods=['GET'])
def home() -> str:
    return '''<h1>VLib - Online Library</h1>
                <p>A flask api implementation for book information.   </p>'''


@app.route('/api/v1/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.route('/api/v1/books', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
        results = []
        for book in books:
            if book['id'] == id:
                results.append(book)
        return jsonify(results)
    else:
        return "Error: No id field provided. Please specify an id."


@app.route("/api/v1/books",  methods=['POST'])
def api_insert():
    book = request.get_json()
    books.append(book)
    return "Success: Book information has been added."


@app.route("/api/v1/books/<id>", methods=["DELETE"])
def api_delete(id):
    for book in books:
        if book['id'] == int(id):
            books.remove(book)
    return "Success: Book information has been deleted."


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
