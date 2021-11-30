#import libraries
from app import create_app
from flask_login import LoginManager
from app.models.authorization import authorization as A1

app = create_app()
app.secret_key = 's3cr3t'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.load_view = "user.login"


@login_manager.user_loader
def load_user(user_email):
    user = A1(user_email)
    return user


if __name__ == '__main__':
    # 启动应用服务器, 使用默认参数, 开启调试模式
    app.run(debug=True, host='127.0.0.1', port=5000)
    # app.run(host='0.0.0.0', port=5001)
