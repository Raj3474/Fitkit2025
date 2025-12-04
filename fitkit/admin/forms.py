from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import SelectMultipleField, TextAreaField, StringField, IntegerField, SubmitField, MultipleFileField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fitkit.users.models import User


class MultipleCheckBoxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ul')
    option_widget = widgets.CheckboxInput()



class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=500)])
    price = IntegerField('Price', validators=[DataRequired()])
    sizes = MultipleCheckBoxField('Sizes', choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('xl', 'Extra Large')], validators=[DataRequired()])
    image = MultipleFileField('Product Image', validators=[FileAllowed(['jpeg', 'jpg', 'png', 'webp']), FileRequired()])
    submit = SubmitField('Submit')