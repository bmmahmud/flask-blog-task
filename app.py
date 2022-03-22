from logging import exception
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# crate an App using flask framework -> obj of Flask
app = Flask(__name__)
# connect with configure with app
app.config.from_object('config.BaseConfig')

# connect database and use db for DBMS -> obj of SQLAlchemy
db = SQLAlchemy(app)
# create and modify database table and entity -> obj of Migration
migrate = Migrate(app,db)

## Model to create Database
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    descriptions = db.Column(db.String(1000))
    createtime = db.Column(db.DateTime())
    authorname = db.Column(db.String(100))

    def __init__(self,title='Default',descriptions=None,createtime=None,authorname=None):
        self.title = title
        self.descriptions = descriptions
        self.createtime = createtime
        self.authorname = authorname
        
# API Routes
@app.route('/')
@app.route('/home')
def home():
    postList = Blog.query.all()
    return render_template('index.html',postList=postList)

# add
@app.route('/add',methods=['POST'])
def add():
    title = request.form.get('title')
    descriptions = request.form.get('descriptions')
    createtime = datetime.now() #request.form.get('createtime')
    authorname = 'Mahmud'#request.form.get('authorname')

    newPost = Blog(title=title, descriptions=descriptions,createtime=createtime,authorname=authorname)
    db.session.add(newPost)
    db.session.commit()
    return redirect(url_for("home")) 
# view one post
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blog.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post)
# update
@app.route('/update/<int:post_id>',methods = ['GET','POST'])
def update(post_id):
    post = Blog.query.filter_by(id=post_id).first()
    if request.method == 'POST':
        post.title = request.form['title']
        post.descriptions = request.form['descriptions']
        post.createtime = datetime.now() #request.form.get('createtime')
        post.authorname = 'Mahmud'#request.form.get('authorname')
        try:
            db.session.commit()
            return redirect(f'/post/{post_id}')
        except: 
            return f"Post with id = {post_id} Does not exist"
    # show details of the post
    return render_template('update.html', post = post)

@app.route("/delete/<int:post_id>")
def delete(post_id):
    todo = Blog.query.filter_by(id=post_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))



if __name__ == '__main__':
    app.run(debug=True)