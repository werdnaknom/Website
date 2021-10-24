from flask import render_template, request, make_response, current_app
import requests
from app.csv_json import bp
from app.csv_json.forms import FilterProductForm, FilterForm
from io import StringIO
import csv


@bp.route("/get_csv", methods=['GET', 'POST'])
def get_csv():
    form = FilterForm(request.form)
    filter_dict = {}
    if form.validate_on_submit():
        filter_dict = {}
        product = form.product.data
        filter_dict["dut"] = product

        test = form.test.data
        filter_dict['test_category'] = test

        pba = form.pba.data["value"]
        pba_comp = form.pba.data["comparison"]
        if pba:
            filter_comp = f"pba{pba_comp}"
            filter_dict[filter_comp] = pba

        rework = form.rework.data['value']
        rework_comp = form.rework.data["comparison"]
        if rework != -99:
            filter_comp = f"rework{rework_comp}"
            filter_dict[filter_comp] = rework
        submission = form.submission.data['value']
        submission_comp = form.submission.data['comparison']
        if submission:
            filter_comp = f"serial_number{submission_comp}"
            filter_dict[filter_comp] = submission
        runid = form.runid.data['value']
        runid_comp = form.runid.data['comparison']
        if runid != -99:
            filter_comp = f"runid{runid_comp}"
            filter_dict[filter_comp] = runid

        capture = form.capture.data['value']
        capture_comp = form.capture.data['comparison']
        if capture != -99:
            filter_comp = f"capture{capture_comp}"
            filter_dict[filter_comp] = capture
        waveform = form.waveform.data['value']
        waveform_comp = form.waveform.data['comparison']
        if waveform:
            filter_comp = f"waveform{waveform_comp}"
            filter_dict[filter_comp] = waveform

        status = form.status.data
        print(status)
        if status != "any":
            filter_dict["status"] = status
        temp = form.temperature.data['value']
        temp_comp = form.temperature.data['comparison']
        if temp != -99:
            filter_comp = f"temperature{temp_comp}"
            filter_dict[filter_comp] = temp

        # print(filter_dict)
        json_filter = {"filters": filter_dict}
        s = requests.session()
        s.trust_env = False
        resp = s.get(current_app.config["DATABASE"] + "dataframe",
                     json=json_filter)
        # resp = s.get("http://npoflask2.jf.intel.com:5001/dataframe",
        #             json=json_filter)

        json_resp = resp.json()
        # print(json_resp)
        if bool(resp) and len(json_resp) > 0:
            product = json_resp[0]
            headers = product[0].keys()

            buffer = StringIO()

            writer = csv.DictWriter(buffer, fieldnames=headers,
                                    extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rowdicts=product)

            output_name = "FILE_NAME.csv"
            output = make_response(buffer.getvalue())
            output.headers[
                "Content-Disposition"] = f"attachment; filename={output_name}"
            output.headers["Content-type"] = "text/csv"
            return output

        else:
            filter_dict["errors"] = json_resp

    else:
        # print(form.errors)
        pass
        # s = Session()
        #         # s.trust_env = False
        #         # test_plan_content = s.get(url="{}:{}/{}".format(DATABASE, '5002', "return_testplan"))
        # return send_file(BytesIO(test_plan_content.content), as_attachment=True, attachment_filename="Testplan.xlsx")
    return render_template('csv_json/csv_json.html',
                           title="Filter Json", form=form,
                           filter_dict=filter_dict)
