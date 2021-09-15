from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

from datetime import datetime


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))
    return jsonify({'all_diary': diaries})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    # [업로드 이미지 처리]
    # 클라이언트가 업로드한 파일을 서버에 저장
    file = request.files["file_give"]

    # 이미지 확장자
    # 가장 마지막 문자열 가져오기 [-1]
    extension = file.filename.split('.')[-1]

    today = datetime.now() # 현재 시각 가져오기
    time = today.strftime('%Y-%m-%d-%H-%M-%S')
    fname = f'file-{time}'

    save_to = f'static/{fname}.{extension}' # python f-string
    file.save(save_to)

    # 업데이트 날짜 표시
    date = today.strftime('%Y.%m.%d')

    # [DB 처리]
    doc = {
        'title': title_receive,
        'content': content_receive,
        'file': f'{fname}.{extension}',
        'date': date
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)