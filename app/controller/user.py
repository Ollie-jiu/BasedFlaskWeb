from app.models.base import db
from app.models.designer import Designer
from app.models.lecturer import Lecturer
from app.models.student import Student
from app.models.authorization import authorization as A1
from flask import (Blueprint, jsonify, redirect, render_template, request,url_for)
from sqlalchemy import all_, and_, any_, or_
from sqlalchemy.orm import query
from flask_login import  LoginManager,login_user,logout_user

userBP = Blueprint('user',__name__)


@userBP.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',title='Sample Login',header='Sample Case')
    else:
        email = request.form.get('email')
        _password = request.form.get('password')
        _type= request.form.get('type')
        #print(email, _password,_type)
        if '@mail.uic.edu.hk' in email and _type=='student':
            result = Student.query.filter(and_(Student.userName == email,Student._password == _password)).first()
            if result:
                user=A1(email)
                login_user(user)
                return redirect(url_for('student.get_student',email=email))
            else:
                return render_template('login.html',status='error1')
        elif '@mail.uic.edu.hk' in email and _type=='lecturer':
            result = Lecturer.query.filter(and_(Lecturer.userName == email,Lecturer._password == _password)).first()
            print(result)
            if result:
                user=A1(email)
                login_user(user)
                return redirect(url_for('lecturer.get_lecturer',email=email))
            else:
                # return "username or password incorrect"
                return render_template('login.html',status='error1')
        elif '@mail.uic.edu.hk' in email and _type=='courseDesigner':
            result = Designer.query.filter(and_(Designer.userName == email,Designer._password == _password)).first()
            if result:
                user=A1(email)
                login_user(user)
                return redirect(url_for('designer.get_designer',email=email))
            else:
                # return "username or password incorrect"
                return render_template('login.html',status='error1')
        else:
            return render_template('login.html',status='error2')
@userBP.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for("user.login"))
    