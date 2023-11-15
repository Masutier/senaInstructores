from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField
from wtforms.validators import InputRequired, Length


class AprendizInfoForm(FlaskForm):
    ficha = StringField('Ficha', validators=[InputRequired(), Length(min=5, max=8)])
    name = StringField('Nombre', validators=[InputRequired(), Length(min=2, max=100)])
    lastname = StringField('Apellidos', validators=[InputRequired(), Length(min=5, max=100)])
    tipoDoc = StringField('Tipo Documento', validators=[InputRequired(), Length(min=1, max=3)])
    numdoc = IntegerField('Numero de Documento', validators=[InputRequired()])


class FichaForm(FlaskForm):
    ficha = StringField('Ficha', validators=[InputRequired(), Length(min=5, max=8)])
