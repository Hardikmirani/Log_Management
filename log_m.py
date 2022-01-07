from flask import Flask, render_template, redirect, url_for,flash,request,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_mail import *
from random import randint


app = Flask(__name__)

mail = Mail(app)

app.secret_key = 'Yudiz'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'imgujju19@gmail.com'  
app.config['MAIL_PASSWORD'] = 'hardik****'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True

mail = Mail(app) 
db = SQLAlchemy(app)

otp = randint(000000,999999) 

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(20), unique = True , nullable = False)
    email = db.Column(db.String(20), unique = True , nullable = False)
    password = db.Column(db.String(30), nullable = False)
    log = db.relationship('Log', backref = 'intern')

class Log(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    intern_id = db.Column(db.Integer, db. ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    log = db.Column(db.String(20), nullable = False)
    fileupload = db.Column(db.LargeBinary)


@app.route('/')

def index():
    return redirect('login')

@app.route('/register',methods = ['GET','POST'])

def register():
    if request.method=="POST":
        Full_Name = request.form['full_name']
        Email = request.form['email']
        Password = request.form['password']

    
        user = User(full_name = Full_Name , email = Email , password = Password)
        
        db.session.add(user)
        db.session.commit()
        
        # return redirect(url_for('login'))
    mylog = User.query.all()
    return render_template('register.html')



@app.route('/login',methods = ['GET','POST'])

def login():

    if request.method=="POST":
        
        email1 = request.form['email']
        # session = 'email1'
        session["email1"] = request.form.get("email")
        # session ['email1'] = request.form['email']
        password1 = request.form['password']

        user = User.query.filter_by(email = email1, password = password1).first()
        if user is not None:
            print(user.id)
            c_id = user.id
            # profile = Log.query.filter_by(id = c_id)
            profile = Log.query.filter_by(intern_id = c_id)
            # return render_template('dashboard.html')
            # profile = Log.query.filter_by(id = id)
            return render_template('dashshow.html',profile = profile )
            # return redirect('/dashshow/<id = c_id')
        else:
            return render_template('login.html')
    
            mylog = User.query.all()

    return render_template('login.html')


@app.route('/dashboard',methods = ['GET','POST'])

def dashboard():

    # if session.get("email1"):

    # if 'email1' in session: 

    if not session.get('email1'):
        return redirect('/')

    if request.method=="POST":
        
        date = datetime.now()
        log = request.form['log_content']
        email = session['email1']
        user = User.query.filter_by(email = email).first()
        # intern_id = request.form['intern_id']
        intern_id = user.id
            # fileupload = request.form['filename']
        fileupload = request.files['filename']
            # fileupload.save(secure_filename(fileupload.filename))
        log = Log(date = date ,intern_id = intern_id, log = log , fileupload = fileupload.read())
        db.session.add(log)
        db.session.commit()


    logcon = Log.query.all()    
    return render_template('dashboard.html')

@app.route('/dashshow')

def dashshow():

    # profile = Log.query.all()
    return render_template('dashshow.html')
    # return render_template('dashshow.html',profile = profile)


@app.route('/update/<int:id>', methods = ['GET','POST'])

def update(id):

    profile = Log.query.filter_by(id=id).first()

    if request.method == "POST":
        profile = Log.query.filter_by(id=id).first()

        profile.date = datetime.now()
        profile.log = request.form['log_content']
        db.session.commit()
        return redirect('/')
    else:
       return render_template('/update.html',profile = profile)


@app.route('/delete/<int:id>')

def delete(id):   
    profile = Log.query.filter_by(id = id).first()
    db.session.delete(profile)
    db.session.commit()

    return redirect('/')

@app.route('/forgotpassword',  methods = ['GET','POST'] )

def forgotpassword():
    if request.method=="POST":

        user = User.query.all()
        email = request.form['email']
        session["email"] = request.form.get("email")


        user = User.query.filter_by(email = email).first()
        

        if user is not None:
       
            msg = Message('For OTP', sender = 'imgujju19@gmail.com', recipients=[email]) 
            msg.body = 'IF you want to reset your password please enter this OTP number   ' + str(otp)

            mail.send(msg)
            return render_template('verifyotp.html', user = user)

    return render_template('forgotpassword.html')

@app.route('/verifyotp/<int:id>',  methods = ['POST'] )

def verifyotp(id):
    user = User.query.all()
    user_otp = request.form['otp'] 
    session["user_otp"] = request.form.get("otp")
    if otp == int(user_otp):
        user = User.query.filter_by(id=id).first()
        print(user.id)
        print ("hello")
        # s = session['user_otp']
        # return redirect('/resetpassword/<int:id>')
        return render_template('resetpassword.html', user = user)
   
    return render_template('verifyotp.html')


@app.route('/resetpassword/<int:id>', methods = ['GET','POST'])

def resetpassword(id):

    user = User.query.filter_by(id=id).first()
    print (user.id)

    if not session.get('user_otp'):
        return redirect('/')

    if request.method == "POST":

        user = User.query.filter_by(id=id).first()
        print(user.id)
        print('hii')

        user.password = request.form['new_password']
        db.session.commit()
        session.pop('user_otp',None)
        return redirect('/')

    return render_template('resetpassword.html', user = user)



@app.route('/log_out')

def log_out():

    # session.pop('email1',None)
    session.pop('email1', None)
    return redirect('/')


if __name__ == ('__main__'):
    app.run(debug = True)
