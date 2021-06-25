from flask import Flask,redirect,url_for,render_template,request, flash, session
from forms import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from send_mail import send_mail
import urllib.request, urllib.parse
import urllib

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
    try:
        percentage = str(round((score / total) * 100)) + "%"
    except ZeroDivisionError:
        percentage = 0
    return percentage

def findTotal(array):
    total = 0;
    for i in range(len(array)):
        total = total + array[i]
        print("Function " + str(total))
    # percentage
    groupTotal = len(array) * 4
    print("GROUP TOTAL")
    print(groupTotal)
    print(len(array))
    print(total)
    percentage = findPercentage(total, groupTotal)

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
        session['firstname'] = new_user.firstname
        session['lastname'] = new_user.lastname
        session['phone'] = new_user.phone
        session['email'] = new_user.email
        session['course'] = form.course.data
        flash(f'Thank you' + form.firstname.data)
        return redirect(url_for('forms'))
    return render_template('index.html', form=form)

@app.route('/forms')
def forms():
    questions = Question.query.all()
    set1 = []
    set2 = []
    set3 = []
    for question in questions:
        if question.id <= 7:
            set1.append(question)
        if  8 <= question.id <= 14:
            set2.append(question)
        if  15 <= question.id <= 22:
            set3.append(question)
        print(set3)
        # while 7 < question.id < 14:
        
    learnerCentricity = set1
    # learnerCentricity = Question.query.filter_by(skillGroup = "Learner Centricity").all()
    teachingForRecall = set2
    # teachingForRecall = Question.query.filter_by(skillGroup = "Teaching for Recall").all()
    teachingForEngagement = set3
    # teachingForEngagement = Question.query.filter_by(skillGroup = "Teaching for Engagement").all()
    totalquestions = len(questions)
    return render_template('forms.html', questions = questions, totalquestions=totalquestions, learnerCentricity=learnerCentricity, teachingForRecall=teachingForRecall, teachingForEngagement=teachingForEngagement )

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

def send_sms(api_key,phone,message,sender_id):
    params = {"key":api_key,"to":phone,"msg":message,"sender_id":sender_id}
    url = 'https://apps.mnotify.net/smsapi?'+ urllib.parse.urlencode(params)
    content = urllib.request.urlopen(url).read()
    print (content)
    print (url)

@app.route('/report', methods=['GET','POST'])
def report():
    send_mail()
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
            if not i.component in strengths:
                print("Item is in array already.")
                strengths.append(i.component)
        if point == 1:
            print("Needs Much Work")
            if not i.component in muchwork:
                muchwork.append(i.component)    
        if point == 2:
            print("Appending Fair")
            if not i.component in fair:
                fair.append(i.component)
        if point == 0:
            print("Much attention Needed")
            if not i.component in attention:
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
    firstname = session['firstname']
    lastname = session['lastname']
    phone = session['phone']
    email = session['email']
    course = session['course']

    msgbody = "You have recieved a new entry from " + firstname + " " + lastname + " . Email: " + email + ". Phone: " + phone + ". Course: " + course  
    send_sms('aniXLCfDJ2S0F1joBHuM0FcmH','0545977191',msgbody,'PrestoSL')
    return render_template('report.html', percentage = percentage, skills=skills, strengths=strengths, attention=attention, muchwork=muchwork, fair=fair, learnerCentricityTotal=learnerCentricityTotal, teachingForRecallTotal=teachingForRecallTotal, teachingForEngagementTotal=teachingForEngagementTotal)
if __name__ == '__main__':
    app.run(port=5000,debug=True)