from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class TodoForm(FlaskForm):
    content = StringField('Task', validators=[
        DataRequired(),
        Length(min=1, max=500)
    ])
    description = TextAreaField('Description', validators=[Optional()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='medium')
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    due_date = DateTimeLocalField('Due Date', validators=[Optional()], format='%Y-%m-%dT%H:%M')
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Task')


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[
        DataRequired(),
        Length(min=1, max=50)
    ])
    color = StringField('Color', default='#007bff')
    submit = SubmitField('Save Category')


class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')