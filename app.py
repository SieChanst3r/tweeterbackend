import mariadb
from flask import Flask, request, Response, render_template, url_for, flash, redirect
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
import json
import dbcreds
import secrets


app = Flask(__name__)
CORS(app)

# from flask_wtf import FlaskForm
# from wtforms import StringField , PasswordField , SubmitField , BooleanField
# from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# app.config['SECRET_KEY'] = '966a98e7b6fd851217f6f90db9f0e1da'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/users.db'
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)

@app.route('/api/signup', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def queertrUsers():
    if request.method == 'GET':
        conn = None
        cursor = None
        user_id = request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            if user_id != None and user_id != "":
                cursor.execute("SELECT * FROM users WHERE id =?", [user_id])
            else:
                cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
        except mariadb.ProgrammingError:
            print("Something went wrong: Coding error ")        
            # print(error)
        except mariadb.OperationalError:
            print("uh oh, an Connection error occurred!")
        except mariadb.DatabaseError:
            print("A Database error interrupted your experience.. oops")
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
# NEED TO ADD IN THE ROW NUMBER FROM DATABASE FOR EACH ITEM IN THE USER_DATA OBJECT FIELD
            if(rows):
                all_users_data = []
                for row in rows:
                    user_data = {
                        "usersId" = row[],
                        "email" = row[],
                        "username" = row[],
                        "bio" = row[],
                        "DOB" = row[]
                    }
    if request.method == 'POST':
        conn = None
        cursor = None
        users_email = request.json.get("email")
        users_username = request.json.get("username")
        users_password = request.json.get("password")
        users_dob = request.json.get("DOB")
        users_bio = request.json.get("bio")
        rows = None

        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users(email, username, password, DOB, bio) VALUES (?, ?, ?, ?, ?)", [users_email, users_username, users_password, users_dob, users_bio])
            rows = cursor.rowcount

        if(rows == 1):
            loginTokin = secrests.token_hex(16)
            user_id = cursor.lastrowid
            print(loginTokin)
            cursor.execute("INSERT INTO user_session()")
            conn.commit()
            rows= cursor.amount
        except mariadb.ProgrammingError:
            print("Something went wrong: Coding error ")        
            # print(error)
        except mariadb.OperationalError:
            print("uh oh, an Connection error occurred!")
        except mariadb.DatabaseError:
            print("A Database error interrupted your QUEERTR experience.. oops")
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
            if(rows == 1):
                user_info = {
                    "usersId": user_id,
                    "email": users_email,
                    "username": users_username,
                    "bio": users_bio,
                    "DOB": users_dob,
                    "loginToken": loginToken
                }
                 return Response(json.dumps(user_info, default=str), mimetype="application/json", status=201)
            else:
                 return Response("Something went wrong!", mimetype="text/html", status=500)
 