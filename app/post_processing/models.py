from flask_wtf import FlaskForm
from wtforms.fields import SelectField
from flask_wtf.file import FileAllowed, FileField, FileRequired

ALLOWED_EXTENSIONS = {'txt', 'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in \
           ALLOWED_EXTENSIONS


class UploadForm(FlaskForm):
    test_selector = SelectField("Test:",
                                choices=[("load_profile", "Load Profile"),
                                         ("inrush", "Inrush"),
                                         ("vsd", "Voltage System Dynamics"),
                                         ("ber", "Bit Error Ratio"),
                                         ("sequencing", "Sequencing"),
                                         ("on_time", "Power-on Time"),
                                         ("edge_power", "Edge Power")])
    filter_by = SelectField("Results Filter:",
                            choices=[("default", "default"),
                                     ("testpoint", "testpoint"),
                                     ("capture", "Capture"),
                                     ("runid", "Runid"),
                                     ("sample", "Sample"),
                                     ("rework", "Rework"),
                                     ("pba", "PBA"),
                                     ("dut", "Product")])
    csv_file = FileField('CSV Dataframe', validators=[
        FileRequired(),
        FileAllowed(['csv'], "CSV Files Only")
    ])

    user_input_file = FileField('Input File', validators=[
        FileRequired(),
        FileAllowed(['xlsx'], "XLSX Files Only")
    ])
