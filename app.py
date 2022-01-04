from book import *
from flask import Flask
import logging
from functools import wraps
from marshmallow import Schema, fields, ValidationError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

f = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
fh = logging.FileHandler("app.log")
fh.setFormatter(f)

logger.addHandler(fh)

class UserSchema(Schema):

    book_name = fields.String(required=True)
    book_author = fields.String(required=True)
    book_price = fields.Integer(required=True)
    book_category = fields.String(required=True)


def required_params(schema):
    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                schema.load(request.get_json())
            except ValidationError as err:
                error = {
                    "status": "error",
                    "messages": err.messages
                }
                return jsonify(error), 400
            return fn(*args, **kwargs)

        return wrapper

    return decorator




#creating an instance of flask app
app = Flask(__name__)


#route to add book details
@app.route("/add_book", methods=["POST"])
@required_params(UserSchema())
def add_book():
    '''Function to add new book details to our database'''
    logger.debug("Adding new book..")
    request_data = request.get_json() #getting data from client
    responce = Book.add_book(request_data, request.url)
    return responce

#route to show all books
@app.route("/show_books", methods=['GET'])
def show_all_books():
    '''function to show books data'''
    responce = Book.get_all_books()
    return responce

#route to show all book with book id
@app.route("/show_book/<int:id>", methods=['GET'])
def show_book(id):
    '''function to show book data'''
    responce = Book.get_book(id)
    return responce

#route to update book details
@app.route("/update_book/<int:id>", methods=["PUT"])
@required_params(UserSchema())
def update_book(id):
    '''Function to update existing book details to our database'''
    request_data = request.get_json() #getting data from client
    responce = Book.update_book(request_data, id, request.url)
    return responce

@app.route('/delete_book/<int:id>', methods=['DELETE'])
def delete_book(id):
    '''function to delete existing book data from our database'''
    request_data = request.get_json()  # getting data from client
    responce = Book.delete_book(id, request.url)
    return responce

if __name__=="__main__":
    app.run(port=5000, debug=True)