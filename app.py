from flask import Flask,redirect,url_for,render_template,request, flash
from forms import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
app.config['SECRET_KEY'] = '5791628b21sb13ce0c676dfde280ba245'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import *

@app.route('/',methods=['GET','POST'])
def home():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Yes")
        new_user = User(firstname = form.firstname.data, lastname=form.lastname.data, phone=form.phone.data, email = form.email.data )
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('forms'))
        flash(f'Thank you' + form.firstname.data)
    return render_template('index.html', form=form)

@app.route('/forms')
def forms():
    questions = Question.query.all()
    return render_template('forms.html', questions = questions)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/questions')
def adminquestions():
    questions = Question.query.all()
    print(questions)
    return render_template('questions.html', questions = questions)

@app.route('/admin/addquestion', methods=['GET','POST'])
def addquestion():
    form = Questions()
    if form.validate_on_submit():
        new_question = Question(question=form.question.data, skillGroup = form.skillGroup.data, q_number=form.q_number.data )
        db.session.add(new_question)
        db.session.commit()
        print("It submits")
        return redirect (url_for('forms'))
    return render_template('addaquestion.html', form=form)

@app.route('/report', methods=['GET','POST'])
def report():
    questions = Question.query.all()
    totalquestions = len(questions)
    for i in questions:
        var = i.id
        var = str(var)
        # print(var)
        name = request.form[ var ]
        print(i.skillGroup + " - " + name)
    return render_template('report.html')
if __name__ == '__main__':
    app.run(port=5000,debug=True)