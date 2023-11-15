from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField
from wtforms.validators import InputRequired, Length

class AprendizInfoForm(FlaskForm):
    ficha = StringField('Ficha', validators=[InputRequired(), Length(min=7, max=7)])
    name = StringField('Nombre', validators=[InputRequired(), Length(min=2, max=100)])
    lastname = StringField('Apellidos', validators=[InputRequired(), Length(min=5, max=100)])
    tipoDoc = StringField('Tipo Documento', validators=[InputRequired(), Length(min=1, max=3)])
    numdoc = IntegerField('Numero de Documento', validators=[InputRequired()])


class AprendizEInstructor(FlaskForm):
    aprendizId = IntegerField()
    instructorId = IntegerField()


class preguntasForm(FlaskForm):
    ficha = StringField('Ficha', validators=[InputRequired(), Length(min=7, max=7)])
    aprendizNumDoc = IntegerField('Numero de Documento', validators=[InputRequired()])
    no_identificacion_instructor = IntegerField('Numero de Documento', validators=[InputRequired()])
    p01 = RadioField('P01', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])
    p02 = RadioField('P02', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])
    p03 = RadioField('P03', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])
    p04 = RadioField('P04', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])
    p05 = RadioField('P05', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])
    p06 = RadioField('P06', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])
    p07 = RadioField('P07', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])
    p08 = RadioField('P08', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])
    p09 = RadioField('P09', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])
    p10 = RadioField('P10', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])
    p11 = RadioField('P11', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])
    p12 = RadioField('P12', choices=['0', '1', '2', '3', '4', '5'], validators=[InputRequired()])


class FichaForm(FlaskForm):
    ficha = StringField('Ficha', validators=[InputRequired(), Length(min=7, max=7)])