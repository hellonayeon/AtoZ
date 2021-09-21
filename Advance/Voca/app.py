from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests


app = Flask(__name__)

client = MongoClient('54.180.87.49', 27017, username="test", password="test")
db = client.dbsparta_advance_week2

@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    msg = request.args.get("msg")
    words = list(db.words.find({}, {'_id': False}))
    return render_template("index.html", words=words, msg=msg)


@app.route('/detail/<keyword>')
def detail(keyword):
    status_receive = request.args.get("status_give")
    # API에서 단어 뜻 찾아서 결과 보내기
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token [내토큰]"})
    if r.status_code != 200:
        return redirect(url_for("main", msg="Word not found in dictionary; Try another word"))
    result = r.json()
    print(result)

    return render_template("detail.html", word=keyword, result=result, status=status_receive)


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    word_receive = request.form["word_give"]
    definition_receive = request.form["definition_give"]
    doc = {
        'word': word_receive,
        'definition': definition_receive
    }

    db.words.insert_one(doc)

    return jsonify({'result': 'success', 'msg': f'단어 {word_receive} 저장 !'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    word_receive = request.form["word_give"]
    db.words.delete_one({ "word": word_receive })
    db.examples.delete_many({"word": word_receive}) # 단어에 대한 예문들도 모두 삭제
    return jsonify({'result': 'success', 'msg': f'단어 {word_receive} 삭제'})

@app.route('/api/get_exs', methods=['GET'])
def get_exs():
    word_receive = request.args.get("word_give")
    result = list(db.examples.find({"word": word_receive}, {"_id": False}))
    print(result)
    return jsonify({'result': 'success', 'examples': result})

@app.route('/api/save_ex', methods=['POST'])
def save_ex():
    # 예문 저장하기
    word_receive = request.form["word_give"]
    ex_receive = request.form["ex_give"]
    doc = {"word": word_receive, "example": ex_receive}
    db.examples.insert_one(doc)

    return jsonify({'msg': f'example "{ex_receive}" is saved!'})

@app.route('/api/delete_ex', methods=['POST'])
def delete_ex():
    # 예문 삭제하기
    word_receive = request.form["word_give"]
    number_receive = int(request.form["number_give"])
    example = list(db.examples.find({"word": word_receive}, {"_id": False}))[number_receive]["example"]

    doc = {"word": word_receive, "example": example}
    db.examples.delete_one(doc)

    return jsonify({'msg': f'example "{example}" is saved!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)