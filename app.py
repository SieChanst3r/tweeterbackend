import mariadb
from flask import Flask, request, Response
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
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/user.db'
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)

# Login/Logout:
@app.route('/api/login', methods=['POST', 'DELETE'])

def queertrLoginOut():
    if request.method == 'POST':
        conn = None
        cursor = None
        user_email = request.json.get("email")
        user_password = request.json.get("password")
        rows = None
        user = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE email = ? AND password = ?", [user_email, user_password,])
            user = cursor.fetchall()
            rows = cursor.rowcount
            if(rows == 1):
                loginToken = secrets.token_hex(16)
                cursor.execute("INSERT INTO user_session(userId, loginToken) VALUES(?, ?)", [user[0][0], loginToken])
                conn.commit()
        except Exception as error:
            print(error)
        except mariadb.ProgrammingError as error:
            print("Something went wrong: Coding error ")        
            print(error)
        except mariadb.OperationalError as error:
            print("uh oh, an Connection error occurred!")
            print(error)
        except mariadb.DatabaseError as error:
            print("A Database error interrupted your experience.. oops")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
            if(rows == 1):
                return Response("Login success!", mimetype = "text/html", status=201)
            else:
                return Response("Something went really wrong here, try again..", mimetype="text/html", status=500)
    # Logout:
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        rows = None
        userId = request.json.get("id")
        loginToken = request.json.get("loginToken")      
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_session WHERE loginToken = ?", [loginToken])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print(error)
        except mariadb.ProgrammingError as error:
            print("Something went wrong: Coding error ")        
            print(error)
        except mariadb.OperationalError as error:
            print("uh oh, an Connection error occurred!")
            print(error)
        except mariadb.DatabaseError as error:
            print("A Database error interrupted your experience.. oops")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
            if(rows == 1):
                return Response("Logout success!", mimetype = "text/html", status=201)
            else:
                return Response("Something went really wrong here, try again..", mimetype="text/html", status=500)


