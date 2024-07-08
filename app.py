from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import  logging
import json
logger = logging.getLogger(__name__)
transform_name = {
    'msg': 'customMessage',
    'levelname': 'logLevel',
    'exc_info': 'exceptionStackTrace'
}

def key(k):
    return transform_name[k] if k in transform_name.keys() else k

#formatter=logging.Formatter(filename='user_auth.log',format='%(asctime)s - %(levelname)s - %(message)s')

class BaseJSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        super(BaseJSONFormatter, self).format(record)
        output = {key(k): str(v) for k, v in record.__dict__.items()}
        return json.dumps(output)

cf = BaseJSONFormatter()

#sh = logging.StreamHandler()
fh = logging.FileHandler('user_auth.log')
fh.setFormatter(cf)
logger.addHandler(fh)

app = Flask(__name__)
client = MongoClient('192.168.1.22', 27017)  # MongoDB is running locally
db = client['user_db']
users_collection = db['users']


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are  required'}), 400

    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        logger.warning('Username already exists')
        return jsonify({'error': 'Username already exists'}), 400
        

    hashed_password = generate_password_hash(password)
    new_user = {'username': username, 'password': hashed_password}
    users_collection.insert_one(new_user)
    logger.info('User registered successfully')
    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = users_collection.find_one({'username': username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful'}), 200

@app.route('/', methods=['GET'])
def default():
    return jsonify({'status': 'OK', 'message':'Welcome to python sample app'}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    app.run(debug=True)
    
    
    

