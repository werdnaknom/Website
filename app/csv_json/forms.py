from flask import request
from flask_wtf import FlaskForm
from requests import Session

from wtforms import StringField, SubmitField, TextAreaField, SelectField, \
    BooleanField, FieldList, FormField
from wtforms import FloatField, IntegerField, Form
from wtforms.validators import InputRequired


class FilterProductForm(FlaskForm):
    filter = SelectField(label=u'Filter', choices=[("submission", "Submission"),
                                                   ("assembly", "PBA"),
                                                   ("rework", "Rework")],
                         validators=[])
    comparison = SelectField(label=u'Comparision',
                             choices=[("__eq", "="),  # Equal
                                      ("__lt", "<"),  # Less Than
                                      ("__gt", ">"),  # Greater Than
                                      ("__le", "<="),  # Less or Equal To
                                      ("__ge", ">="),  # Greater or Equal To
                                      ("__ne", "!=")])  # Not Equal
    value = StringField(label=u"Value", validators=[InputRequired()])


class StringFilterForm(FlaskForm):
    value = StringField()
    comparison = SelectField(label=u'Comparision',
                             choices=[("__eq", "="),  # Equal
                                      ("__ne", "!=")])  # Not Equal


class IntFilterForm(FlaskForm):
    value = IntegerField(default=-99)
    comparison = SelectField(label=u'Comparision',
                             choices=[("__ge", ">="),  # Greater or equal to
                                      ("__eq", "="),  # Equal
                                      ("__lt", "<"),  # Less Than
                                      ("__gt", ">"),  # Greater Than
                                      # ("__le", "<="),  # Less or Equal To
                                      ("__ne", "!=")])


class FilterForm(FlaskForm):
    product = StringField(label=u"Product", validators=[InputRequired()])
    test = SelectField(label="Test Category",
                       choices=[("EthAgent", "EthAgent"),
                                ("Aux To Main", "Aux To Main"),
                                ("Load Profile", "Load Profile"),
                                ("Ripple", "Ripple"),
                                ("QAT", "QAT"),
                                ])
    status = SelectField(label="Status",
                         choices=[
                             ("Complete", "Complete"),
                             ("Aborted", "Aborted"),
                             ("any", "-- Any --"),
                         ])

    '''
    #TODO:: This can be added once I can add them in JS with new IDs :(
    variables = FieldList(FormField(FilterProductForm, label="Filter"),
                          min_entries=1)
    '''
    pba = FormField(StringFilterForm, label="PBA")
    rework = FormField(IntFilterForm, label="Rework")
    submission = FormField(StringFilterForm, label="Submission")
    runid = FormField(IntFilterForm, label="Runid")
    capture = FormField(IntFilterForm, label="Capture")
    waveform = FormField(StringFilterForm, label="Waveform")
    temperature = FormField(IntFilterForm, label="Temperature")
    submit = SubmitField("Submit")
