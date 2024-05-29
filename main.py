from flask import Flask, request, redirect, render_template, jsonify
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import uuid

db_url = 'sqlite:///database/test.db'
engine = create_engine(db_url)
base = declarative_base()

class Task(base):
    __tablename__ = "Tasks"
    uid = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    is_done = Column(Integer, default=0)

base.metadata.create_all(engine)

app = Flask(__name__)

@app.route('/')
def index():
    Session = sessionmaker(bind=engine)
    session = Session()
    tasks = session.query(Task).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add():
    Session = sessionmaker(bind=engine)
    session = Session()

    task = request.form.get('task')

    task = Task(uid=str(uuid.uuid1()), title=task)

    session.add(task)
    session.commit()
    
    return redirect('/')

@app.route('/done/<uid>')
def done(uid):
    Session = sessionmaker(bind=engine)
    session = Session()
    task = session.query(Task).filter(Task.uid == uid).one_or_none()

    if task.is_done == 0:
        task.is_done = 1
        session.commit()
    elif task.is_done == 1:
        task.is_done = 0
        session.commit()

    return redirect('/')

@app.route('/delete/<uid>')
def delete(uid):
    Session = sessionmaker(bind=engine)
    session = Session()
    task = session.query(Task).filter(Task.uid == uid).one_or_none()
    session.delete(task)
    session.commit()
    print(task.title)
    return redirect('/')

@app.route('/api')
def api():
    Session = sessionmaker(bind=engine)
    session = Session()
    tasks = session.query(Task).filter(Task.is_done == 1).all()
    
    main_dict = dict()

    for task in tasks:
        sub_dict = dict()
        sub_dict['title'] = task.title
        sub_dict['is_done'] = task.is_done
        main_dict[task.uid] = sub_dict
    
    print(main_dict)

    return jsonify(main_dict)

if __name__ == "__main__":
    app.run(debug=True)
