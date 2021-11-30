#from code.project_Balsam.app.models.course import Course
#from code.project_Balsam.app.models.gradebook import Gradebook
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
#userName is email, use userName in each class to query
studentPerformanceBP = Blueprint('studentPerformance',__name__)

@studentPerformanceBP.route('/performance?email=<email>', methods=['GET','POST'])
@login_required
def get_performance(email):
    if request.method=='GET':
        temp_list=[]
        courseList=[]
        semester=[]#all the semester that student have
        stuID=Student.query.filter(Student.userName==email).first().stuID #get stuID from email
        # get all course from student_course
        all_courseID=[]
        for i in student_course.query.filter(stuID==student_course.stuID).group_by(student_course.courseID).all():
            courseList.append(Course.query.filter(i.courseID==Course.courseID).first().name)
        #print(courseList)
        # get all semester
        for i in courseList:
            temp=Course.query.filter(Course.name==i).all()
            temp_list.append(temp)
        for i in temp_list:
            for j in i:
                if j.semester in semester:
                    pass
                else:
                    semester.append(j.semester)
        print(semester) 
        return render_template('performance.html',cilo="",email=email,Wtype="student",function="PERFORMANCE",courseList=courseList,message='',semester=semester)
    else:
        mark=[]        
        courseList=[]
        semester=[]
        courseInput=request.form.get("CourseName")#form's courseName
        semesterInput=request.form.get("semester")#form's semester
        
        stuID=Student.query.filter(Student.userName==email).first().stuID #get stuID from email
        stu_course=student_course.query.filter(student_course.stuID==stuID).all()
        #return all course
        for i in stu_course:
            courseList.append(Course.query.filter(i.courseID==Course.courseID).first().name)
        
        #return courseList and semester to web page
        all_courseID=[]
        for i in student_course.query.filter(stuID==student_course.stuID).all():
            all_courseID.append(i.courseID)
        #print('sdafa:',all_courseID)
        for i in all_courseID:
            temp=Course.query.filter(i==Course.courseID).group_by(Course.semester).all()
            for j in temp:
                if j.semester not in semester:
                    semester.append(j.semester)

        try:
            courseID=Course.query.filter(and_(courseInput==Course.name,Course.semester==semesterInput)).first().courseID#get courseID
        except AttributeError:
            message='some details are incorrect'
            return render_template('performance.html',cilo='',message=message,email=email,Wtype="student",function="PERFORMANCE",courseList=courseList,semester=semester)
        print('cID',courseID)
        print('adsf',Gradebook.query.filter(and_(courseID==Gradebook.courseID,Gradebook.stuID==stuID,Gradebook.semester==semesterInput)).all())
        for i in Gradebook.query.filter(and_(courseID==Gradebook.courseID,Gradebook.stuID==stuID,Gradebook.semester==semesterInput)).all():
            mark.append((i.jsonstr())['mark'])
        print(mark)
        ass=assessment.query.filter(and_(assessment.courseID==courseID,assessment.Semester==semesterInput)).all()#get assessment method
        print('ass:',ass)
        
        
        
        #print('clist:',courseList)
        
        #calculate performance
        weight=[]
        cilo=[]
        final_weight=[]
        for i in ass:
            weight.append([i['CILO'],i['weight']])
            final_weight.append(i['weight'])
        for i in weight:
            temp=list(map(int,i[0].split('-')))
            if len(temp)>1:
                if(temp[1]!=2 and temp[0]==1):
                    temp.insert(1,2)
            cilo.append(temp)
        cilo1_weight=0
        cilo2_weight=0
        cilo3_weight=0
        for i in range(0,len(mark)):
            if len(cilo[i])==1:
                if (cilo[i])[0]==1:
                    cilo1_weight+=final_weight[i]
                elif (cilo[i])[0]==2:
                    cilo2_weight+=final_weight[i]
                else:
                    cilo3_weight+=final_weight[i]
            elif len(cilo[i])==2:
                if 1 in cilo[i]:
                    cilo1_weight+=final_weight[i] / len(cilo[i])
                if 2 in cilo[i]:
                    cilo2_weight+=final_weight[i] / len(cilo[i])
                if 3 in cilo[i]:
                    cilo3_weight+=final_weight[i] / len(cilo[i])
            else:
                cilo1_weight+=final_weight[i] / len(cilo[i])
                cilo2_weight+=final_weight[i] / len(cilo[i])
                cilo3_weight+=final_weight[i] / len(cilo[i])
        cilo1_weight/=100
        cilo2_weight/=100
        cilo3_weight/=100
        print('cilo1_weight:',cilo1_weight)
        #declare variable of performance on each cilo
        performance1=0
        performance2=0
        performance3=0
        #calculate performance
        for i in range(0,len(mark)):
            #print('cilo[i]:',cilo[i])
            if len(cilo[i])==1:
                # print(cilo[i][0])
                if ((cilo[i])[0])==1:
                    performance1+=mark[i]
                    continue
                elif ((cilo[i])[0])==2:
                    performance2+=mark[i]
                    continue
                else:
                    performance3+=mark[i]
                    continue       
            elif len(cilo[i])==2:
                if 1 in cilo[i]:
                    performance1+=mark[i] / len(cilo[i])
                if 2 in cilo[i]:
                    performance2+=mark[i] / len(cilo[i])
                if 3 in cilo[i]:
                    performance3+=mark[i] / len(cilo[i])
            else:
                performance1+=mark[i]/len(cilo[i])
                performance2+=mark[i]/len(cilo[i])
                performance3+=mark[i]/len(cilo[i])
        #return the result
        try:
            p1=round(performance1/cilo1_weight,1)
        except ZeroDivisionError:
            p1=0
        try:    
            p2=round(performance2/cilo2_weight,1)
        except ZeroDivisionError:
            p2=0
        try:
            p3=round(performance3/cilo3_weight,1)
        except :
            p3=0
        final_performance={'cilo1':0,# the dict value that return to web page
                'cilo2':0,
                'cilo3':0}
        temp_performance=[p1,p2,p3]
        for i in range(1,len(temp_performance)+1):
            if i!=0:
                final_performance['cilo'+str(i)]=temp_performance[i-1]
        print(final_performance)
    # return str(p1)+', '+str(p2)+', '+str(p3)
    return render_template('performance.html',cilo=final_performance,email=email,Wtype="student",function="PERFORMANCE",courseList=courseList,message='',semester=semester)