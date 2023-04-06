from flask import Flask
app = Flask(__name__)
app.secret_key="Keep it save"
DATABASE = "users_login"