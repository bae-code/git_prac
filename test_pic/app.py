from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.0pi7g.mongodb.net/Cluster0?retryWrites=true&w=majority') # 클라이언트 설정시 작성
db = client.dbsparta

#################################
##  HTML을 주는 부분             ##
#################################
@app.route('/')
def home():
    return render_template('index.html')

# 방식1 : DB에는 파일 이름만 넣어놓고, 이미지 자체는 서버 컴퓨터에 저장하는 방식
@app.route('/fileupload', methods=['POST'])
def file_upload():
    # and 닉네임 변경 
    title_receive = request.form['title_give']
    file = request.files['file_give']
    # 해당 파일에서 확장자명만 추출
    extension = file.filename.split('.')[-1]
    # 파일 이름이 중복되면 안되므로, 지금 시간을 해당 파일 이름으로 만들어서 중복이 되지 않게 함!
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{title_receive}-{mytime}'
    # 파일 저장 경로 설정 (파일은 db가 아니라, 서버 컴퓨터 자체에 저장됨)
    save_to = f'static/{filename}.{extension}'
    # 파일 저장!
    file.save(save_to)
    
    # 아래와 같이 입력하면 db에 추가 가능!
    doc = {'title':title_receive, 'img':f'{filename}.{extension}'}
    db.camp.insert_one(doc)

    return jsonify({'result':'success'})

# 주소에다가 /fileshow/이미지타이틀 입력하면 그 이미지타이틀을 title이라는 변수로 받아옴
@app.route('/fileshow/<title>')
def file_show(title):
    # title은 현재 이미지타이틀이므로, 그것을 이용해서 db에서 이미지 '파일'의 이름을 가지고 옴
    img_info = db.camp.find_one({'title': title})
    # 해당 이미지 정보를 jinja 형식으로 사용하기 위해 넘김
    return render_template('showimg.html', img_info=img_info)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)