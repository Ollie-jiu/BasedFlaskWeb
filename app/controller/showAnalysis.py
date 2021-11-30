from flask import Blueprint, render_template, request
from sqlalchemy.sql.expression import and_
from app.models.base import db
from app.models.designer import Designer
from flask_login import login_required
from app.models.lecturer import Lecturer
from app.models.analysis_course import analysis_course
from app.models.student import Student
from app.models.gradebook import Gradebook
from app.models.student_course import student_course
from app.models.assessment import assessment
from app.models.course import Course
from pyecharts.charts import Bar
showAnalysisBP = Blueprint('showAnalysis', __name__)


@showAnalysisBP.route('/showAnalysis?email=<email>', methods=['GET', 'POST'])
@login_required
def get_analysis(email):

    courseList = []
    if request.method == 'GET':
        staffID = Lecturer.query.filter(
            Lecturer.userName == email).first().staffID  # get stuID from email
        staff_course = analysis_course.query.filter(
            analysis_course.staffID == staffID).all()
        for i in staff_course:
            courseList.append(Course.query.filter(
                i.courseID == Course.courseID).first().name)
        print(courseList)
        return render_template('analysis.html', cilo="", email=email, Wtype="lecturer", function="ANALYSIS", courseList=courseList, message='')
    else:
        semester = []
        course = []
        students = []
        courseInput = request.form.get("CourseName")  # form's courseName
        staffID = Lecturer.query.filter(
            Lecturer.userName == email).first().staffID  # get stuID from email
        staff_course = analysis_course.query.filter(
            analysis_course.staffID == staffID).all()
        for i in staff_course:
            courseList.append(Course.query.filter(
                i.courseID == Course.courseID).first().name)
        print(courseList)
        try:
            courseID = Course.query.filter(
                courseInput == Course.name).first().courseID  # get courseID
        except AttributeError:
            message = 'some details are incorrect'
            return render_template('analysis.html', cilo='', message=message, email=email, Wtype="lecturer", function="ANALYSIS", courseList=courseList, semester=semester)

        course_semester = Course.query.filter(Course.name == courseInput).all()
        for i in course_semester:
            semester.append((i.jsonstr())['semester'])

        students_course = student_course.query.filter(
            student_course.courseID == courseID).all()
        for i in students_course:
            students.append((i.jsonstr())['stuID'])

        average1 = []
        average2 = []
        average3 = []

        for i in semester:
            average1_semester = 0
            average2_semester = 0
            average3_semester = 0
            stuPerformance1 = []
            stuPerformance2 = []
            stuPerformance3 = []
            for j in students:
                ass = assessment.query.filter(
                    and_(assessment.Semester == i, assessment.courseID == courseID)).all()
                weight = []
                cilo = []
                cilo_weight = []

                for k in ass:
                    weight.append((k.jsonstr())['weight'])
                # calculate each cilo's weight
                for k in ass:
                    temp = list(map(int, k['CILO'].split('-')))
                    cilo.append(temp)
                for k in range(0, len(cilo)):
                    cilo_weight.append([cilo[k], weight[k]])

                cilo1_weight = 0
                cilo2_weight = 0
                cilo3_weight = 0
                for k in cilo_weight:
                    if(len(k[0]) == 1):
                        if(k[0][0] == 1):
                            cilo1_weight += k[1]
                        if(k[0][0] == 2):
                            cilo2_weight += k[1]
                        if(k[0][0] == 3):
                            cilo3_weight += k[1]
                    if(len(k[0]) == 2):
                        if(k[0] == [1, 2]):
                            cilo1_weight += k[1]/2
                            cilo2_weight += k[1]/2
                        if(k[0] == [1, 3]):
                            cilo1_weight += k[1]/2
                            cilo3_weight += k[1]/2
                        if(k[0] == [2, 3]):
                            cilo2_weight += k[1]/2
                            cilo3_weight += k[1]/2
                    if(len(k[0]) == 3):
                        cilo1_weight += k[1]/3
                        cilo2_weight += k[1]/3
                        cilo3_weight += k[1]/3
                cilo1_weight /= 100
                cilo2_weight /= 100
                cilo3_weight /= 100

                mark = []
                performance1 = 0
                performance2 = 0
                performance3 = 0
                grade = Gradebook.query.filter(and_(
                    Gradebook.semester == i, Gradebook.courseID == courseID, Gradebook.stuID == j)).all()
                for k in grade:
                    mark.append((k.jsonstr())['mark'])
                if(mark != []):
                    # calculate performance
                    for k in range(0, len(mark)):
                        # print('cilo[i]:',cilo[i])
                        if len(cilo[k]) == 1:
                            # print(cilo[i][0])
                            if cilo[k][0] == 1:
                                performance1 += mark[k]
                                continue
                            elif cilo[k][0] == 2:
                                performance2 += mark[k]
                                continue
                            else:
                                performance3 += mark[k]
                                continue
                        elif len(cilo[k]) == 2:
                            if 1 in cilo[k]:
                                performance1 += mark[k] / len(cilo[k])
                            if 2 in cilo[k]:
                                performance2 += mark[k] / len(cilo[k])
                            if 3 in cilo[k]:
                                performance3 += mark[k] / len(cilo[k])
                        else:
                            performance1 += mark[k]/len(cilo[k])
                            performance2 += mark[k]/len(cilo[k])
                            performance3 += mark[k]/len(cilo[k])
                    # return the result
                    try:
                        p1 = round(performance1/cilo1_weight, 1)
                    except ZeroDivisionError:
                        p1 = 0
                    try:
                        p2 = round(performance2/cilo2_weight, 1)
                    except ZeroDivisionError:
                        p2 = 0
                    try:
                        p3 = round(performance3/cilo3_weight, 1)
                    except ZeroDivisionError:
                        p3 = 0

                    stuPerformance1.append(p1)
                    stuPerformance2.append(p2)
                    stuPerformance3.append(p3)

            print("****", stuPerformance1)
            print("****", stuPerformance2)
            print("****", stuPerformance3)

            for j in stuPerformance1:
                average1_semester += j
            average1_semester /= len(stuPerformance1)
            for j in stuPerformance2:
                average2_semester += j
            average2_semester /= len(stuPerformance2)
            for j in stuPerformance3:
                average3_semester += j
            average3_semester /= len(stuPerformance3)

            average1.append([i, average1_semester,"CILO1"])
            average2.append([i, average2_semester,"CILO2"])
            average3.append([i, average3_semester,"CILO3"])

        print("^^^^^", average1)  # CILO1,[Semester,its avereage]
        print("^^^^^", average2)
        print("^^^^^", average3)

        analysis=[]
        errorCount1 = 0
        for i in range(0,len(average1)):
            if average1[i][1] != 0:
                errorCount1 += 1
        if errorCount1 == len(average1):
            analysis.append(average1)
        
        errorCount2 = 0
        for i in range(0,len(average2)):
            if average2[i][1] != 0:
                errorCount2 += 1
        if errorCount2 == len(average2):
            analysis.append(average2)

        errorCount3 = 0
        for i in range(0,len(average3)):
            if average3[i][1] != 0:
                errorCount3 += 1
        if errorCount3 == len(average3):
            analysis.append(average3)
        
        print("#####",analysis)
        # return_dict1 = dict()
        # return_dict2 = dict()
        # return_dict3 = dict()
        # for i in average1:
        #     return_dict1[str(i[0])] = i[1]
        # for i in average2:
        #     return_dict2[str(i[0])] = i[1]
        # for i in average3:
        #     return_dict3[str(i[0])] = i[1]

        # # return the result
        # analysis = []
        # for i in average1:
        #     print(i)
        # print('dict1', return_dict1)
        # print('dict2', return_dict2)
        # print('dict3', return_dict3)
        # analysis.append(return_dict1)
        # analysis.append(return_dict2)
        # analysis.append(return_dict3)
        # print("analysis", analysis)
        # for i in analysis:
        #     print(i)

        return render_template('analysis.html', cilo='final_performance', analysis=analysis, email=email, Wtype="lecturer", function="ANALYSIS", courseList=courseList, message='', semester=semester)
