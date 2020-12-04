import mariadb
from flask import Flask, request, Response
from flask_cors import CORS
import json
import dbcreds
import secrets


app = Flask(__name__)
CORS(app)

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
                cursor.execute("SELECT t.id, t.userId, t.content, t.createdAt, u.username FROM tweet t INNER JOIN user u ON t.userId = u.id WHERE u.id = ?", [userId])
            else:
                cursor.execute("SELECT t.id, t.userId, t.content, t.createdAt, u.username FROM tweet t INNER JOIN user u ON t.userId = u.id")
            cursor.fetchall()
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
            if(rows != None):
                all_tweets = []
                for row in rows:
                    users_tweets = {
                        "tweetId": row[0],
                        "userId": row[],
                        "username": row[],
                        "content": row[],
                        "createdAt": row[]
                    }
                    all_tweets.append(users_tweets)
                return Response(json.dumps(all_tweets, default = str), mimetype="application/json", status=200)
            else:
                return Response("There was an error, please attempt this again shortly!", mimetype="text/html", status=500)
# POST tweets method:
    elif request.method == 'POST':
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        tweet_content = request.json.get("content")
        rows = None
        tweetId = None
        createdAt = datetime.datetime.now().strftime("%Y-%M-%D")
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT u.username, us.userId FROM user_session us INNER JOIN user u ON us.userId = u.id WHERE us.loginToken = ?", [loginToken,])
            user = cursor.fetchall()
            letter_length = len(tweet_content)
            if letter_length <= 255 and len(user) == 1:
                cursor.execute("INSERT INTO tweet(content, userId, createdAt) VALUES (?, ?, ?)", [tweet_content, user[0][0], createdAt])
                conn.commit()
                tweetId = cursor.lastrowid
            else:
                print("Max of 255 characters, Be carfeul QUEERTR!")
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
            if(tweetId != None):
                tweet_stuff = {
                    "tweetId": tweetId,
                    "userId": user[0][3],
                    "username": user[0][0],
                    "content": tweet_content,
                    "createdAt": createdAt
                }                
                return Response(json.dumps(tweet_stuff, default=str), mimetype="application/json", status=201)
            else:
                return Response("Uh oh, something went wrong here, lets try that again QUEERTR", mimetype="text/html", status=500)
    # PATCH request tweets:
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        row = None
        tweetId = request.json.get("tweetId")
        loginToken = request.json.get("loginToken")
        tweet_content = request.json.get("content")
        updated_tweet_stuffs = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()     
            cursor.execute("SELECT * FROM user_session WHERE loginToken = ?", [loginToken,])
            user = cursor.fetchall()
            # double bracket thing == confusion
            if user[0][1] == loginToken:
                cursor.execute("UPDATE tweet SET content = ? WHERE id =?", [tweet_content, tweetId])
                conn.commit()
            rows = cursor.rowcount
            cursor.execute("SELECT * FROM tweet WHERE id=?", [tweetId])
            updated_content = cursor.fetchall()
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
                #look at api documentation for this part:
                 updated_tweet_stuffs = {
                     "tweetId": updated_content[0][0],
                     "content": updated_content[0][2]
                 }
                 return Response(json.dumps(updated_tweet_stuffs, default=str), mimetype="application/json", status=200)
            else:
                return Response("oops, something errored here, please try again QUEERTR", mimetype="text/html", status=500)
    # DELETE method for tweets:
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        rows = None
        loginToken = request.json.get("loginToken")
        tweetId = request.json.get('tweetId')
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM user_session WHERE loginToken = ?", [loginToken,]")  
            user = cursor.fetchall()
            if user[0][1] == loginToken:
                cursor.execute("DELETE FROM tweet WHERE loginToken = ?", [loginToken])
                conn.commit()
                rows = cursor.rowcount
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
                return Response("Very good, Your QUEERTR post has been deleted!", mimetype="text/html", status=204)
            else:
                return Repsonse("Oh my, something did not go as planned here... attempt again please!", mimetype="text/html", status=500)
