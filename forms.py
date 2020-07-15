from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, FloatField
from wtforms.validators import DataRequired


class MyFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None


class ExpensesForm(FlaskForm):
    title = StringField('title', validators=[
                        DataRequired()], description='Nazwa')
    category = StringField('category', validators=[
                           DataRequired()], description='Kategoria')
    description = TextAreaField('description', description='Opis')
    value = MyFloatField('value', validators=[
                         DataRequired()], default=0.00, description='Wartość')
    periodic = BooleanField('periodic', description='Okresowy')
