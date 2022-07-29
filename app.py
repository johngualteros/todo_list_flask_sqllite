from flask import Flask,render_template,request,redirect,url_for,flash,session,jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/create-task',methods=['POST'])
def create():
    task = Task(content=request.form['content'],done=False)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/done/<int:id>')
def done(id):
    task = Task.query.get(id)
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete-task/<int:id>')
def delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)