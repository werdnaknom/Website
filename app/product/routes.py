import typing as t
from dataclasses import dataclass, field

from flask import render_template, jsonify, Markup, send_file, current_app, request
import requests
from Entities.Entities import ProjectEntity, PBAEntity, ReworkEntity, RunidEntity, WaveformCaptureEntity
from app.product import bp
from io import BytesIO
import datetime

from database_functions.mongodatabase_functions import MongoDatabaseFunctions


@dataclass
class PowerChannel():
    name: str
    group: str
    on: bool
    voltages: t.List = field(default_factory=list)
    slew_rates: t.List = field(default_factory=list)

    '''@classmethod
    def build_from_runid(cls, runid:str, channel:0):
        cursor = MongoDatabaseFunctions.get_runid_voltages_by_channel(runid=runid, channel=channel)
        result = list(cursor)[0]
        pch = cls(name=, group=, on=, voltages=, slew_rates=)
    '''


# from bokeh.plotting import figure
# from bokeh.resources import CDN
# from bokeh.embed import file_html

def get_pba_entities_by_product(product: str) -> t.List[PBAEntity]:
    pba_entities = []
    pbas = MongoDatabaseFunctions.find_pba_entity_by_product(product)

    for pba in pbas:
        pba_entity = PBAEntity.from_dict(pba)
        pba_entity.reworks.extend(MongoDatabaseFunctions.find_reworks_by_pba(pba_entity.part_number))
        pba_entities.append(pba_entity)
    return pba_entities


def get_rework_entities_by_product(product: str) -> t.List[ReworkEntity]:
    rework_entities = []
    reworks = MongoDatabaseFunctions.find_rework_entities_by_product(product=product)

    for rework in reworks:
        rework_entity = ReworkEntity.from_dict(rework)
        rework_entities.append(rework_entity)
    return rework_entities


def get_runid_entities_by_product(product: str) -> t.List[ReworkEntity]:
    runid_entities = []
    runids = MongoDatabaseFunctions.find_runid_entities_by_product(product)
    for runid in runids:
        runid_entity = RunidEntity.from_dict(runid)
        runid_entities.append(runid_entity)
    return runid_entities


def get_capture_entities_by_product(product: str) -> t.List[ReworkEntity]:
    capture_entities = []
    capture_dicts = MongoDatabaseFunctions.find_waveform_capture_entities_by_product(product)
    print(capture_dicts[0])
    for capture in capture_dicts:
        try:
            capture_entity = WaveformCaptureEntity.from_dict(capture)
            capture_entities.append(capture_entity)
        except:
            pass
    return capture_entities


def get_runid_by_id(runid: str):
    runid_dict = MongoDatabaseFunctions.find_runid_by_id(id=runid)
    return runid_dict


def get_capture_temperatures_by_runid(runid: str):
    temperature, voltages = MongoDatabaseFunctions.get_runid_capture_data(runid=runid)
    return temperature, voltages


def get_runid_voltage_channels(runid: str) -> t.Tuple[t.List, t.List, t.List, t.List]:
    channel0 = get_runid_voltage_channel(runid, channel="0")
    channel1 = get_runid_voltage_channel(runid, channel="1")
    channel2 = get_runid_voltage_channel(runid, channel="2")
    channel3 = get_runid_voltage_channel(runid, channel="3")
    return channel0, channel1, channel2, channel3


def get_runid_voltage_channel(runid: str, channel: str) -> t.List:
    channel_info = MongoDatabaseFunctions.get_runid_voltages_by_channel(runid=runid, channel=channel)
    r = list(channel_info)
    print(channel_info, r)
    return r


@bp.route('/products/<product>')
def product(product):
    '''
    s = requests.Session()
    s.trust_env = False
    json_filter = {"filters": {"dut": product}}
    r = s.get(current_app.config["DATABASE"] + 'list', json=json_filter)
    product_dict = r.json()[0]
    '''
    product_dict = MongoDatabaseFunctions.find_product(product=product)
    # print(product_dict)
    product_entity = ProjectEntity.from_dict(product_dict)
    pbas = get_pba_entities_by_product(product)
    reworks = get_rework_entities_by_product(product)
    runids = get_runid_entities_by_product(product)

    # print(product_entity.tests_unique)
    return render_template('/product/product.html',
                           title=product_entity.descriptor,
                           product=product_entity,
                           pbas=pbas,
                           reworks=reworks,
                           runids=runids,
                           description="This is a description")


