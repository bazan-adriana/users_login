from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


#  ===========       CREATE USER    =============
    @classmethod
    def create(cls, data):
            query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
            """
            return connectToMySQL(DATABASE).query_db(query, data)

#  ===========  GET USER BY ID  =============
    @classmethod
    def get_by_id(cls, data):
            query = """
            SELECT * FROM users
            WHERE id = %(id)s;
            """
            results = connectToMySQL(DATABASE).query_db(query, data)
            print(results)
            # if len(results) < 1:
                # return []
            return cls(results[0])

#  =========== GET USER BY EMAIL  =============
    @classmethod
    def get_by_email(cls, data):
            query = """
            SELECT * FROM users
            WHERE email = %(email)s;
            """
            results = connectToMySQL(DATABASE).query_db(query, data)
            print(results)
            if len(results) < 1:
                return False
            return cls(results[0])

#  ===========  VALIDATIONS  ========
    @staticmethod
    def validate(user):
            is_valid = True
            query = """
            SELECT * FROM users
            WHERE email = %(email)s;
            """
            results = connectToMySQL(DATABASE).query_db(query, user)

            if len(user['first_name']) < 1:  # checks validation for first_name
                flash("first_name required", "first_name")
                is_valid = False
                
            if len(user['last_name']) < 1:  # checks validation for last_name
                flash("last_name required", "reg")
                is_valid = False
                
            if len(user) < 1:      # checks validation for email
                flash("email required", "reg")
                is_valid = False
            elif not EMAIL_REGEX.match(user['email']): 
                flash("Invalid email address!", "reg")
                is_valid = False
            else:
                email_dict = {
                    'email': user['email']
                }
                potential_user = User.get_by_email(email_dict)
                if potential_user:
                    is_valid = False
                    flash("email already taken!", "reg")
                    
            if len(user['password']) < 1:  # checks validation for password
                flash("password required")
                is_valid = False
            if not user['password'] == user['confirm']:
                flash("password don't match!", "reg")
                is_valid = False
                
            return is_valid
