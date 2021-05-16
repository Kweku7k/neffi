from flask import Flask,redirect,url_for,render_template,request, flash
from forms import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
app.config['SECRET_KEY'] = '5791628b21sb13ce0c676dfde280ba245'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://isbiiqutsfeekn:c2058971f5bb424127a6b01d9ed3419b5599727a6f67d80136187b13465fe69a@ec2-34-200-94-86.compute-1.amazonaws.com:5432/d3ucdicb4224a8'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import *

#Functions
def skill(percentage):
    poor = range(0, 29)
    fair = range(30, 59)
    acceptable = range(60, 75)
    good = range(76, 92)
    outstanding = range(93,97)
    exceptional = range(98,101)
    yourskill = "not set"
    for i in poor:
        if percentage == i:
            print(i)
            yourskill = "Poor"
    for i in fair:
        if percentage == i:
            print(i)
            yourskill = "Fair"
    for i in acceptable:
        if percentage == i:
            print(i)
            yourskill = "Acceptable"
    for i in good:
        if percentage == i:
            print(i)
            yourskill = "Good"
    for i in outstanding:
        if percentage == i:
            print(i)
            yourskill = "Outstanding"
    for i in exceptional:
        if exceptional == i:
            print(i)
            yourskill = "Exceptional"
    return yourskill


def findPercentage(score, total):
    percentage = str(round((score / total) * 100)) + "%"
    return percentage

def findTotal(array):
    total = 0;
    for i in range(len(array)):
        total = total + array[i]
        print("Function " + str(total))
    # percentage
    percentage = findPercentage(len(array), total)
    return percentage

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
    totalquestions = len(questions)
    return render_template('forms.html', questions = questions, totalquestions=totalquestions)

@app.route('/admin')
def admin():
    questions = Question.query.all()
    totalquestions = len(questions)
    return render_template('admin.html', questions = questions, totalquestions = totalquestions)


@app.route('/admin/questions')
def adminquestions():
    questions = Question.query.all()
    print(questions)
    return render_template('questions.html', questions = questions)

@app.route('/admin/addquestion', methods=['GET','POST'])
def addquestion():
    form = Questions()
    if form.validate_on_submit():
        new_question = Question(question=form.question.data, skillGroup = form.skillGroup.data, q_number=form.q_number.data, component =form.component.data )
        db.session.add(new_question)
        db.session.commit()
        print("It submits")
        return redirect (url_for('admin'))
    return render_template('addaquestion.html', form=form)

@app.route('/report', methods=['GET','POST'])
def report():
    questions = Question.query.all()
    totalquestions = len(questions)
    score = 0
    muchwork = []
    attention = []
    fair = []
    strengths = []
    teachingForRecall = []
    learnerCentricity = []
    teachingForEngagement = []

    for i in questions:
        # questionId is the question id
        questionId = str(i.id)
        # name is the point for each question
        point = int(request.form[ questionId ])
        # This picks the point you scored for each question and makes it an integer for a specific time
        score = score + point
        print(score)
        print("Component " + i.skillGroup)
        print(i.skillGroup + " - " + str(point))
        if 3 <= point <= 4:
            print("Appending Strengths")
            strengths.append(i.component)
        if 0 <= point <= 1:
            print("Needs Much Work")
            muchwork.append(i.component)    
        if point == 2:
            print("Appending Fair")
            fair.append(i.component)
        if point == 0:
            print("Much attention Needed")
            attention.append(i.component)
        # Fill the skillGroup for calculations
        if (i.skillGroup) == "Learner Centricity":
            learnerCentricity.append(point)
            print("This is a Learner Centricity Component with a total of ")

        if (i.skillGroup) == "Teaching for Recall":
            print("This is a Teaching for Recall Component")
            teachingForRecall.append(point)
        if (i.skillGroup) == "Teaching for Engagement":
            print("This is a Teaching for Engagement Component")
            teachingForEngagement.append(point)


    print("Score = " + str(score))
    total = totalquestions*4
    print("Total = " + str(total))
    percent = (score/total)
    print("Your percent" + str(percent))
    percentage = round(percent * 100)
    print(str(percentage) + "%")
    print("Your Skill was " + skill(12))
    skills = skill(percentage)
    print("Your Strengths = " + str(strengths))
    print("Attention needed = " + str(attention))
    print("Fair Skills = " + str(fair))
    learnerCentricityTotal = findTotal(learnerCentricity)
    teachingForRecallTotal = findTotal(teachingForRecall)
    teachingForEngagementTotal = findTotal(teachingForEngagement)
    print(learnerCentricityTotal)
    print(teachingForRecallTotal)
    print(teachingForEngagementTotal)
    return render_template('report.html', percentage = percentage, skills=skills, strengths=strengths, attention=attention, muchwork=muchwork, fair=fair, learnerCentricityTotal=learnerCentricityTotal, teachingForRecallTotal=teachingForRecallTotal, teachingForEngagementTotal=teachingForEngagementTotal)
if __name__ == '__main__':
    app.run(port=5000,debug=True)