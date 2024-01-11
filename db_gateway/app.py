import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'user'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'

# Create table
with app.app_context():
    db.create_all()

@app.route('/api/hello', methods=['GET'])
def get_hello():
    return jsonify({'message': 'Hello from the server!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
