import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import redirect

class Message: 
    def __init__(self, data):
        self.id = data["id"]
        self.message = data["message"]
        self.user_id = data["user_id"]
        self.reciever_id = data["reciever_id"]


    @classmethod
    def create_message(cls, data):
        query = "INSERT INTO messages (message, user_id, reciever_id) VALUES ( %(message)s, %(user_id)s, %(reciever_id)s);"

        return connectToMySQL("private_wall").query_db(query,data)

    @classmethod
    def get_messages(cls, data):
        query =  "SELECT first_name AS sender_first_name, messages.id, last_name AS send_last_name, messages.created_at, message, reciever_id  FROM messages LEFT JOIN users ON messages.user_id = users.id WHERE messages.reciever_id = %(id)s;"
        results = connectToMySQL("private_wall").query_db(query,data)
        if len(results) < 1:
            return False
        print(results)
        return results
    
    @classmethod
    def delete_message(cls,data):
        query = "DELETE FROM messages WHERE messages.id = %(message_id)s;"
        result = connectToMySQL("private_wall").query_db(query,data)



        
        

    