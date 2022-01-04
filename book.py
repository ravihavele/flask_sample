import pymysql
from app import *
from db import mysql
from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

f = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
fh = logging.FileHandler("book.log")
fh.setFormatter(f)

logger.addHandler(fh)


def nofound(self,_request_url):
    message = {
        'status': 404,
        'message': 'Not Found: ' + _request_url,
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

# the class Book will create object for employee details
class Book:

    def add_book(_json,_request_url):
        conn = None
        cursor = None

        _book_name = _json["book_name"]
        _book_author = _json["book_author"]
        _book_price = _json["book_price"]
        _book_category = _json["book_category"]


        try:
            # validate the received values
            if _book_name and _book_author and _book_price and _book_category and request.method == 'POST':
                # save edits
                sql = "INSERT INTO tbl_book(book_name,book_author,book_price,book_category) VALUES(%s, %s, %s , %s)"
                data = (_book_name, _book_author, _book_price, _book_category,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('Book details added successfully!')
                logger.debug("Book details successfully added to database...")
                resp.status_code = 200
                return resp
            else:
                logger.critical("Issue with book details addition...")
                return nofound(_request_url)
        except Exception as e:
            logger.critical("Issue with book details addition..." + str(e))
            print(e)
        finally:
            cursor.close()
            conn.close()

    def get_all_books():
        conn = None
        cursor = None
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT book_id Id,book_name Name,book_author Author,book_price Price,"
                           "book_category Category FROM tbl_book")
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            logger.debug("fetching book details from database...")
            return resp
        except Exception as e:
            logger.critical("Issue with fetching book details from database..." + str(e))
            print(e)
        finally:
            cursor.close()
            conn.close()

    def get_book(_id):
        conn = None
        cursor = None
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT book_id Id,book_name Name,book_author Author,book_price Price,"
                           "book_category Category"
                           "FROM tbl_book where book_id="+str(_id))
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            logger.debug("fetching specific book details from database...")
            return resp
        except Exception as e:
            logger.critical("Issue with fetching book details from database..." + str(e))
            print(e)
        finally:
            cursor.close()
            conn.close()

    def update_book(_json,_book_id,_request_url):
        conn = None
        cursor = None

        _book_name = _json["book_name"]
        _book_author = _json["book_author"]
        _book_price = _json["book_price"]
        _book_category = _json["book_category"]

        try:
            # validate the received values
            if _book_name and _book_author and _book_price and _book_category and request.method == 'PUT':
                # save edits
                sql = "Update tbl_book SET book_name=%s,book_author=%s,book_price=%s,book_category=%s where book_id=%s"
                data = (_book_name, _book_author, _book_price, _book_category,_book_id,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('Book details updated successfully!')
                logger.debug("Book details successfully updated to database...")
                resp.status_code = 200
                return resp
            else:
                logger.critical("Issue with book details updating...")
                return nofound(_request_url)
        except Exception as e:
            logger.critical("Issue with book details updating..." + str(e))
            print(e)
        finally:
            cursor.close()
            conn.close()

    def delete_book(_id,_request_url):
        conn = None
        cursor = None
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tbl_book WHERE book_id=%s", (_id,))
            conn.commit()
            resp = jsonify('Book details deleted successfully!')
            resp.status_code = 200
            logger.debug("Book details successfully deleted from database...")
            return resp
        except Exception as e:
            logger.critical("Issue with book details deletion..." + str(e))
            print(e)
        finally:
            cursor.close()
            conn.close()