@bp.route('/products/<product>/pbas')
def product_pbas(product):
    '''
    s = requests.Session()
    s.trust_env = False
    print(product)

    json_filter = {"filters": {"dut": product}}
    r = s.get(current_app.config["DATABASE"] + 'assembly/overview',
              json=json_filter)
    return jsonify(r.json())
    '''
    pba_entities = get_pba_entities_by_product(product)
    return render_template('/product/pbas-tab.html',
                           pbas=pba_entities)


@bp.route('/products/<product>/reworks')
def product_reworks(product):
    '''
    s = requests.Session()
    s.trust_env = False
    print(product)

    json_filter = {"filters": {"dut": product}}
    r = s.get(current_app.config["DATABASE"] + 'rework/overview',
              json=json_filter)
    return jsonify(r.json())
    '''
    rework_entities = get_rework_entities_by_product(product)
    return render_template('/product/reworks-tab.html',
                           reworks_entities=rework_entities)


@bp.route('/products/<product>/runids')
def product_runids(product):
    runid_entities = get_runid_entities_by_product(product)

    return render_template('product/runids-tab.html',
                           runid_entities=runid_entities)


"""
@bp.route('/products/<product>/bokeh image')
def product_runids(product):
    plot = figure()
    xdata = range(1, 6)
    ydata = [x * x for x in xdata]
    plot.line(xdata, ydata)

    return Markup(file_html(plot, CDN, "my plot"))
"""


@bp.route('/products/<product>/tests')
def product_tests(product):
    '''
    s = requests.Session()
    s.trust_env = False
    print(product)

    json_filter = {"filters": {"dut": product}}
    r = s.get(current_app.config["DATABASE"] + 'test/overview',
              json=json_filter)
    return jsonify(r.json())
    '''
    capture_entities = get_capture_entities_by_product(product)
    print(capture_entities[0])
    return render_template('product/product-waveforms.html',
                           wfm_captures=capture_entities)


@bp.route('/products/<product>/table')
def product_table(product):
    s = requests.Session()
    s.trust_env = False
    print(product)

    json_filter = {"filters": {"dut": product}}

    r = s.get(current_app.config["DATABASE"] + 'product_table_data',
              json=json_filter)

    return jsonify(r.json())


@bp.route('/products')
def products():
    return render_template('/products/page-products.html', title="Products")


@bp.route("/product/<product>/testdata/<test>", methods=['GET'])
def testdata(product, test):
    print(product, test)
    import pandas as pd
    s = requests.Session()
    s.trust_env = False
    json_filter = {"filters": {"dut": product,
                               "test_category": test,
                               "status": "Complete"}}
    test_data_content = s.get(url=current_app.DATABASE + "dataframe",
                              json=json_filter)
    df = pd.DataFrame(test_data_content.json()[0])
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=test)
    writer.save()
    output.seek(0)

    return send_file(filename_or_fp=output, as_attachment=True,
                     attachment_filename="{}_{}_{}.xlsx".format(product, test,
                                                                datetime.datetime.now()))


from .pages import RunidPage


@bp.route('/products/runids/<runid>')
def runid_overview(runid):
    runid = get_runid_by_id(runid=runid)
    runid_entity = RunidEntity.from_dict(runid)

    page = RunidPage(entity=runid_entity, repo=MongoDatabaseFunctions())

    # TODO:: Get types of tests run, temperature and voltages tested.
    channel0 = get_runid_voltage_channel(runid=runid_entity.runid, channel="0")

    # return render_template('product/runid_overview_og.html',
    return render_template('product/runid_overview.html',
                           runid_entity=runid_entity,
                           page=page)


@bp.route('/products/<product>/runids/viewimage_grid/<runid>')
def runid_viewimage_grid(product, runid):
    tests = MongoDatabaseFunctions.get_runid_images_for_grid(runid=runid)

    return render_template('product/runid_viewimage_grid.html', title="{0} Runid {1}".format(product, runid),
                           product=product, tests=tests)


