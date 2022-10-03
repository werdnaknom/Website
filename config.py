import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

"""
EntityBuilders Structure:
    Product, SpeedAssembly, Rework, Submission, Runid, TestCategory, Capture, Waveform
"""

DATADIRECTORY = os.getenv("OR_ATS_DIRECTORY") or r'\\npo\coos\LNO_Validation\Validation_Data\_data\ATS 2.0'
PICKLEDIRECTORY = os.getenv("PICKLEDIRECTORY") or r'\\npo\coos\LNO_Validation\Validation_Data\_data\ATS 2.0_pickle'

REPOSITORYFILTER = 'dut'
PRODUCTFILTERS = ["dut"]
ASSEMBLYFILTERS = ['pba', 'dash', 'base']
REWORKFILTERS = ['rework']
SUBMISSIONFILTERS = ['serial_number']
RUNIDFILTERS = ['runid', 'status', 'technician', 'test_station']
TESTCATEGORYFILTERS = ['test_category']
CAPTUREFILTERS = ['temperature', 'temperature_setpoint', 'nominal_power',
                  'voltage', 'slew', 'waveform', 'temp',
                  'capture']
WAVEFORMFILTERS = ['testpoint', "scope_channel"]

REPOSITORYOPERATORS = ['eq', 'ne']
PRODUCTOPERATORS = ['eq', 'ne']
ASSEMBLYOPERATORS = ['eq', 'ne']
REWORKOPERATORS = ['eq', 'lt', 'gt', 'ne']
SUBMISSIONOPERATORS = ['eq', 'lt', 'gt', 'ne']
RUNIDOPERATORS = ['eq', 'lt', 'gt', 'ne']
TESTCATEGORYOPERATORS = ['eq', 'ne']
SUBCATEGORYOPERATORS = ['eq', 'ne']
CAPTUREOPERATORS = ['eq', 'lt', 'gt', 'ne']
WAVEFORMOPERATORS = ['eq', 'lt', 'gt', 'ne']

STATUSKEYS = ['Status', "Time", "Info", "Runtime"]
TESTRUNKEYS = ['DUT', 'PBA', 'Rework', 'Serial Number', 'Technician',
               'Test Station', 'Test Points']
CAPTUREKEYS = ['initial x', 'x increment', 'names', 'compress', 'meta']
METAKEYS = ['Temperature Setpoint', 'Temperature', 'Power Supply'] + ['temp']

VALIDFILTERS = PRODUCTFILTERS + ASSEMBLYFILTERS + REWORKFILTERS + SUBMISSIONFILTERS + \
               RUNIDFILTERS + TESTCATEGORYFILTERS + CAPTUREFILTERS + WAVEFORMFILTERS + \
               []

TRAFFICTESTS = ["ethagent", "ripple"]

AGEFILE = 'testrun.json'