# Tweet-like methods:
@app.route('/api/tweet-likes', methods=['GET', 'POST', 'DELETE'])
def tweetLikesEndpoint():
    # GET tweet-likes:
    if request.method == 'GET':
        conn = None
        cursor = None
        tweetId = request.args.get("tweetId")
        likes = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor() 
            cursor.execute("SELECT tweet_like.tweet_id, tweet_like.user_id, user.username FROM tweet_like INNER JOIN user ON user.id = tweet_like.user_id WHERE tweet_like.tweet_id = ?", [tweetId])
            likes = cursor.fetchall()     
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
            if(likes != None):
                user_data = []
                for like in likes:
                    likes_info = {
                        "tweetId": like[2],
                        "userId": like[1],
                        "username": like[0]
                    }  
                    user_data.append(likes_info)
                return Response(json.dumps(user_data, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong here, please try again!", mimetype="text/html", status=500)   
    #POST tweet-like method:
    elif request.method == 'POST':
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        tweetId = request.json.get("tweetId")
        rows = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()   
            cursor.execute("SELECT * FROM user_session WHERE loginToken = ?", [loginToken])
            user_liking = cursor.fetchall()
            if user_liking[0][1] == loginToken:
                cursor.execute("INSERT INTO tweet_like(tweet_id, user_id) VALUES(?, ?)", [tweet_id, user_liking[0][1],])
                conn.commit()
                rows = cursor.fetchall()
            else:
                return Response("There was an error! Please try again.", mimetype="text/html", status=400)
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
            if(rows != None):
                return Response("Tweet liked, very good!", mimetype="text/html", status=201)
            else:
                return Response("Something went terribly wrong here, try again shortly.", mimetype="text/html", status=500)

    #DELETE tweet like method:
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        tweetId = request.json.get("tweetId")
        rows = None
        if user_unliking [0][1] == loginToken:
            cursor.execute("DELETE FROM tweet_like WHERE tweet_id = ?", [tweet_id, user_unliking[0][2]])
            print(user_unliking)
            conn.commit()
            rows = cursor.fetchall()
        else:
            return Response("There was an error, please try again.", mimetype="text/html", status=400)
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
            if(rows != None):
                return Response("Tweet unliked, very good!", mimetype="text/html", status=204)
            else:
                return Response("Something went wrong, please try again.", mimetype="text/html", status=500)

# comments methods:
@app.route('/api/comments', methods=['GET', 'POST', 'PATCH', 'DELETE']) 
def commentsEndpoint():
    if request.method == 'GET':
        conn = None 
        cursor = None
        tweetId = request.args.get("tweetId")
        comment_content = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor() 
            if tweetId != None and tweetId != "":
                cursor.execute("SELECT comment.*, user.username FROM comment INNER JOIN user ON comment.userId WHERE comment.tweetId = ?", [tweetId])
                comment_content = cursor.fetchall()
            elif tweetId == None and tweetId != "":
                cursor.execute("SELECT * FROM comment")
                comment_content = cursor.fetchall()
            else:
                return Response("Oh my, something did not go as planned here... attempt again please!", mimetype="text/html", status=200)
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
            if(comment_info != None):
                comment_stuffs = []
                for comment in comment_info:
                    comment_stuffs = {
                        "commentId": comment[2],
                        # how do you get the tweet id here???:
                        "tweetId": comment[3],
                        "userId": comment[0],
                        "username": comment[5],
                        "content": comment[4],
                        "createdAt": comment[6]
                    }
                    all_tweets.append(users_tweets)
                return Response(json.dumps(all_tweets, default = str), mimetype="application/json", status=200)
            else:
                return Response("There was an error, please attempt this again shortly!", mimetype="text/html", status=500)
    # POST for comments:
    elif request.method == 'POST':  
        conn = None 
        cursor = None
        tweetId = request.json.get("tweetId")
        loginToken = request.json.get("loginToken")
        comment_data = request.json.get("content")
        createdAt = datetime.datetime.now().strftime("%Y-%M-%D")
        recent_comment_userId = None
        rows = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()             
            cursor.execute("SELECT * FROM user_session WHERE loginToken = ?", [loginToken])
            user_new_comment = cursor.fetchall()
            char_num = len(comment_data) 
            rows = cursor.rowcount
            if user_new_comment[0][4] == loginToken and char_num <= 150:
                cursor.execute("INSERT INTO comment(content, tweetId, createdAt, userId) VALUES (?, ?, ?, ?)", [comment_content, createdAt, tweetId, user_new_comment[0][2]])     
                recent_comment_userId = cursor.lastrowid
                conn.commit()
                rows = cursor.rowcount
                cursor.execute("SELECT comment.*, user.username FROM comment INNER JOIN user ON user.id = comment.userId WHERE comment.id =?", [recent_comment_userId,])
                recent_comment_userId = cursor.fetchall()
                return Response("Comment succesfully posted!", mimetype="text/html", status=201)
            else: 
                return Response("Error when posting comment, it needs to be at least 150 characters!", mimetype="text/html", status=400)    
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
                comment_info = {
                    "commentId": recent_comment_userId,
                    "tweetId": tweetId,
                    "userId": user_new_comment[0][0]
                    "username": recent_comment_userId[0][0]
                }
                return Response(json.dumps(comment_data, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something did not go as planned here.. please try again.", mimetype="text/html", status=500)
    # PATCH comments method:
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        rows = None
        loginToken = request.json.get("loginToken")
        commentId = request.json.get("commentId")
        comment_content = request.json.get("content")
        createdAt = datetime.datetime.now(). strftime("%Y-%M-%D")
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken = ?", [loginToken,])
            user_updating_comment = cursor.fetchall()
            cursor.execute("SELECT userId FROM comment WHERE id = ?", [commentId,])
            comment_owner = cursor.fetchall()
            if user_updating_comment[0][4] == loginToken and user_updating_comment[0][2] == comment_owner[0][0]:
                cursor.execute("UPDATE comment SET content = ? WHERE id = ?", [comment_content, commentId])
                conn.commit()
                rows = cursor.rowcount
            else:
                return Response("Sorry, only the owner of this comment can alter the content.", mimetype="text/html", status=400)
            if(rows != None):
                cursor.execute("SELECT comment.*, user.username FROM user INNER JOIN comment ON user.id = comment.userId WHERE comment.id = ?", [commentId,])
                user_new_comment = cursor.fetchall()
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
                comment_content = {
                    "commentId": commentId,
                    "tweetId": user_comment[0][3],
                    "userId": user_comment[0][0]
                    "username": user_comment[0][5],
                    "content": comment_content,
                    "createdAt": createdAt

                }
                return Repsonse(json.dumps(comment_content, default=str), mimetype="application/json", status=200)
            else:
                return Response("Oops, something went wrong here! Try again.", mimetype="text/html", status=500)
    # DELETE Comment:
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        commentId = request.json.get("commentId")
        rows = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken = ?", [loginToken])
            user_deleting_comment = cursor.fetchall()
            cursor.execute("SELECT userId FROM comment WHERE id = ?", [commentId,])
            comment_owner = cursor.fetchall()
            if user_deleting_comment[0][4] == loginToken and user_deleting_comment[0][2] == comment_owner[0][0]:
                cursor.execute("DELETE FROM comment WHERE id = ?", [commentId,])
                conn.commit()
                rows = cursor.rowcount
            else:
                return Response("You are not authorized to delete this comment, sorry.", mimetype="text/html", status=400)
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
            if(rows != None):
                return Response("Comment deleted!", mimetype="text/html", status=204)
            else:
                return Response("Something went bad here, we should try again!", mimetype="text/html", status=500)

@app.route('/api/comment-likes', methods=['GET', 'POST', 'DELETE'])
def commentLikesEndpoint():
    # GET comment likes:
    if request.method == 'GET':
        conn = None
        cursor = None
        commentId = request.json.get("commentId")
        likes = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT comment_like.commentId, comment_like.userId, user.username FROM comment_like INNER JOIN user ON user.id = comment_like.userId WHERE comment_like.commentId = ?", [commentId])
            likes = cursor.fetchall()
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
            if(likes != None):
                user_data = []
                for like in likes:
                    likes_info = {
                        "commentId": like[4],
                        "userId": like[3],
                        "username": like[0]
                    }  
                    user_data.append(likes_info)
                return Response(json.dumps(user_data, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong here, please try again!", mimetype="text/html", status=500)
    # POST comment-like:
    elif request.method == 'POST':
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        commentId = request.json.get("commentId")
        rows = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_session WHERE loginToken = ?", [loginToken])
            user_liking = cursor.fetchall()
            # print(user_liking) 
            if user_liking[0][3] == loginToken:
                cursor.execute("INSERT INTO comment_like(commentId, userId) VALUES(?, ?)", [commentId, user_liking[0][3]])
                conn.commit()
                rows = cursor.rowcount
            else:
                return Response("There was an Error, try again!", mimetype="text/html", status=400)
            cursor.execute("SELECT comment_like.*, user.username FROM comment_like INNER JOIN user ON user.id = comment_like.userId WHERE comment_like.commentId = ?", [commentId,])
            likes = cursor.fetchall()
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
            if(rows != None):
                return Response("Liked!", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong here..", mimetype="text/html", status=500)
    # DELETE Comment_like:
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        commentId = request.json.get("commentId")
        rows = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM user_session WHERE loginToken = ?", [loginToken,])
            user_unliking = cursor.fetchall()
            # print(user_unliking)
            cursor.execute("SELECT userId FROM comment_like WHERE commentId = ?", [commentId])
            like_owner = cursor.fetchall()
            # print(like_owner)
            if user_unliking[0][3] == loginToken:
                cursor.execute("DELETE FROM comment_like WHERE commentId = ? AND userId = ?", [commentId, user_unliking])
                conn.commit()
                rows = cursor.rowcount
            else:
                return Response("You cannot unlike something that isn't yours!", mimetype="text/html", status=400)
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
            if(rows != None):
                return Response("Unliked!", mimetype="text/html", status=204)
            else:
                return Response("Oops, something happened here and it did not work.. Please try again!", mimetype="text/html", status=500)   

    #Endpoint for follows (GET, POST, DELETE): 
@app.route('/api/follows', method=['GET', 'POST', 'DELETE'])
def followsEndpoint():
    # GET follows method:
    if request.method == 'GET':
        conn = None
        cursor = None
        userId = request.args.get("userId")
        follows = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()   
            cursor.execute("SELECT f.followId, u.email, u.username, u.bio, u.birthdate FROM follow f INNER JOIN user u ON u.id = f.follow.id WHERE f.userId = ?", [userId,])
            follows = cursor.fetchall()
            print(follow)
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
            if(follows != None):
                user_data = []
                for follow in follows:
                    user_following_info = {
                        "userId": follow[1],
                        "email": follow[5],
                        "username": follow[0],
                        "bio": follow[2],
                        "birthdate": follow[1]
                    }
                    user_data.append(user_following_info)
                return Response(json.dumps(user_data, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something did not go right, try again!", mimetype="text/html", status=500)

    elif request.method == 'POST':
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        followId = request.json.get("followId")
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor() 
            cursor.execute("SELECT userId FROM user_session WHERE loginToken = ?", [loginToken,])
            user_making_follow = cursor.fetchall()
            if user_making_follow[0][0] == followId:
                cursor.execute("INSERT INTO follow(followId, userId) VALUES(?, ?)", [followId, user_making_follow[0][0],])
                conn.commit()
                rows = cursor.fetchall()
            else:
                return Response("You can only follow other users.", mimetype="text/html", status=400)
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
                return Response("Followed user, very good!", mimetype="text/html", status=204)
            else:
                return Response("Something went wrong here, please try again shortly.", mimetype="text/html", status=500)

    elif request.method == 'DELETE':
        conn = None
        cursor = None
        loginToken = request.json.get("loginToken")
        followId = request.json.get("followId")
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()          

    # Endpoint for followers (GET, POST, DELETE):
@app.route('/api/followers', methods=['GET', 'POST', 'DELETE'])
def followersEndpoint():
    # GET followers method:
    if request.method == 'GET':
        conn = None
        cursor = None
        userId = request.json.get("userId")
        try:
            conn = mariadb.connect(host = dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor() 

    
    