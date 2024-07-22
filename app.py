from flask import Flask, g, request, jsonify, send_from_directory
import psycopg
import json
import db
import train
import io
import sys

app = Flask(__name__, static_url_path='', static_folder='static')

def get_db():
    if 'db' not in g:
        g.db = psycopg.connect(**db.params)
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/info")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/")
def index_html():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/train")
def train_html():
    return send_from_directory(app.static_folder, 'train.html')

@app.route("/my_icons.json/<f>")
def model(f):
    return send_from_directory('my_icons.json', f)

@app.route("/write", methods=["POST"])
def write_to_db():
    data = request.get_json()     
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            print("Connected to the database.")            

            # Insert data into a table
            insert_query = """
                INSERT INTO training_data (data)
                VALUES (%s)
            """
            data_to_insert = (json.dumps(data),)

            cursor.execute(insert_query, data_to_insert)
            conn.commit()
            
            response = { 'message': 'Data inserted successfully'}
    except Exception as e:        
        print(e)
        response = {
            'message': e
        }
    res = jsonify(response)
    res.headers['Content-Type'] = 'application/json'

    return res, 200