class Config(object):
    TESTING = False
    DEBUG = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # LOGGING CONFIG
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")

    # BABEL Config
    LANGUAGES = {
        "en": "English",
    }

    # SERVER FOLDER CONFIGURATION
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
    RESULTS_FOLDER = os.environ.get("RESULTS_FOLDER")

    DATADIRECTORY = os.environ.get("ATS_DATA_DIRECTORY")
    PICKLEDIRECTORY = os.environ.get("ATS_PICKLE_DIRECTORY")

    # DATABASE SETUP
    DATABASE = "MONGODB"
    # DATABASE = "PICKLEDB"
    # DATABASE = "DIRECTORYDB"

    # MONGODB SETUP
    MONGO_DBNAME = os.getenv("MONGO_DATABASE_NAME") or "ATS2"
    MONGO_URI = os.environ.get("MONGO_URI") or "mongodb://192.168.1.226:27017" + "/" + MONGO_DBNAME
    print("Database Name: ", MONGO_DBNAME)
    print("MONGO_URL: ", MONGO_URI)

    # BACKEND SETUP
    BACKEND_DOCKER = os.environ.get("BACKEND_DOCKER_NAME")
    BACKEND_PORT = os.environ.get("BACKEND_PORT")
    DATABASE_DOCKER_URL = f"http://{BACKEND_DOCKER}:{BACKEND_PORT}/"

    # TESTPLAN SETUP
    TESTPLAN_DOCKER = os.environ.get("TESTPLAN_DOCKER_NAME")
    TESTPLAN_PORT = os.environ.get("TESTPLAN_PORT")
    TESTPLAN = f"http://{TESTPLAN_DOCKER}:{TESTPLAN_PORT}/"

    # Redis Config
    redis_docker = os.environ.get("REDIS_DOCKER_NAME")
    redis_port = os.environ.get("REDIS_PORT")
    REDIS_URL = os.environ.get('REDIS_URL')

    # Celery Config
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    CELERY_ROUTES = {
        'post_processor': {
            'exchange': 'worker',  # -Q name during run command
            'exchange_type': 'direct',
            'routing_key': 'worker'  # -Q name during run command
        },
        'load_profile_one': {
            'exchange': 'worker',  # -Q name during run command
            'exchange_type': 'direct',
            'routing_key': 'worker'  # -Q name during run command
        },
        'waveform_reader_subtract': {
            'exchange': 'worker',  # -Q name during run command
            'exchange_type': 'direct',
            'routing_key': 'worker'  # -Q name during run command
        },
        'single_waveform': {
            'exchange': 'worker',  # -Q name during run command
            'exchange_type': 'direct',
            'routing_key': 'worker'  # -Q name during run command
        },
        'group_waveform': {
            'exchange': 'worker',  # -Q name during run command
            'exchange_type': 'direct',
            'routing_key': 'worker'  # -Q name during run command
        }
    }

    basedir = os.path.abspath(os.path.dirname(__file__))

    """
    EntityBuilders Structure:
        Product, SpeedAssembly, Rework, Submission, Runid, TestCategory, Capture,     Waveform
    """

    REPOSITORYFILTER = 'dut'
    PRODUCTFILTERS = ["dut"]
    ASSEMBLYFILTERS = ['pba', 'dash', 'base']
    REWORKFILTERS = ['rework']
    SUBMISSIONFILTERS = ['serial_number']
    RUNIDFILTERS = ['runid', 'status', 'technician', 'test_station']
    TESTCATEGORYFILTERS = ['test_category']
    CAPTUREFILTERS = ['temperature', 'temperature_setpoint', 'nominal_power',
                      'voltage', 'slew', 'waveform', 'temp',
                      'capture']
    WAVEFORMFILTERS = ['testpoint', "scope_channel"]

    REPOSITORYOPERATORS = ['eq', 'ne']
    PRODUCTOPERATORS = ['eq', 'ne']
    ASSEMBLYOPERATORS = ['eq', 'ne']
    REWORKOPERATORS = ['eq', 'lt', 'gt', 'ne']
    SUBMISSIONOPERATORS = ['eq', 'lt', 'gt', 'ne']
    RUNIDOPERATORS = ['eq', 'lt', 'gt', 'ne']
    TESTCATEGORYOPERATORS = ['eq', 'ne']
    SUBCATEGORYOPERATORS = ['eq', 'ne']
    CAPTUREOPERATORS = ['eq', 'lt', 'gt', 'ne']
    WAVEFORMOPERATORS = ['eq', 'lt', 'gt', 'ne']

    STATUSKEYS = ['Status', "Time", "Info", "Runtime"]
    TESTRUNKEYS = ['DUT', 'PBA', 'Rework', 'Serial Number', 'Technician',
                   'Test Station', 'Test Points']
    CAPTUREKEYS = ['initial x', 'x increment', 'names', 'compress', 'meta']
    METAKEYS = ['Temperature Setpoint', 'Temperature', 'Power Supply'] + [
        'temp']

    VALIDFILTERS = PRODUCTFILTERS + ASSEMBLYFILTERS + REWORKFILTERS + \
                   SUBMISSIONFILTERS + RUNIDFILTERS + TESTCATEGORYFILTERS + \
                   CAPTUREFILTERS + WAVEFORMFILTERS + []

    TRAFFICTESTS = ["ethagent", "ripple"]

    AGEFILE = 'testrun.json'

    PRODUCT = "PROJECT"
    PBA = "PBA"
    REWORK = "REWORK"
    RUNID = "RUNID"
    CAPTURE = "DATACAPTURE"
    WAVEFORM = "WAVEFORM"
    TESTPOINT = "TESTPOINT"


