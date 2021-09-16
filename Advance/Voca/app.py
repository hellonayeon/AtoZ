from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def main():
    myname = 'hellonayeon'
    return render_template("index.html", name=myname)

# 주소의 일부를 클라이언트측의 변수로 사용 가능하도록 [url?key=value 형식X]
@app.route('/detail/<keyword>')
def detail(keyword):
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token [토큰정보]"})
    result = r.json()
    print(result)

    word_receive = request.args.get("word_give")
    print(word_receive)

    return render_template("detail.html", word=keyword)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)