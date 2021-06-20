from flask_bcrypt import Bcrypt
from flask_app import app
from flask import redirect, request, render_template, flash, session
from flask_app.models.user import User  
from flask_app.models.message import Message
bcrypt = Bcrypt(app) 

@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/user/reg", methods=["POST"])
def registration():
    print("validating the user input")

    # validate data
    if not User.validate(request.form):
        print('not valid')
        return redirect("/")

    # hash the password
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    
    # create the data for the query
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }

    print(request.form)
    # call the function to create a user which will return the users.id generated for the db
    user_id = User.create_user(data)
    flash("Thank you for registering. Please login!")
    # store the id in session for log in 
    return redirect("/")
    
    
  

@app.route("/user/login", methods=["POST"])
def login():
    # get user by email in db and check if email is in db. If not prompt to register
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    print(user_in_db)
    if not (user_in_db):
        flash("We don't recognize that email. Please register!")
        return redirect("/")
    # check to see that given password matches in db (compare hash)
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Password invalid. Please try again - unless you're a hacker ;)")
        return redirect("/")
    # if valid let the user log into the wall 
    session["first_name"] = user_in_db.first_name
    session["id"] = user_in_db.id
    print("id in session")
    return redirect("/user/display")


@app.route("/user/display")
def display_wall():
    # get all the users for the message display 
    users = User.get_all_users()
    data = {
        "id": session["id"]
    }
    messages = Message.get_messages(data)
    print(messages)
    return render_template("wall.html", users = users, messages = messages)

@app.route("/user/send_message", methods = ["POST"])
def add_message_to_db():
    user_id = session["id"]
    data = {
        "message": request.form["message"],
        "user_id": session["id"],
        "reciever_id": request.form["reciever_id"]
    }

    Message.create_message(data)
    print("######")
    print("your message was created!!")
    return redirect("/user/display")
    

@app.route("/user/delete_message", methods=["POST"])
def delete_message():
    
    print(request.form["message_id"])
    data = {
        "message_id": request.form["message_id"]
    }
    Message.delete_message(data)
    return redirect("/user/display")



@app.route("/user/logout")
def logout():
    session.clear()
    return redirect("/")

