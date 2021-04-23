from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        t1 = Task(title=title, desc = desc)
        db.session.add(t1)
        db.session.commit()
        
    all_tasks = Task.query.all()
    return render_template('index.html', all_tasks=all_tasks)


@app.route('/delete/<int:sno>')
def delete(sno):
    t_delete = Task.query.filter_by(sno=sno).first()
    db.session.delete(t_delete)
    db.session.commit()
    return redirect("/")


@app.route('/update/<int:sno>',  methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        t_update  = Task.query.filter_by(sno=sno).first()
        t_update.title = title
        t_update.desc = desc
        db.session.add(t_update)
        db.session.commit()
        return redirect("/")

    t_update  = Task.query.filter_by(sno=sno).first()
    return render_template('update.html', t_update=t_update)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=False)
