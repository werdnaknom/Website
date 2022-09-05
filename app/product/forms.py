from flask import request
from flask_wtf import FlaskForm
from requests import Session

from wtforms import StringField, SubmitField, TextAreaField, SelectField, \
    BooleanField, FieldList, FormField
from wtforms import DecimalField, IntegerField, Form
from wtforms.validators import InputRequired


class Testpoint_Current_Form(FlaskForm):
    edge_rail = BooleanField(label="Edge Rail", default=True)


class BERForm(FlaskForm):
    module = StringField(label="Module/Speed")
    ber = DecimalField(label="Target BER", default=1e-12)
    confidence = IntegerField(label="Target Confidence", default=99)


class Testpoint_Voltage_Form(FlaskForm):
    product = StringField(label="Product", validators=[InputRequired()])
    testpoint = StringField(label="Testpoint", validators=[InputRequired()])
    edge_rail = BooleanField(label="Edge Rail", default=False)
    nominal_voltage = DecimalField(label="Nominal Voltage (V)", validators=[InputRequired()])
    spec_min = DecimalField(label="Specification Minimum (V)", validators=[InputRequired()])
    spec_max = DecimalField(label="Specification Maximum (V)", validators=[InputRequired()])
    bandwidth = DecimalField(label="Bandwidth (MHz)")
    max_poweron_time = DecimalField(label="Expected Power-on Time (ms)", validators=[InputRequired()])
    valid_voltage = DecimalField(label="Valid Voltage (V)")
    submit = SubmitField("Submit")
