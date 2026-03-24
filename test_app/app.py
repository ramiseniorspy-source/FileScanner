from db import execute_query
from flask import Flask, request

app = Flask(__name__)

@app.route('/login')
def login():
    username = request.args.get('username')
    
    # Passing untrusted user input directly to the DB module
    # The scanner AST should link this route to the db file!
    results = execute_query(username)
    
    if results:
        return "Logged inside!"
    return "Failed"
