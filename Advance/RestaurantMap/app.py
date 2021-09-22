from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('13.209.68.233', 27017, username="test", password="test")
db = client.dbsparta_advance_week3


@app.route('/')
def main():
    return render_template("index.html")

# 맛집 목록을 반환하는 API
@app.route('/matjip', methods=["GET"])
def get_matjip():
    # 1. 데이터베이스에서 맛집 목록을 꺼내오기
    # 2. 클라이언트 사이드에 돌려주기
    matjip_list = list(db.matjips.find({}, {"_id": False}))
    return jsonify({'result': 'success', 'matjip_list': matjip_list})

@app.route('/like_matjip', methods=["POST"])
def like_matjip():
    title_receive = request.form["title_give"]
    address_receive = request.form["address_give"]
    action_receive = request.form["action_give"]
    print(title_receive, address_receive, action_receive)

    if action_receive == "like":
        db.matjips.update_one({"title": title_receive, "address": address_receive}, {"$set": {"liked": True}})
    else:
        db.matjips.update_one({"title": title_receive, "address": address_receive}, {"$unset": {"liked": False}})
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)