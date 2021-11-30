#from code.project_Balsam.app.models.course import Course
#from code.project_Balsam.app.models.gradebook import Gradebook
from app.models.course_precourse import course_precourse
from flask import Blueprint,render_template, request
from sqlalchemy.sql.expression import and_
from app.models.base import db
from app.models.designer import Designer
from flask_login import login_required
from app.models.student import Student
from app.models.gradebook import Gradebook
from app.models.student_course import student_course
from app.models.assessment import assessment
from app.models.course import Course
studentShowDependencyBP = Blueprint('studentShowDependency',__name__)

@studentShowDependencyBP.route('/showDependency?email=<email>', methods=['GET','POST'])
@login_required
def showDependency(email):
        if request.method=='GET':
                programmeList=[]
                temp=Course.query.filter().group_by(Course.programme).all()
                for i in temp:
                        programmeList.append(i.programme)
                print(programmeList)
                return render_template('showDependency.html',programmeList=programmeList,email=email,function="DEPENDENCY",Wtype="student")
        else:
                programmeList=[]
                temp=Course.query.filter().group_by(Course.programme).all()
                for i in temp:
                        programmeList.append(i.programme)
                print(programmeList)
                programmeInput='CST'#assume input is CST
                courseID=[]
                precourseID=[]
                temp=dict()
                relation=dict()
                #get all courseID and its precourseID
                for i in Course.query.filter(Course.programme==programmeInput).group_by(Course.courseID).all():
                        courseID.append(i.courseID)        
                        precourseID.append(i.getprecourseID())
                #the relation between course and its precourse
                for i in range(len(courseID)):
                        temp[str(courseID[i])]=precourseID[i]
                for key,value in temp.items():
                        if temp[key]==0:
                                pass
                        else:
                                relation[key]=value
                #print(relation)
                course_pre=[]#query in course_precourse table
                for i in relation:
                        course_pre.append(course_precourse.query.filter(course_precourse.precourseID==relation[i]).all())
                #print(course_pre)
                # for i in range(len)
                # print(course_pre)
                for i in course_pre:
                        for j in range(0,len(i)):
                                i[j]=i[j].ciloName#change element in course_pre list to its ciloname
                #print('course_pre:',course_pre)
                keys=[]
                final_relation=dict()
                for key in relation:
                        keys.append(key)
                #print(keys)
                #print(len(course_pre))
                #print(course_pre[0])
                for i in range(0,len(course_pre)):
                        final_relation[str(keys[i])]=course_pre[i]
                print(final_relation)
                return render_template('showDependency.html',programmeList=programmeList,email=email,function="DEPENDENCY",Wtype="student")