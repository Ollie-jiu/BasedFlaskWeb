from flask import Flask
from app.controller import lecturer, student, designer, user, createCourse, modifyCourse, getPerformance, defineDependency, studentShowDependency, lecturerShowDependency, designerShowDependency, showAnalysis
from app.models import assessment,course_cilo,gradebook,analysis_course,course_precourse,log

# 定义注册蓝图方法
def register_blueprints(app):
    app.register_blueprint(lecturer.lecturerBP,url_prefix='/lecturer')
    app.register_blueprint(lecturer.lecturerSearchBP,url_prefix='/lecturer')
    app.register_blueprint(showAnalysis.showAnalysisBP,url_prefix='/lecturer')
    app.register_blueprint(lecturerShowDependency.lecturerShowDependencyBP,url_prefix='/lecturer')
    app.register_blueprint(student.studentBP,url_prefix='/student')
    app.register_blueprint(student.studentsearchBP,url_prefix='/student')
    app.register_blueprint(getPerformance.studentPerformanceBP,url_prefix='/student')
    app.register_blueprint(studentShowDependency.studentShowDependencyBP,url_prefix='/student')
    app.register_blueprint(designer.designerBP,url_prefix='/designer')
    app.register_blueprint(createCourse.createCourseBP,url_prefix='/designer')
    app.register_blueprint(createCourse.addCILO_AssessmentBP,url_prefix='/designer/createCourse')
    app.register_blueprint(designer.designersearchBP,url_prefix='/designer')
    app.register_blueprint(modifyCourse.modifyCourseBP,url_prefix='/designer')
    app.register_blueprint(modifyCourse.modifyCILOs_AssessmentsBP,url_prefix='/designer/modify')
    app.register_blueprint(defineDependency.defineDenpendencyBP,url_prefix='/designer')
    app.register_blueprint(designerShowDependency.designerShowDependencyBP,url_prefix='/designer')
    app.register_blueprint(user.userBP,url_prefix='/user')
    

# 注册插件(数据库关联)
def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    # create_all要放到app上下文环境中使用
    with app.app_context():
        db.create_all()
 

def create_app():
    app = Flask(__name__)
    # app.config.from_object('app.config.setting') # 基本配置(setting.py) 
    app.config.from_object('app.config.secure') # 重要参数配置(secure.py)
    # 注册蓝图与app对象相关联
    register_blueprints(app)
    # 注册插件(数据库)与app对象相关联
    register_plugin(app)
    # 一定要记得返回app
    return app