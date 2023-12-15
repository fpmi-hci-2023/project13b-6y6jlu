import flask
import mysql.connector
from flask import request, jsonify
from typing import List, Dict
from flasgger import Swagger
import json
from DBHelper import *

Session = sessionmaker(bind=engine)

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SWAGGER"] = {"title": "API Documentation", 
                         "description": "API for forWords app", 
                         "version": "0.0.1", 
                         "termsOfService" : ''}
swagger = Swagger(app)

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
        "website": "http://eloquentjavascript.net/",
    },
    {
        "id": 2,
        "isbn": "9781491943533",
        "title": "Practical Modern JavaScript",
        "subtitle": "Dive into ES6 and the Future of JavaScript",
        "author": "Nicolas Bevacqua",
        "published": "2017-07-16T00:00:00.000Z",
        "publisher": "O'Reilly Media",
        "pages": 334,
        "description": "To get the most out of modern JavaScript, you need learn the latest features of its parent specification, ECMAScript 6 (ES6). This book provides a highly practical look at ES6, without getting lost in the specification or its implementation details.",
        "website": "https://github.com/mjavascript/practical-modern-javascript",
    },
]


@app.route("/test", methods=["GET"])
def get_books():
    """
    Get all books.
    ---
    responses:
      200:
        description: A list of books.
    """
    # Create a connection
    cnx = mysql.connector.connect(
        user="root", password="root", host="db", port="32000", database="mydatabase"
    )

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
        book = {"id": book_id, "title": title, "author": author}
        books.append(book)

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Return the book data as JSON response
    return jsonify(books)


@app.route("/", methods=["GET"])
def home():
    """
    Home page 
    """
    return """<h1>VLib - Online Library</h1>
                <p>A flask api implementation for book information.   </p>"""


@app.route("/api/v1/books/all", methods=["GET"])
def api_all():
    """
    Get all books.
    ---
    responses:
      200:
        description: A list of books.
    """
    return jsonify(books)


@app.route("/api/v1/books", methods=["GET"])
def api_id():
    """
    Get a book by its ID.
    ---
    parameters:
      - name: id
        in: query
        type: integer
        required: true
        description: The ID of the book.
    responses:
      200:
        description: The book with the specified ID.
      404:
        description: Book not found.
    """
    if "id" in request.args:
        id = int(request.args["id"])
        results = []
        for book in books:
            if book["id"] == id:
                results.append(book)
        return jsonify(results)
    else:
        return "Error: No id field provided. Please specify an id."


@app.route("/api/v1/books", methods=["POST"])
def api_insert():
    """
    Insert a new book.
    ---
    parameters:
      - name: book
        in: body
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The ID of the book.
            isbn:
              type: string
              description: The ISBN of the book.
            title:
              type: string
              description: The title of the book.
            subtitle:
              type: string
              description: The subtitle of the book.
            author:
              type: string
              description: The author of the book.
            published:
              type: string
              format: date-time
              description: The publication date of the book.
            publisher:
              type: string
              description: The publisher of the book.
            pages:
              type: integer
              description: The number of pages in the book.
            description:
              type: string
              description: The description of the book.
            website:
              type: string
              description: The website of the book.
          required:
            - id
            - title
            - author
    responses:
      200:
        description: Book information has been added successfully.
    """
    book = request.get_json()
    books.append(book)
    return "Success: Book information has been added."


@app.route("/api/v1/books/<id>", methods=["DELETE"])
def api_delete(id):
    """
    Delete a book by its ID.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the book.
    responses:
      200:
        description: Book information has been deleted successfully.
      404:
        description: Book not found.
    """
    for book in books:
        if book["id"] == int(id):
            books.remove(book)
    return "Success: Book information has been deleted."


#book

#search book by name   
@app.route("/api/v1/books/search/title", methods=["POST"])
def api_search_by_name():
    data = request.json
    book = data["name"]
    with Session() as session:
        query = session.query(Book.id).filter(Book.name.like('%title%'))
        result = query.all()
        for row in result:
            print(row.id)
        session.commit()


            
#search book by id   
@app.route("/api/v1/books/search/id", methods=["POST"])
def api_search_by_id():
    data = request.json
    book_id = data["book_id"]
    with Session() as session:
        book = session.query(Book).get(book_id)
        if book is not None:
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}")
        else:
            print("Книга не найдена.")
        session.commit()



