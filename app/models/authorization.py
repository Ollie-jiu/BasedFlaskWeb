from flask_login import UserMixin
class authorization(UserMixin):
    email=""
    def __init__(self,email):
        super().__init__()
        self.email=email
    def get_id(self):
        return '1'