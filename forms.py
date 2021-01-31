from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

#dont think need datarequired
class BookSearchForm(FlaskForm):
    """Form to search for books"""
    title = StringField('Title or Author',
                        [DataRequired(message=("Please Enter a Title"))])
    submit = SubmitField('Search GoodReads')

class ChooseBook(FlaskForm):
    """from to select book"""
    books = SelectField('Book Options')
    submit = SubmitField('Select')

class AddNote(FlaskForm):
    body = TextAreaField('Message Body')
    #notes =


# [VARIABLE] = [FIELD TYPE]('[LABEL]', [
#         validators=[VALIDATOR TYPE](message=('[ERROR MESSAGE'))
#     ])
# https://hackersandslackers.com/flask-wtforms-forms/
