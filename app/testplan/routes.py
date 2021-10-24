from flask import render_template, redirect, url_for, send_file, jsonify, \
    request, current_app
from .forms import CreateTestPlanForm
from .forms import MediaTypeForm
from requests import Session
from io import BytesIO

from app.testplan import bp
#from flaskweb import globalConfig


def retrieve_testplan():
    s = Session()
    s.trust_env = False

    test_plan_content = s.get(url="{}{}".format(current_app.TESTPLAN,
                                                "testplan"))
    return test_plan_content


@bp.route("/create_testplan", methods=['GET', 'POST'])
def create_testplan():
    form = CreateTestPlanForm(request.form)
    test_plan_content = retrieve_testplan()
    print(test_plan_content.json())
    print(form.data)
    if form.validate_on_submit():
        print("Pass")
        print(form.data)
        print(form.product.data)
        print(form.thermal.data)
        print(form.media.data)
        print(form.power_configs[0].power_channel_1.data)
        print(form.test_points.data)
        # print(form.product.rework.data, form.product.pba.data, form.product.product_selector.data)
        # print(test_plan_content.json())
        # return redirect(url_for('main.index'))
    else:
        print(form.errors)
        pass
        # s = Session()
        #         # s.trust_env = False
        #         # test_plan_content = s.get(url="{}:{}/{}".format(DATABASE, '5002', "return_testplan"))
        # return send_file(BytesIO(test_plan_content.content), as_attachment=True, attachment_filename="Testplan.xlsx")
    return render_template('testplan/create_testplan.html',
                           title="Create Test Plan", form=form)


@bp.route('/process_add_member', methods=['POST'])
def add_member():
    print("OK!")
    form = CreateTestPlanForm()

    getattr(form, 'media').append_entry()

    return render_template('testplan/media_form.html', title="Create Test Plan",
                           form=form)
