from flask import render_template, jsonify, Markup, send_file, current_app
import requests
from Entities.Entities import ProjectEntity, PBAEntity, ReworkEntity, RunidEntity
from app.product import bp
from io import BytesIO
import datetime

from database_functions.mongodatabase_functions import MongoDatabaseFunctions


# from bokeh.plotting import figure
# from bokeh.resources import CDN
# from bokeh.embed import file_html

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
    print(product_dict)
    product_entity = ProjectEntity.from_dict(product_dict)
    pbas = MongoDatabaseFunctions.find_pbas_by_product(product)
    reworks = MongoDatabaseFunctions.count_reworks_by_product(product)
    runids = MongoDatabaseFunctions.find_runids_by_product(product)

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
    pba_entities = []
    pbas = MongoDatabaseFunctions.find_pba_entity_by_product(product)

    for pba in pbas:
        pba_entity = PBAEntity.from_dict(pba)
        pba_entity.reworks.extend(MongoDatabaseFunctions.find_reworks_by_pba(pba_entity.part_number))
        pba_entities.append(pba_entity)
    return render_template('/product/product-pbas.html',
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
    rework_entities = []
    reworks = MongoDatabaseFunctions.find_rework_entities_by_product(product=product)

    for rework in reworks:
        rework_entity = ReworkEntity.from_dict(rework)
        rework_entities.append(rework_entity)
    return render_template('/product/product-reworks.html',
                           reworks_entities=rework_entities)


@bp.route('/products/<product>/runids')
def product_runids(product):
    runid_entities = []
    runids = MongoDatabaseFunctions.find_runid_entities_by_product(product)
    for runid in runids:
        print(runid["project"])
        runid_entity = RunidEntity.from_dict(runid)
        runid_entities.append(runid_entity)
        print(runid_entity)

    return render_template('product/product-runids.html',
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
    s = requests.Session()
    s.trust_env = False
    print(product)

    json_filter = {"filters": {"dut": product}}
    r = s.get(current_app.config["DATABASE"] + 'test/overview',
              json=json_filter)
    return jsonify(r.json())


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
