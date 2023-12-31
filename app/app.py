import flask
import mysql.connector
from flask import request, jsonify, send_from_directory
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


#book

#get all books
@app.route("/api/v1/books/all", methods=["POST"])
def api_get_all_books():
    """
    Retrieve all books.

    ---
    tags:
      - Books
    responses:
      200:
        description: A list of books.
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Book'
    """
    book_list = []
    with Session() as session:
        books = session.query(Book).all()
        for book in books:
            author = session.query(Author).get(book.author_id)
            img = session.query(img_path).get(book.book_id)
            auth_name = ''
            if author is not None:
                auth_name = author.name
            book_dict = {
            'book_id': book.book_id,
            'author' : auth_name,
            'name' : book.name,
            'path' : img.path}
            book_list.append(book_dict)
        return  json.dumps(book_list, ensure_ascii=False)

#search book by name
@app.route("/api/v1/books/search/title", methods=["POST"])
def api_search_by_name():
    """
    Search books by name.

    ---
    tags:
      - Books
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
            example:
              title: "Harry Potter"
    responses:
      200:
        description: A list of books matching the search query.
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Book'
    """
    data = request.json
    title = data
    book_list = []
    with Session() as session:
        books = session.query(Book).filter(Book.name.like(f'%{title}%')).all()
        for book in books:
            author = session.query(Author).get(book.author_id)
            img = session.query(img_path).get(book.book_id)
            auth_name = ''
            if author is not None:
                auth_name = author.name
            book_dict = {
            'book_id': book.book_id,
            'author' : auth_name,
            'name' : book.name,
            'path' : img.path}
            book_list.append(book_dict)
        return json.dumps(book_list, ensure_ascii=False)



#search book by id
@app.route("/api/v1/books/search/id", methods=["POST"])
def api_search_by_id():
    """
    Search book by ID.

    ---
    tags:
      - Books
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              book_id:
                type: string
            example:
              book_id: "1"
    responses:
      200:
        description: The book details if found.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Book'
      404:
        description: Book not found.
        content:
          application/json:
            schema:
              type: object
    """
    data = request.json
    book_id = data
    with Session() as session:
        book = session.query(Book).get(book_id)
        if book is not None:
            auth_id = book.author_id
            author = session.query(Author).get(auth_id)
            img = session.query(img_path).get(book.book_id)
            auth_name = ''
            if author is not None:
                auth_name = author.name
            response = {
            'book_id': book.book_id,
            'author' : auth_name,
            'name' : book.name,
            'annotation' : book.annotation,
            'rate': book.rate,
            'path' : img.path}
            return json.dumps(response, ensure_ascii=False)
        else:
            print("Книга не найдена.")
        session.commit()
    response = {}
    return json.dumps(response, ensure_ascii=False)


# NEED CHECK
#add book into collection
@app.route("/api/v1/books/collection", methods=["POST"])
def api_add_into_collection():
    """
    Add a book into a collection.

    ---
    tags:
      - Books
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              book_id:
                type: string
              collection_id:
                type: string
            example:
              book_id: "1"
              collection_id: "2"
    responses:
      200:
        description: Book added successfully to the collection.
      400:
        description: Invalid request body or missing data.
    """
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
def api_add_into_collection2():
    """
    Add or update book status in user's collection.

    ---
    tags:
      - Books
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              book_id:
                type: string
              user_id:
                type: string
              status:
                type: string
            example:
              book_id: "1"
              user_id: "2"
              status: "completed"
    responses:
      200:
        description: Book status added or updated successfully.
      400:
        description: Invalid request body or missing data.
    """
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
    """
    Create a new collection.

    ---
    tags:
      - Collections
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              collection_id:
                type: string
              collection_name:
                type: string
              owner_id:
                type: string
            example:
              collection_id: "1"
              collection_name: "My Books"
              owner_id: "2"
    responses:
      200:
        description: Collection created successfully.
      400:
        description: Invalid request body or missing data.
    """
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
def api_create_new_user_collection():
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

def checkCredentials(username, password=None):
    """
    Check user credentials.

    If only username is provided, check if the username exists.
    If both username and password are provided, check if the username and password match.

    ---
    tags:
      - Authentication
    parameters:
      - name: username
        in: path
        description: Username of the user
        required: true
        schema:
          type: string
      - name: password
        in: query
        description: Password of the user
        required: false
        schema:
          type: string
    responses:
      200:
        description: Credentials are valid.
        content:
          application/json:
            schema:
              type: integer
              description: User ID if credentials are valid, -1 otherwise.
      400:
        description: Invalid request parameters.
    """
    if password is None:
        with Session() as session:
            results = session.query(LoginData).filter(LoginData.login == username).all()
        if len(results) > 0:
            return -1
        else:
            return 0
    else:
        with Session() as session:
            results = session.query(LoginData).filter(and_(LoginData.login == username, LoginData.password == password)).all()
        if len(results) != 1:
            return -1
        else:
            return results[0].user_id