@bp.route('/products/runids/runid_overview_ajax', methods=('GET', 'POST'))
def runid_overview_ajax():
    if request.method == "POST":
        # TODO:: Get this data dynamically
        runid = request.form["runid"]
        runid_request = MongoDatabaseFunctions.find_runid_by_id(runid)
        system_info_json = runid_request['system_info']
        probes = system_info_json['probes']
        ats_version = system_info_json['ats_version']
        location = "OR"
        project = "Island Rapids"
        pba = "K87758-002"
        rework = 0
        serial = "894DA0"
        status = "Complete"
        status_info = "Test was aborted by user after 3 Hours 18 Minutes 53 Seconds"
        probes = [
            {
                "channel": 1,
                "part_number": "TDP1000",
                "serial_number": "B040055",
                "units": "V",
                "cal_status": "D",
                "dynamic_range": 8.5,
                "deguass": True
            },
            {
                "channel": 2,
                "part_number": "TCP0030A",
                "serial_number": "C005015",
                "units": "A",
                "cal_status": "D",
                "dynamic_range": 100,
                "deguass": True
            },
            {
                "channel": 3,
                "part_number": "TDP1000",
                "serial_number": "B040025",
                "units": "V",
                "cal_status": "D",
                "dynamic_range": 84,
                "deguass": True

            },
            {
                "channel": 4,
                "part_number": "TCP0030A",
                "serial_number": "C003949",
                "units": "A",
                "cal_status": "D",
                "dynamic_range": 100,
                "deguass": True
            },
            {
                "channel": 5,
                "part_number": "TDP1000",
                "serial_number": "B040051",
                "units": "V",
                "cal_status": "D",
                "dynamic_range": 8.5,
                "deguass": True
            },
            {
                "channel": 6,
                "part_number": "TDP1000",
                "serial_number": "B040097",
                "units": "V",
                "cal_status": "D",
                "dynamic_range": 8.5,
                "deguass": True
            },
            {
                "channel": 7,
                "part_number": "TDP1000",
                "serial_number": "B040050",
                "units": "V",
                "cal_status": "D",
                "dynamic_range": 8.5,
                "deguass": True
            },
            {
                "channel": 8,
                "part_number": "TDP1000",
                "serial_number": "B040101",
                "units": "V",
                "cal_status": "D",
                "dynamic_range": 8.5,
                "deguass": True
            }
        ]
    ats_version = "ATS 2.0 Alpha 25_19E77"
    technician = "phyllis sanderson"
    test_station = "LNO-TEST9"
    configuration = "4"
    board_id = 2401
    test_points = {
        "0": "3P3V_AUX",
        "1": "3P3V_AUX_CURRENT",
        "2": "12V_MAIN",
        "3": "12V_CURRENT",
        "4": "3P3V",
        "5": "1P8_VDDH_CVL1",
        "6": "1P8_VDDH_CVL2",
        "7": "1P1V_VDDH"
    }
    for tp in test_points.keys():
        probes[int(tp)]["Name"] = test_points[tp]

    comments = "start up config 4"

    # return jsonify({'htmlresponse': render_template('product/runid_overview.html', modal_runid=runid_request)})

    tests_run = MongoDatabaseFunctions.get_runid_test_categories(runid=runid_request["runid"])
    tests_run_str = ", ".join(tests_run)

    # print(runid_request["runid"])
    temperatures, voltages = MongoDatabaseFunctions.get_runid_capture_data(runid=runid_request["runid"])
    # print(temperatures)
    # print(voltages)
    for l in voltages:
        print("--------------")
        for key in l.keys():
            print(key, l[key])
    return jsonify(
        {'htmlresponse': render_template('product/runid_overview_with_dash.html',
                                         probes=probes,
                                         test_points=test_points,
                                         ats_version=ats_version,
                                         technician=technician.title(),
                                         test_station=test_station,
                                         configuration=configuration,
                                         board_id=board_id,
                                         pba=pba,
                                         serial_number=serial,
                                         rework=rework,
                                         status=status,
                                         status_info=status_info,
                                         comments=comments,
                                         tests_run=tests_run_str,
                                         runid=runid[3:]
                                         )})
