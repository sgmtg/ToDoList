from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # todo.dbという名前のdbを設定
db = SQLAlchemy(app)  # dbを生成



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))  # 空でもok
    due = db.Column(db.DateTime, nullable=False)  # 日付型を指定
    done = db.Column(db.Boolean, default=False)  # 完了かどうか



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts)

    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        
        due = datetime.strptime(due, '%Y-%m-%d')  # フォームから文字列を受け取るため日付型に変換
        new_post = Post(title=title, detail=detail, due=due)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/detail/<int:id>')
def detail(id):
    post = Post.query.get(id)  # 該当するidの投稿内容を取得
    return render_template('detail.html', post=post)

@app.route('/change_status/<int:id>')
def change_status(id):
    app.logger.info(id)

    post = Post.query.get(id)
    app.logger.info(post)
    
    post.done = not post.done
    db.session.commit()
    return redirect('/')
    

# アプリケーションコンテキスト内でデータベース操作を行うための関数を作成
def create_tables():
    db.create_all()
    

if __name__ == "__main__":
    app.run(port=3000, debug=True)  # 8080
    create_tables()


