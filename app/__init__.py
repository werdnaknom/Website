from flask import Flask, g, current_app
from config import Config
import requests
from flask_wtf import CSRFProtect
from celery import Celery
from database_functions.mongodatabase_functions import MongoDatabaseFunctions

from .extensions import mongo, bootstrap

celeryapp = Celery('web', broker='pyamqp://guest:guest@localhost:5672/vhost',
                   backend="redis://localhost:6379/0")


def init_celery(app: Flask):
    ''' Add flaskapp context to celery.Task'''
    celeryapp = Celery('web',
                       broker='pyamqp://guest:guest@localhost:5672/vhost',
                       backend="redis://localhost:6379/0")
    celeryapp.conf.update(app.config)

    class ContextTask(celeryapp.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                self.run(*args, **kwargs)

    celeryapp.Task = ContextTask
    return celeryapp


'''
def get_database(app: Flask, config_class: Config):
    """
    Configuration method to return db instance
    :return:
    """
    db_type = config_class.DATABASE
    if db_type == "MONGODB":
        MongoDatabaseFunctions.init()

    return db
'''


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    bootstrap.init_app(app)
    mongo.init_app(app)
    print(config_class.MONGO_URI, config_class.MONGO_DBNAME)

    # Configure Celery
    celeryapp = init_celery(app)

    # Configure Database
    # db = get_database(app, config_class)

    csrf = CSRFProtect(app)

    from app.display_images import bp as display_bp
    app.register_blueprint(display_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.product import bp as product_bp
    app.register_blueprint(product_bp)
    csrf.exempt(product_bp)

    from app.testplan import bp as testplan_bp
    app.register_blueprint(testplan_bp)

    from app.csv_json import bp as json_bp
    app.register_blueprint(json_bp)

    ''' All the test post processing '''
    from .post_processing import bp as post_processing_input_bp
    app.register_blueprint(post_processing_input_bp, url_prefix="/post")

    # Post Processing
    from .post_processing.tests import bp as postprocessing_bp
    app.register_blueprint(postprocessing_bp,
                           url_prefix='/postprocessing')
    # Bit Error Ratio
    from .post_processing.tests.ber import bp as ber_bp
    app.register_blueprint(ber_bp, url_prefix='/ber')

    # Edge Power
    from .post_processing.tests.edge_power import bp as edge_bp
    app.register_blueprint(edge_bp, url_prefix='/edgePower')

    # Inrush
    from .post_processing.tests.inrush import bp as inrush_bp
    app.register_blueprint(inrush_bp, url_prefix='/inrush')

    # Load Profile
    from .post_processing.tests.load_profile import bp as load_bp
    app.register_blueprint(load_bp, url_prefix='/load_profile')

    # Power-on Time
    from .post_processing.tests.on_time import bp as ontime_bp
    app.register_blueprint(ontime_bp, url_prefix='/PowerOnTime')

    # Sequencing
    from .post_processing.tests.sequencing import bp as seq_bp
    app.register_blueprint(seq_bp, url_prefix='/sequencing')

    # Voltage System Dynamics
    from .post_processing.tests.vsd import bp as vsd_bp
    app.register_blueprint(vsd_bp, url_prefix="/VoltageSystemDynamics")

    ''' DASH '''
    from .plotlydash.dash_setup import init_dash
    app = init_dash(app)
    csrf._exempt_views.add('dash.dash.dispatch')
    ''' END test post processing '''

    ''' Celery Task Pages '''
    from .post_processing.task_pages import bp as task_bp
    app.register_blueprint(task_bp, url_prefix="/Celery")

    @app.context_processor
    def utility_processor():
        def get_product_names():
            try:
                '''
                s = requests.Session()
                s.trust_env = False
                r = s.get(config_class.DATABASE + 'list')
                # return ["Need", "To", "Uncomment", "on", "server"]
                return r.json()
                '''
                products = MongoDatabaseFunctions.list_products()
                # return ["Need", "To", "Uncomment", "on", "server"]
                return products
            except:
                return ""

        def get_product_update_times():
            try:
                s = requests.Session()
                s.trust_env = False
                r = s.get(config_class.DATABASE_DOCKER_URL + 'products_update_time')
                print(r.json())
                return r.json()
            except:
                return ""

        return dict(product_names=get_product_names,
                    product_update_times=get_product_update_times)

    return app
