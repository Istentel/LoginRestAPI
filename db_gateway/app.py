import os
from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'user'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, text_password):
        self.password_hash = bcrypt.generate_password_hash(text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'<User {self.username}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f'<Student {self.firstname}>'

# Create table
with app.app_context():
    db.create_all()

@app.route('/api/hello', methods=['GET'])
def get_hello():
    return jsonify({'message': 'Hello from the db_gateway server!'})

@app.route('/api/register', methods=['POST'])
def register_user():          
    try:
        print("Call register api!")
        user = json.loads(request.json)

        new_username = user["username"]
        new_password = user["password"]
        new_email = user["email"]

        if new_username and new_password and new_email and request.method == 'POST':
            new_user = User(username=new_username, 
                                password=new_password,
                                email=new_email)
            
            db.session.add(new_user)
            db.session.commit()

            response = jsonify('User added successfully!')
            response.status_code = 200
            return response
        else:
            response = jsonify('No data available')
            response.status_code = 204
            return response
    except Exception as e:
        print(e)
        response = "Internal server error!"
        response.status_code = 500
        return response
    
@app.route('/api/login', methods=['GET'])
def login_user(): 
    auth = request.authorization

    if not auth:
        return "missing credentials", 401
    
    attempted_user = User.query.filter_by(email=auth.username).first()
    
    if attempted_user and attempted_user.check_password_correction(attempted_password=auth.password):
        return "Successfuly logged", 200
    else:
        return "Invalid credentials", 401
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