@app.route('/api/users', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def queertrUsers():
    if request.method == 'GET':
        conn = None
        cursor = None
        user_id = request.args.get("user_id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            if user_id != None and user_id != "":
                cursor.execute("SELECT * FROM user WHERE id =?", [user_id])
            else:
                cursor.execute("SELECT * FROM user")
            rows = cursor.fetchall()
            print(user_id)
        except Exception as error:
            print(error)
        except mariadb.ProgrammingError as error:
            print("Something went wrong: Coding error ")        
            print(error)
        except mariadb.OperationalError as error:
            print("uh oh, an Connection error occurred!")
            print(error)
        except mariadb.DatabaseError as error:
            print("A Database error interrupted your experience.. oops")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
# NEED TO ADD IN THE ROW NUMBER FROM DATABASE FOR EACH ITEM IN THE USER_DATA OBJECT FIELD
            if(rows):
                all_user_data = []
                for row in rows:
                    user_data = {
                        "userId": row[4],
                        "email": row[5],
                        "username": row[0],
                        "bio": row[2],
                        "birthdate": row[1]
                    }
                    all_user_data.append(user_data)
                return Response(json.dumps(all_user_data, default = str), mimetype = "application/json", status = 200)
            else:
                return Response("Something went really wrong here, please try again..", mimetype = "text/html", status = 500)
    elif request.method == 'POST':
        conn = None
        cursor = None
        user_email = request.json.get("email")
        user_username = request.json.get("username")
        user_password = request.json.get("password")
        user_birthdate = request.json.get("birthdate")
        user_bio = request.json.get("bio")
        rows = None

        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user(email, username, password, birthdate, bio) VALUES (?, ?, ?, ?, ?)", [user_email, user_username, user_password, user_birthdate, user_bio])
            rows = cursor.rowcount

        if(rows == 1):
            loginToken = secrets.token_hex(16)
            user_id = cursor.lastrowid
            print(loginToken)
            cursor.execute("INSERT INTO user_session()")
            conn.commit()
            rows= cursor.amount
        except mariadb.ProgrammingError as error:
            print("Something went wrong: Coding error ")        
            print(error)
        except mariadb.OperationalError as error:
            print("uh oh, an Connection error occurred!")
            print(error)
        except mariadb.DatabaseError as error:
            print("A Database error interrupted your QUEERTR experience.. oops")
            print(error)
        except Exception as error:
            print(error)

        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
            if(rows == 1):
                user_data = {
                    "userId": user_id,
                    "email": user_email,
                    "username": user_username,
                    "bio": user_bio,
                    "birthdate": user_birthdate,
                    "loginToken": loginToken
                }
                 return Response(json.dumps(user_data, default=str), mimetype="application/json", status=201)
            else:
                 return Response("Something went wrong!", mimetype="text/html", status=500)
    # UPDATE user info:
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        rows = None
        user_email = request.json.get("email")
        user_username = request.json.get("username")
        user_bio = request.json.get("bio")
        user_birthdate = request.json.get("birthdate")
        user_password = request.json.get("password")
        loginTokin = request.json.get("loginToken")
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT userId FROM user_session WHERE loginToken = ?", [loginToken])
            user_successful = cursor.fetchone()
            if user_successful:
                if(user_email != "" and user_email != None):
                    cursor.execute("UPDATE user SET email = ? WHERE id = ?", [user_email, user_successful[0],])
                if(username != "" and username != None):
                    cursor.execute("UPDATE user SET username =? WHERE id = ?", [user_username, user_successful[0],])
                if(user_bio != "" and user_bio != None):
                    cursor.execute("UPDATE user SET bio =? WHERE id = ?", [user_bio, user_successful[0],])
                if(user_birthdate != "" and user_birthdate != None):
                    cursor.execute("UPDATE user SET birthdate = ? WHERE id = ?", [user_birthdate, user_successful[0],])
                if(user_password != "" and user_password != None):
                    cursor.execute("UPDATE user SET password = ? WHERE id =?", [user_password, user_successful[0],])
                conn.commit()
                rows = cursor.rowcount
                cursor.execute("SELECT * FROM user WHERE id =?", [user_successful[0],])
                user = cursor.fetchall()
        except mariadb.ProgrammingError as error:
            print("Something went wrong: Coding error ")        
            print(error)
        except mariadb.OperationalError as error:
            print("uh oh, an Connection error occurred!")
            print(error)
        except mariadb.DatabaseError as error:
            print("A Database error interrupted your QUEERTR experience.. oops")
            print(error)
        except Exception as error:
            print(error)

        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
            if(rows == None):
                # do the below have to match table names as well as accessing the correct array and row????
                user_data = {
                    "userId": user_successful[0],
                    "email": user[0][5],
                    "username": user[0][0],
                    "bio": user[0][2],
                    "birthdate": user[0][1]
                }
                return Response(json.dumps(user_data, default=str), mimetype="text/html", status=200)
            else:
                return Response(json.dumps(user_data, default=str), mimetype="text/html", status=500)
    # user DELETE:
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        user_password = request.json.get("password")
        loginToken = request.json.get("loginToken")
        rows = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken =?", [loginToken,])
            user = cursor.fetchall()
            if user[0][4] == loginToken:
                cursor.execute("DELETE FROM user WHERE id = ? AND password = ?", [user[0][3], user_password])
                conn.commit()
                rows = cursor.rowcount
            else:
                return Response("There was an error in the information you providedd, please try again", mimetype="text/html",status=500)
        except mariadb.ProgrammingError as error:
            print("Something went wrong: Coding error ")        
            print(error)
        except mariadb.OperationalError as error:
            print("uh oh, an Connection error occurred!")
            print(error)
        except mariadb.DatabaseError as error:
            print("A Database error interrupted your QUEERTR experience.. oops")
            print(error)
        except Exception as error:
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
            if(rows == 1):
                return Response("Account successfully deactivated!", mimetype="text/html", status=204)
            else:
                return Response("There was an error, please attempt this again shortly!", mimetype="text/html", status=500)
@app.route('/api/tweets', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def userTweets():
    # GET request: use params and request.args here:
    if request.method == 'GET':
        conn = None
        cursor = None
        userId = request.args.get("userId")
        rows = None
        tweet_stuff = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor() 
            if userId != None and userId != "":          
 