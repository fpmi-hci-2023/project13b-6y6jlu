from sqlalchemy import (
    create_engine,
    ForeignKey,
    Column,
    Integer,
    Float,
    String,
    and_,
    func,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///app_data.db", echo=True)

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "Author"
    auth_id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_date = Column(String)
    death_date = Column(String)


class Book(Base):
    __tablename__ = "Book"
    book_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("Author.auth_id"))
    name = Column(String)
    annotation = Column(String)
    rate = Column(Float)


class User(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    info = Column(String)
    book_challenge_id = Column(Integer, ForeignKey("BookChallenge.challenge_id"))


class BookChallenge(Base):
    __tablename__ = "BookChallenge"
    challenge_id = Column(Integer, primary_key=True)
    book_read = Column(Integer)
    book_want = Column(Integer)

class Collection(Base):
    __tablename__ = "Collection"
    collection_id = Column(Integer, primary_key=True)
    collection_name = Column(String)
    owner_id = Column(Integer, ForeignKey("User.user_id"))


class Comment(Base):
    __tablename__ = "Comment"
    comment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    txt = Column(String)
    date = Column(String)


class LoginData(Base):
    __tablename__ = "LoginData"
    login = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    password = Column(String)
    email = Column(String)


class Review(Base):
    __tablename__ = "Review"
    review_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    book_id = Column(Integer, ForeignKey("Book.book_id"))
    rate = Column(Float)
    txt = Column(String)
    date = Column(String)

    
class FriendList(Base):
    __tablename__ = "FriendList"
    user_id = Column(Integer, ForeignKey("User.user_id"), primary_key=True)
    friend_id = Column(Integer, ForeignKey("User.user_id"), primary_key=True)

class BookStatus(Base):
    __tablename__ = "BookStatus"
    book_id = Column(Integer, ForeignKey("Book.book_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), primary_key=True)
    status = Column(String)

class UserCollections(Base):
    __tablename__ = "UserCollections"
    user_id = Column(Integer, ForeignKey("User.user_id"), primary_key=True)
    collection_id = Column(Integer, ForeignKey("Collection.collection_id"), primary_key=True)


class BookCollection(Base):
    __tablename__ = "BookCollection"
    book_id = Column(Integer, ForeignKey("Book.book_id"), primary_key=True)
    collection_id = Column(String, ForeignKey("Collection.collection_id"), primary_key=True)

class img_path(Base):
    __tablename__ = "img_path"
    book_id = Column(Integer, primary_key=True)
    path = Column(String)
   