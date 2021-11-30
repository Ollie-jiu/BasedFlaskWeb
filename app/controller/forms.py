from typing import Text


from flask_wtf import FlaskForm
from wtforms import*
from wtforms.validators import*
class NewPostForm(FlaskForm):
    addCILO=SubmitField('addCILO')
    add=SubmitField('add')
    submit=SubmitField('submit')
    setDependency=SubmitField('setDependency')
    finishModify=SubmitField('finishModify')