from struct import calcsize
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///a.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# QĐ1: Có 10 sân bay. Thời gian bay tối thiểu là 30 phút. Có tối đa 2 sân bay trung gian với thời gian dừng từ 10 đến 20 phút.
# QĐ2: Chỉ bán vé khi còn chỗ. Có 2 hạng vé (1, 2). Vé hạng 1 bằng 105% của đơn giá, vé hạng 2 bằng với đơn giá, mỗi chuyến bay có một giá vé riêng.
# QĐ3: Chỉ cho đặt vé chậm nhất 1 ngày trước khi khởi hành. Vào ngày khởi hành tất cả các phiếu đặt sẽ bị hủy.
# QĐ6: Người dùng có thể thay đổi các qui định như sau: 
#       + QĐ1: Thay đổi số lượng sân bay, thời gian bay tối thiểu, số sân bay trung gian tối đa, thời gian dừng tối thiểu/ tối đa tại các sân bay trung gian.
#       + QĐ2: Thay đổi số lượng các hạng vé.
#       + QĐ3: Thay đổi thời gian chậm nhất khi đặt vé, thời gian hủy đặt vé.

class Nhanvien(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True)

    def __repr__(self):
        return self.name

    def add(self, name):
        try:
            self.name = name
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
        

class a:
    pass

class b:
    # code
    def i(a:a):
        pass

class a:
    # code
    def i(self):
        pass

with app.app_context():
    db.create_all()

# a=  Nhanvien.query.get(1)
