from flask import request
from flask_wtf import FlaskForm
from requests import Session

from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField, FieldList, FormField
from wtforms import FloatField, IntegerField, Form



class PowerChannelForm(FlaskForm):
    current_limit = FloatField(default=10.0)
    off_delay = FloatField(default=5.0)
    on_delay = FloatField(default=5.0)
    power_group = SelectField(label="Power Group", choices=[("main", "Main"),
                                                            ("aux", "Aux"),
                                                            ("disabled", "Disabled"), ])
    voltages = FieldList(FloatField(), min_entries=3)


class PowerConfigForm(FlaskForm):
    config_name = StringField(label="Power Config", default="Main")
    power_channel_1 = FormField(PowerChannelForm)
    power_channel_2 = FormField(PowerChannelForm)
    power_channel_3 = FormField(PowerChannelForm)
    power_channel_4 = FormField(PowerChannelForm)


class MediaTypeForm(FlaskForm):
    media_type = StringField(label="Type")
    media_speeds = FieldList(StringField("Speed (Mbps)"), min_entries=3)


class TemperatureForm(FlaskForm):
    thermal_dwell_time = IntegerField(default=5)
    temperature = FieldList(IntegerField(), min_entries=3, default=[25, 0, 60])


class TestPointForm(FlaskForm):
    name = StringField()
    test_point = StringField()
    voltage_rail = BooleanField(default=True)
    edge_rail = BooleanField(default=False)
    autoscale = BooleanField(default=True)
    expected_voltage = FloatField()
    vertical_offset = FloatField(default=0.0)
    vertical_range = FloatField(default=0.0)


class ProductForm(FlaskForm):
    product_selector = StringField(label="Product")
    pba = StringField(label="PBA")
    rework = StringField(label="Rework")


class CreateTestPlanForm(FlaskForm):
    product = FormField(ProductForm)

    thermal = FormField(TemperatureForm)
    media = FieldList(FormField(MediaTypeForm), min_entries=1)
    power_configs = FieldList(FormField(PowerConfigForm), min_entries=1)

    test_points = FieldList(FormField(TestPointForm), min_entries=1)

    submit = SubmitField("Submit")
