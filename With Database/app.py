from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
app.secret_key="alok"
db=SQLAlchemy(app)

class  Blogpost(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content= db.Column(db.Text,nullable=False)
    author =db.Column(db.String(20),nullable=False,default='N/A')
    def __repr__(self):
        return 'BLog Post :' + str(self.id)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method=='POST':
        if request.form['login']!='admin' or \
            request.form['password']!='admin':
            error= 'Invalid Username or password , please try again'
        else:
            flash("You are successfully logged in")
            flash("Logout Before login again")
            return redirect('/logout')
    return render_template("login.html", error=error) 

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/posts',methods=['GET','POST'])
def posts(): 
    if(request.method =='POST'):
        post_author=request.form['author']
        post_title=request.form['title']
        post_content=request.form['content']
        new_post=Blogpost(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return(redirect('/posts'))
    else:
        allposts=Blogpost.query.all()
        return render_template('post.html',posts=allposts) 
@app.route('/posts/delete/<int:id>')
def delete(id):
        post=Blogpost.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post=Blogpost.query.get_or_404(id)
    if request.method=="POST":
        post.author=request.form['author']
        post.title=request.form['title']
        post.content=request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post)

@app.route('/about')
def about():
    return render_template('about.html')
    
if __name__ == "__main__":
    app.run(debug=True)

