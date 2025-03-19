from email import message
from struct import calcsize
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate, migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///a.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'hello_man'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
limiter = Limiter(get_remote_address,app=app, default_limits= "10 per minute")
requests_count = {}


# QĐ1: Có 10 sân bay. Thời gian bay tối thiểu là 30 phút. Có tối đa 2 sân bay trung gian với thời gian dừng từ 10 đến 20 phút.
# QĐ2: Chỉ bán vé khi còn chỗ. Có 2 hạng vé (1, 2). Vé hạng 1 bằng 105% của đơn giá, vé hạng 2 bằng với đơn giá, mỗi chuyến bay có một giá vé riêng.
# QĐ3: Chỉ cho đặt vé chậm nhất 1 ngày trước khi khởi hành. Vào ngày khởi hành tất cả các phiếu đặt sẽ bị hủy.
# QĐ6: Người dùng có thể thay đổi các qui định như sau: 
#       + QĐ1: Thay đổi số lượng sân bay, thời gian bay tối thiểu, số sân bay trung gian tối đa, thời gian dừng tối thiểu/ tối đa tại các sân bay trung gian.
#       + QĐ2: Thay đổi số lượng các hạng vé.
#       + QĐ3: Thay đổi thời gian chậm nhất khi đặt vé, thời gian hủy đặt vé.

class Nhanvien(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.Text)
    email = db.Column(db.String(120), unique = True)
    pos = db.Column(db.Integer)

    def __repr__(self):
        return self.name
    
    def create_user(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = password 
        self.email = email
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

with app.app_context():
    db.create_all()
    db.session.commit()


def log_count():
    ip = request.remote_addr
    if ip in requests_count:
        requests_count[ip] +=1
    else:
        requests_count[ip] =1
    print(f'{ip} requested')

@app.route('/')
def index():
    return jsonify({"message": 'hello'})


@app.route('/api/login', methods=['POST'])
@limiter.limit('10 per minute')
def login():
    log_count()
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = Nhanvien.query.filter_by(username = username).first()
        if check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            session['name'] = user.name
            return {'status': 'success', 'message': 'Login successful'}
        else:
            return jsonify({'status': 'error', 'message': 'Invalid username or password'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/api/logout', methods=['POST'])
@limiter.limit('10 per minute')
def logout():
    log_count()
    if 'user_id' in session:
        session.clear()
        return jsonify({'message' : 'Logout success'})
    return jsonify({'message': "logout fail"})


@app.route('/api/register', methods =['POST'])
@limiter.limit('10 per minute')
def register():
    log_count()
    data = request.get_json()
    tmp = ['username', 'password', 'name', 'email']
    if any(i not in data for i in tmp):
        return jsonify({'message': 'Thiếu thông tin kìa cu'})
    username = data['username']
    password = data['password']
    hashpass = generate_password_hash(password)
    email = data['email']
    name = data['name']
    user =Nhanvien()
    if user.create_user(name, username, hashpass, email):
        return jsonify({'message': 'success'})
    return jsonify({'message': 'fail'})

@app.route('/api/get_account/')
@limiter.limit('10 per minute')
def get_acc():
    log_count()
    if 'username' in session:
        return jsonify({
            'username' :  session['username'],
            'email' : session['email'],
            'name': session.get('name')
        })
    return jsonify({'message': 'chưa login'})


# {
#     "username": "huypro37",
#     "password": "123456",
#     "email": "111",
#     "name": "huy"
# }

if __name__ == '__main__':
    app.run(debug=True)