from app.models.course_precourse import course_precourse
from flask import Blueprint,render_template, request
from flask.globals import session
from flask_login.utils import logout_user
from app.models.base import db
from app.models.student import Student
from flask_login import login_required
from app.models.course import Course
from app.models.user import User
from app.models.student_course import student_course
from sqlalchemy import and_
from app.models.course_cilo import course_cilo
from app.models.student import Student
from app.models.course_precourse import course_precourse

studentBP = Blueprint('student',__name__)
studentsearchBP=Blueprint('studentSearch',__name__)

@studentBP.route('/Main?email=<email>', methods=['GET','POST'])
@login_required
def get_student(email):
    if request.method == 'GET':
        courseID=[]
        stuID=(Student.query.filter(email==Student.userName).all())[0].stuID #get stuID from email
        #print(stuID)
        temp=student_course.query.filter(student_course.stuID==stuID).all()#use stuID get couseID in student_course table
        #print(temp)
        for i in temp:
            courseID.append(i.courseID)
        #print(courseID)
        length=len(courseID)
        result=[]
        course=[]
        for i in range(0,length):
            result.append(Course.query.filter(Course.courseID==courseID[i]).all())
        #print(result)
        for i in result:
            for j in i:
                course.append(j)
        #print(course)
        # for i in course:
        #     print(i.name)
        # result=db.session.query(Student,Course).filter(email==email).all()
        # print(result)
        #course=Course.query.filter(result[0].courseID==Course.courseID).all()
        return render_template('student.html',Wtype='Student',email = email,course=course,function="STUDENT")


@studentsearchBP.route('/Search?email=<email>', methods=['GET','POST'])
def search(email):
    if request.method == 'GET':
        # print(1)
        return render_template('search.html',email=email,function="Search",Wtype="student")
    else:
        searchMessage=request.form.get('search')
        _type=request.form.get('type')
        print(searchMessage)
        print(_type)
        if _type=='courseName':
            show_pre = 0
            if(Course.query.filter(Course.name==searchMessage).all() != []):
                course=Course.query.filter(Course.name==searchMessage).all()
                show_pre = 1
            else:
                course=Course.query.filter(Course.name.like('%{keyword}%'.format(keyword=searchMessage))).group_by(Course.name).all()
            if(show_pre == 1):
                try:
                    courseID=Course.query.filter(Course.name == (course[0].jsonstr())['CourseName']).first().courseID
                    precourseID=course_precourse.query.filter(course_precourse.courseID == courseID).first().precourseID
                    precourseName=Course.query.filter(Course.courseID == precourseID).first().name
                except:
                    precourseName="None"
                try:
                    beprecourseID=course_precourse.query.filter(course_precourse.precourseID == courseID).first().courseID
                    beprecourseName=Course.query.filter(Course.courseID == beprecourseID).first().name
                except:
                    beprecourseName="None"
                return render_template('search.html',type=_type,Wtype="student",course=course,email=email,function="SEARCH",show_pre=show_pre,precourseName=precourseName,beprecourseName=beprecourseName)
            return render_template('search.html',type=_type,Wtype="student",course=course,email=email,function="SEARCH")
        elif _type=='CILO':
            cilo=course_cilo.query.filter(course_cilo.ciloName == searchMessage).all()
            cilo_courseName=[]
            show_pre = 0
            if(len(cilo) == 1):
                show_pre = 1
                cilo_courseID=(cilo[0].jsonstr())['courseID']
                ciloCourseName=Course.query.filter(Course.courseID == cilo_courseID).all()
                for i in ciloCourseName:
                    cilo_courseName.append((i.jsonstr())['CourseName'])
                cilo_courseName=list(set(cilo_courseName))
                print("^^^^",cilo_courseName)
                try:
                    precourse_cilos=[]
                    precourseID=course_precourse.query.filter(course_precourse.courseID == cilo_courseID).first().precourseID
                    precourse_cilo=course_cilo.query.filter(course_cilo.courseID == precourseID).all()
                    for i in precourse_cilo:
                        precourse_cilos.append((i.jsonstr())['ciloName'])
                except:
                    precourse_cilos=["None"]
                try:
                    beprecourse_cilos=[]
                    beprecourseID=course_precourse.query.filter(course_precourse.precourseID == cilo_courseID).first().courseID
                    beprecourse_cilo=course_cilo.query.filter(course_cilo.courseID == beprecourseID).all()
                    for i in beprecourse_cilo:
                        beprecourse_cilos.append((i.jsonstr())['ciloName'])
                except:
                    beprecourse_cilos=["None"]
                print("%%%%",cilo)
                print("^^^^^",precourse_cilos)
                print("^^^^^",beprecourse_cilos)
                return render_template('search.html',type=_type,Wtype="student",cilo=cilo,email=email,function="SEARCH",show_pre=show_pre,precourse_cilos=precourse_cilos,beprecourse_cilos=beprecourse_cilos,cilo_courseName=cilo_courseName)
            # print(result)
            return render_template('search.html',type=_type,Wtype="student",cilo=cilo,email=email,function="SEARCH",cilo_courseName=cilo_courseName)
        else:
            programme=Course.query.filter(Course.programme == searchMessage).group_by(Course.name).all()
            return render_template('search.html',type=_type,Wtype="student",programme=programme,email=email,function="SEARCH")



