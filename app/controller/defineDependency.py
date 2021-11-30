from flask import Blueprint,render_template, request
from app.models.base import db
from app.models.course import Course
from flask_login import login_required
from app.models.course_cilo import course_cilo
from app.models.course_precourse import course_precourse
defineDenpendencyBP=Blueprint('defineDependency',__name__)
CourseFirst=[]
@defineDenpendencyBP.route('/defineDependency?email=<email>', methods=['GET','POST'])
@login_required
def defineDependency(email):
    if request.method == "GET":
        courseList=[]
        for i in Course.query.filter().group_by(Course.name).all():
            #print(i)
            courseList.append(i.name)
        print(courseList)
        
        #pre_course
        #courseName
        return render_template('defDependency.html',message="",courseList=courseList,Pre_CILOs=[],email=email,function="DEFINE DEPENDENCIES",Wtype="Course designer")
    #post method
    else:
        Pre_CILOs=[]
        courseList=[]
        for i in Course.query.filter().group_by(Course.name).all():
            courseList.append(i.name)
        
        if len(request.form.to_dict())>2:
            courseID= Course.query.filter(Course.name==CourseFirst[0]).first().courseID#get courseID
            precourseID=Course.query.filter(Course.name==CourseFirst[1]).first().courseID
            #如何cilo的长度大于2的话；
            #!!!!!!!!!!!!!!!!!!在这个里面加数据到数据库
            print(request.form.get('courseName'))
            print(list(request.form.to_dict()))
            for i in list(request.form.to_dict()):
                if 'checkbox' in i:
                    a=course_precourse(courseID,precourseID,(i.split(':')[1]))
                    db.session.add(a)
                    db.session.commit()
                    print('1')
            print(CourseFirst)#这是个名字呀，
            #没办法只能用数组存值，
            print(CourseFirst[0])
            print(CourseFirst[1])
            print(courseID)#拿到了加吧
            CourseFirst.clear()
            c=Course.query.filter(Course.courseID==courseID).all()
            for i in c:
                i.precourseID=precourseID
                db.session.commit()    
            return render_template('defDependency.html',message="",email=email,courseList=courseList,Pre_CILOs=[],function="DEFINE DEPENDENCIES",Wtype="Course designer")
        else:
            if request.form.get('courseName')==request.form.get('pre_course'):
                return render_template('defDependency.html',message="it's same",email=email,courseList=courseList,Pre_CILOs=Pre_CILOs,function="DEFINE DEPENDENCIES",Wtype="Course designer")
            elif request.form.get('courseName')!='' and request.form.get('pre_course')!='':# both are not null
                courseSeleted=request.form.get('courseName')
                CourseFirst.append(courseSeleted)
                pre_course=request.form.get('pre_course')
                CourseFirst.append(pre_course)
                # print('2:',pre_course)
                precourseID=Course.query.filter(Course.name==pre_course).first().courseID
                # print('a:',precourseID)
                for i in course_cilo.query.filter(course_cilo.courseID==precourseID).all():
                    Pre_CILOs.append(i.ciloName)
                # print('a:',Pre_CILOs)
                return render_template('defDependency.html',message="",email=email,courseList=courseList,Pre_CILOs=Pre_CILOs,function="DEFINE DEPENDENCIES",Wtype="Course designer")
            else:
                return render_template('defDependency.html',message="You need to input two courses",email=email,courseList=courseList,Pre_CILOs=[],function="DEFINE DEPENDENCIES",Wtype="Course designer")
        
        
        
