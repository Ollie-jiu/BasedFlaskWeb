from flask import Blueprint,render_template, request
from app.models.course_cilo import course_cilo
from app.models.course import Course
from app.models.base import db
from app.models.designer import Designer
from app.models.course_precourse import course_precourse
from flask_login import login_required

designerBP = Blueprint('designer',__name__)
designersearchBP=Blueprint('designerSearch',__name__)


@designerBP.route('/main?email=<email>', methods=['GET','POST'])
@login_required
def get_designer(email):
    return render_template('courseDesigner.html',email=email,function="Course Designer",Wtype="Course designer")

@designersearchBP.route('/Search?email=<email>', methods=['GET','POST'])
def search(email):
    if request.method == 'GET':
        # print(1)
        return render_template('search.html',email=email,function="Search",Wtype="Course designer")
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
                return render_template('search.html',type=_type,Wtype="Course designer",course=course,email=email,function="SEARCH",show_pre=show_pre,precourseName=precourseName,beprecourseName=beprecourseName)
            return render_template('search.html',type=_type,Wtype="Course designer",course=course,email=email,function="SEARCH")
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
                return render_template('search.html',type=_type,Wtype="Course designer",cilo=cilo,email=email,function="SEARCH",show_pre=show_pre,precourse_cilos=precourse_cilos,beprecourse_cilos=beprecourse_cilos,cilo_courseName=cilo_courseName)
            # print(result)
            return render_template('search.html',type=_type,Wtype="Course designer",cilo=cilo,email=email,function="SEARCH",cilo_courseName=cilo_courseName)
        else:
            programme=Course.query.filter(Course.programme == searchMessage).group_by(Course.name).all()
            return render_template('search.html',type=_type,Wtype="Course designer",programme=programme,email=email,function="SEARCH")