#add book into collection
@app.route("/api/v1/books/collection", methods=["POST"])
def api_add_into_collection():
    data = request.json
    book_id = data["book_id"]
    collection_id = data["collection_id"]
    with Session() as session:
        book_collection = BookCollection(book_id=book_id, collection_id=collection_id)
        session.add(book_collection)
        session.commit()


#change book status
# NOT SURE

@app.route("/api/v1/books/book_status", methods=["POST"])
def api_add_into_collection():
    data = request.json
    book_id = data["book_id"]
    user_id = data["user_id"]
    status = data["status"]
    
    with Session() as session:
        existing_status = session.query(BookStatus).filter_by(user_id=user_id, book_id=book_id).first()
        if existing_status:
            existing_status.status = status
        else:
            new_status = BookStatus(user_id=user_id, book_id=book_id, status=status)
            session.add(new_status)

        session.commit()



#collections

#create new collection
@app.route("/api/v1/books/new_collection", methods=["POST"])
def api_create_new_collection():
    data = request.json
    collection_id = data["collection_id"]
    collection_name = data["collection_name"]
    owner_id = data["owner_id"]
    with Session() as session:
        new_collection = Collection(collection_name=collection_name, collection_id=collection_id, owner_id=owner_id)
        session.add(new_collection)
        session.commit()
    
    
#create new user collection
@app.route("/api/v1/books/new_collection", methods=["POST"])
def api_create_new_collection():  
    data = request.json
    user_id = data["user_id"]
    collection_id = data["collection_id"]
    with Session() as session:
        new_collection = UserCollections(collection_id=collection_id, user_id=user_id)
        session.add(new_collection)
        session.commit()
    
#get all user collections
@app.route("/api/v1/books/all_user_collections", methods=["POST"])
def api_get_all_user_collections():
    data = request.json
    user_id = data["user_id"]
    with Session() as session:
        query = session.query(UserCollections.collection_id).get(UserCollections.user_id)
        result = query.all()
        for row in result:
            print(row.collection_id)
        session.commit()
    

#get all book from collection
@app.route("/api/v1/books/all_collection_books", methods=["POST"])
def get_all_books_collection():
    data = request.json
    collection_id = data["collection_id"]
    with Session() as session:
        query = session.query(BookCollection.collection_id).get(BookCollection.book_id)
        result = query.all()
        for row in result:
            print(row.collection_id)
        session.commit()


# add new friend
@app.route("/api/v1/books/friend_list", methods=["POST"])
def add_new_friend():
    data = request.json
    user_id = data["user_id"]
    friend_id = data["friend_id"]
    with Session() as session:
        z1 = FriendList(user_id=user_id, friend_id=friend_id)
        z2 = FriendList(user_id=friend_id, friend_id=user_id)
        session.add(z1)
        session.add(z2)
        session.commit()
        
# register
@app.route("/api/v1/books/registration", methods=["POST"])
def new_register():
    data = request.json
    login = data["login"]
    user_id = data["user_id"]
    password = data["password"]
    email = data["email"]
    with Session() as session:
        log = LoginData(login=login, user_id=user_id, password=password, email=email)
        session.add(log)
        session.commit()
        
# user
@app.route("/api/v1/books/new_user", methods=["POST"])
def new_user():
    data = request.json
    name = data["name"]
    user_id = data["user_id"]
    info = info["info"]
    with Session() as session:
        us = User(name=name, user_id=user_id, info=info, book_challenge_id=user_id)
        bc = BookChallenge(challenge_id=user_id, book_read=0, book_want=0)
        session.add(bc)
        session.add(us)
        session.commit()
        
# book challenge
@app.route("/api/v1/books/book_challenge_read", methods=["POST"])
def update_books_to_read():
    data = request.json
    book_read = data["book_read"]
    with Session() as session:
        existing_status = session.query(BookChallenge).filter_by(challenge_id=challenge_id).first()
        if existing_status:
            existing_status.book_read = book_read
        session.commit()


@app.route("/api/v1/books/book_challenge_want", methods=["POST"])
def update_books_want():
    data = request.json
    book_want = data["book_want"]
    with Session() as session:
        existing_status = session.query(BookChallenge).filter_by(challenge_id=challenge_id).first()
        if existing_status:
            existing_status.book_want = book_want
        session.commit()    




if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
  # with Session() as session:
  #     result = session.query(Book).join(Author).all()
  #     print(result[0].name)
