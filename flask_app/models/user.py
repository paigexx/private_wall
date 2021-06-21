from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.messages = []

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        return connectToMySQL("private_wall").query_db(query)

    @classmethod
    def create_user(cls, data):
        query  = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("private_wall").query_db(query,data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL("private_wall").query_db(query, data)
        # if not email then add a conditional 
        if len(results) < 1:
            return False
        return cls(results[0])



    @staticmethod
    def validate(data):
        is_valid = True

        if len(data["first_name"]) <2 or not data["first_name"].isalpha(): 
            flash("Your first name must be longer than 2 characters of the English alphabet.", "first_name")
            is_valid = False

    
        if len(data["last_name"]) < 2 or not data["last_name"].isalpha(): 
            flash("Your first name must be longer than 2 characters.", "last_name")
            is_valid = False

        if User.get_by_email(data): 
            flash("Email address already exsits!")
            is_valid = False
        
        if not email_regex.match(data["email"]):
            flash("Please enter a valid email.", "email")
            is_valid = False

        if len(data["password"]) < 8:
            flash("Password must be 8 or more characters")
            is_valid = False

        if data["password"] != data["confirm_password"]:
            flash("Your passwords must match.", "password")
            is_valid = False


        return is_valid