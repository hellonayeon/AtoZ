from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def add_order():
    name_receive = request.form['name_give']
    quantity_receive = request.form['quantity_give']
    residence_receive = request.form['residence_give']
    phone_receive = request.form['phone_give']

    print(name_receive, quantity_receive, residence_receive, phone_receive)

    doc = {
        'name': name_receive,
        'quantity': quantity_receive,
        'residence': residence_receive,
        'phone': phone_receive
    }
    db.orders.insert_one(doc)

    return jsonify({'msg': '내용 저장 완료 !'})

@app.route('/order', methods=['GET'])
def show_orders():
    orders = list(db.orders.find({}, {'_id': False}))
    return jsonify({'all_orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)