# register
@app.route("/api/v1/books/registration", methods=["POST"])
def new_register():
    data = request.json
    with Session() as session:
        login = data["login"]
        user_id = session.query(func.max(LoginData.user_id)).first()[0]+1
        password = data["password"]
        email = data["email"]
        name = data["name"]
        info = info["info"]
        response = {}
        if checkCredentials(username=login) == -1:
            response = {'success': False, 'message': 'User with same name already exists.', 'userId': None}
            return json.dumps(response, ensure_ascii=False)
        log = LoginData(login=login, user_id=user_id, password=password, email=email)
        us = User(name=name, user_id=user_id, info=info, book_challenge_id=user_id)
        bc = BookChallenge(challenge_id=user_id, book_read=0, book_want=0)
        session.add(log)
        session.add(us)
        session.add(bc)
        session.commit()
        response = {'success': True, 'message': 'Register and login successful!', 'userId': user_id}
        return json.dumps(response, ensure_ascii=False)



@app.route("/api/v1/books/signIn", methods=["POST"])
def signIn():
    """
    Sign in with username and password.

    ---
    tags:
      - Authentication
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              login:
                type: string
              password:
                type: string
            example:
              login: "my_username"
              password: "my_password"
    responses:
      200:
        description: Sign-in successful.
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
                userId:
                  type: integer
      400:
        description: Invalid request body or missing data.
    """
    username = request.json.get('login')
    password = request.json.get('password')
    current_user_id = checkCredentials(username=username, password=password)

    if current_user_id != -1:
        response = {'success': True, 'message': 'Login successful!', 'userId': current_user_id}
    else:
        response = {'success': False, 'message': 'Invalid username or password.', 'userId': None}
    return json.dumps(response, ensure_ascii=False)



# book challenge
@app.route("/api/v1/books/book_challenge_read", methods=["POST"])
def update_books_to_read():
    """
    Update the number of books read in a challenge.

    ---
    tags:
      - Challenges
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              challenge_id:
                type: string
              book_read:
                type: integer
            example:
              challenge_id: "1"
              book_read: 5
    responses:
      200:
        description: Challenge updated successfully.
      400:
        description: Invalid request body or missing data.
    """
    data = request.json
    book_read = data["book_read"]
    with Session() as session:
        existing_status = session.query(BookChallenge).filter_by(challenge_id=challenge_id).first()
        if existing_status:
            existing_status.book_read = book_read
        session.commit()


@app.route("/api/v1/books/book_challenge_want", methods=["POST"])
def update_books_want():
    """
    Update the number of books read in a challenge.

    ---
    tags:
      - Challenges
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              challenge_id:
                type: string
              book_read:
                type: integer
            example:
              challenge_id: "1"
              book_read: 5
    responses:
      200:
        description: Challenge updated successfully.
      400:
        description: Invalid request body or missing data.
    """
    data = request.json
    book_want = data["book_want"]
    with Session() as session:
        existing_status = session.query(BookChallenge).filter_by(challenge_id=challenge_id).first()
        if existing_status:
            existing_status.book_want = book_want
        session.commit()


# get all user books
@app.route("/api/v1/books/get_user_books", methods=["POST"])
def get_all_user_books():
    data = request.json
    user_id = data
    book_list = []
    with Session() as session:
        query = session.query(BookStatus).filter(BookStatus.user_id == user_id).all()
        for q in query:
            book_id = q.book_id
            book = session.query(Book).get(book_id)
            author = session.query(Author).get(book.author_id)
            img = session.query(img_path).get(book.book_id)
            auth_name = ''
            if author is not None:
                auth_name = author.name
            book_dict = {
            'book_id': book.book_id,
            'author' : auth_name,
            'name' : book.name,
            'status' : q.status,
            'path' : img.path}
            book_list.append(book_dict)
    return json.dumps(book_list, ensure_ascii=False)

@app.route("/api/v1/books/user", methods=["POST"])
def get_user_info():
    data = request.json
    user_id = data
    with Session() as session:
        query = session.query(User).filter(User.user_id == user_id).first()
        user_dict = {
            'name' : query.name,
            'info': query.info
            }
    return json.dumps(user_dict, ensure_ascii=False) 

@app.route("/images")
def showImg():
    """
    Retrieve book information and image path.

    ---
    tags:
      - Books
    responses:
      200:
        description: Book information and image path retrieved successfully.
        content:
          application/json:
            schema:
              type: object
              properties:
                book_id:
                  type: integer
                author:
                  type: string
                name:
                  type: string
                annotation:
                  type: string
                rate:
                  type: float
                path:
                  type: string
      404:
        description: Book not found.
    """
    with Session() as session:
        book = session.query(Book).get(1)
        if book is not None:
            auth_id = book.author_id
            author = session.query(Author).get(auth_id)
            img = session.query(img_path).get(book.book_id)
            auth_name = ''
            if author is not None:
                auth_name = author.name
            response = {
            'book_id': book.book_id,
            'author' : auth_name,
            'name' : book.name,
            'annotation' : book.annotation,
            'rate': book.rate,
            'path' : img.path}
            return json.dumps(response, ensure_ascii=False)


@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory('images', filename)


#@app.route("/")
#def showHomePage():
#    return "This is home page"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