class MongoConfig(Config):
    MONGO_URI = os.environ.get("MONGO_URI") or "mongodb://npoflask.jf.intel.com:27017"
    DATABASE_NAME = "ATS2"


class DeploymentConfig(Config):
    pass


class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True

    # MONGODB SETUP
    MONGO_DBNAME = "ATS2"
    MONGO_URI = os.environ.get("MONGO_URI") or "mongodb://localhost:27017"  # Must setup in standalone docker
    redis_port = 6379
    REDIS_URL = 'redis://localhost'

    DATABASE_DOCKER_URL = "http://npoflask2.jf.intel.com:5001/"
    TESTPLAN = "http://npoflask2.jf.intel.com:5000/"

    UPLOAD_FOLDER = r"C:\Users\ammonk\OneDrive - Intel Corporation\Desktop\Test_Folder\fake_uploads"
    RESULTS_FOLDER = r"C:\Users\ammonk\OneDrive - Intel Corporation\Desktop\Test_Folder\fake_uploads\fake_results"

    DATADIRECTORY = r'\\npo\coos\LNO_Validation\Validation_Data\_data\ATS 2.0'
    PICKLEDIRECTORY = r'\\npo\coos\LNO_Validation\Validation_Data\_data\ATS     2.0_pickle'
    # Celery Config
    CELERY_BROKER_URL = "pyamqp://guest:guest@localhost:5672/vhost"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


class DirectoryConfig(Config):
    DATABASE_NAME = os.environ.get("OREGON_DIRECTORY") or r"\\npo\coos\LNO_Validation\Validation_Data\_data\ATS 2.0"
    ATS2_OR = os.environ.get("OREGON_DIRECTORY") or r"\\npo\coos\LNO_Validation\Validation_Data\_data\ATS 2.0"
    ATS2_KM = os.environ.get("KULIM_DIRECTORY") or r"\\npo\coos\LNO_Validation\Kulim\ATS 2.0 Data"
    HARDDRIVE_DIRECTORIES = [ATS2_OR, ATS2_KM]
    DIR_FMT_PROJECT = "{project}"
    PROJECT_DEPTH = 1
    DIR_FMT_PBA = "{project}/{pba}"
    PBA_DEPTH = 2
    DIR_FMT_REWORK = "{project}/{pba}/{rework}"
    REWORK_DEPTH = 3
    DIR_FMT_SERIAL = "{project}/{pba}/{rework}/{serial_number}"
    SERIAL_DEPTH = 4
    DIR_FMT_RUNID = "{project}/{pba}/{rework}/{serial_number}/{runid}"
    RUNID_DEPTH = 5
    DIR_FMT_TEST = "{project}/{pba}/{rework}/{serial_number}/{runid}/Tests/{test}"
    TEST_DEPTH = 7
    DIR_FMT_CAPTURE = "{project}/{pba}/{rework}/{serial_number}/{runid}/Tests/{test}/{capture}"
    CAPTURE_DEPTH = 8
    DIR_FMT_SCRIPTS_HOST = "{project}/{pba}/{rework}/{serial_number}/{runid}/Tests/{test}/{host}"
    HOSTS_DEPTH = 8

    TESTRUN_JSON_FILENAME = "testrun.json"
    SYSTEMINFO_JSON_FILENAME = "System Info.json"
    STATUS_JSON_FILENAME = "status.json"
    POWER_JSON_FILENAME = "power.json"
    POWER_CSV_FILENAME = "power.csv"
    COMMENT_FILENAME = "Comments.txt"
