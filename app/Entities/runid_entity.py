from app.Entities.entity import Entity, RUNID
from app.Entities.testcategory_entity import TestCategory
from app.Entities.domain_model import DomainModel

from config import RUNIDFILTERS, RUNIDOPERATORS

'''
STATUS.JSON
{   "Status":   "Aborted",
    "Time":     "1/29/2019 11:10 AM",
    "Info":     "Test was aborted by user after 0 Hours 43 Minutes 32 Seconds",
    "Runtime":  {"Total Seconds":2612,
                "Hours":0,
                "Minutes":43,
                "Seconds":32
                }
}

testrun.JSON
{   "DUT":              "Testing",
    "PBA":              "J12345-001",
    "Rework":           "RWK 10",
    "Serial Number":    "1337",
    "Technician":       "Steve",
    "Test Station":     "lno-test-dev",
    "Test Points":  ["PCIE 12V Main",
                    "PCIE 3.3V Main",
                    "PCIE 3.3V Aux",
                    "",
                    "",
                    "",
                    "",
                    "PCIE 3.3V Current"]
}
'''

IGNORED_COLUMNS = []


class Runid(Entity):
    '''
    Has an ID, several setup json files, and a list of tests
    '''

    def __init__(self, runid, tests=[]):
        super(Runid, self).__init__(descriptor=runid,
                                    next_list=tests,
                                    next_entity=TestCategory,
                                    filters_list=RUNIDFILTERS,
                                    operators_list=RUNIDOPERATORS)
        self._type = RUNID
        self._comments = ""


    @property
    def storedTemperatures(self):
        return self._storedTemperatures

    @property
    def storedVoltages(self):
        return self._storedVoltages

    @property
    def comments(self):
        return self._comments

    @property
    def runid(self):
        return self.descriptor

    '''Status json'''

    @property
    def status(self):
        value = self.get_json_field(json_name="status", field="Status", expected_type="")
        return value

    @property
    def time(self):
        value = self.get_json_field(json_name="status", field="Time", expected_type="")
        return value

    @property
    def info(self):
        value = self.get_json_field(json_name="status", field="Info", expected_type="")
        return value

    @property
    def runtime(self):
        value = self.get_json_field(json_name="status", field="Runtime", expected_type={})
        return value

    ''' testrun.json'''

    @property
    def dut(self):
        value = self.get_json_field("testrun", field="DUT", expected_type="")
        return value

    @property
    def pba(self):
        value = self.get_json_field("testrun", field="PBA", expected_type="")
        return value

    @property
    def rework(self):
        value = self.get_json_field("testrun", field="Rework", expected_type="")
        return value

    @property
    def serial_number(self):
        value = self.get_json_field("testrun", field="Serial Number", expected_type="")
        return value

    @property
    def technician(self):
        value = self.get_json_field("testrun", field="Technician", expected_type="")
        return value

    @property
    def test_station(self):
        value = self.get_json_field("testrun", field="Test Station", expected_type="")
        return value

    @property
    def test_points(self):
        value = self.get_json_field("testrun", field="Test Points", expected_type=[])
        return value

    @classmethod
    def _from_dict(cls, adict):
        tr = Runid(runid=adict['runid'], tests=[TestCategory._from_dict(test) for test in adict['tests']])
        desc = adict.get('json_descriptors', dict)
        for key, value in desc.items():
            tr.add_json_descriptor(name=key, json_dict=value)

        tr.add_files(adict.get('files', []))
        tr.set_comments(adict.get("comments", ""))
        return tr

    def _to_dict(self):
        to_dict = self._to_dataframe_json()
        to_dict['json_descriptors'] = self.json_descriptors
        to_dict['tests'] = [test.to_dict() for test in self.get_next()]
        to_dict['comments'] = self.comments
        return to_dict

    def _to_dataframe_json(self):
        return {'runid': self.descriptor,
                'comments': self.comments}

    def set_comments(self, comments):
        self._comments = comments

    def add_comments(self):
        files = self.get_files()
        comment_files = [file for file in files if "Comments" in file.name and file.suffix == ".txt"]
        comments = ""
        oldRead = None
        for comment in comment_files:
            with open(comment, "r") as f:
                newRead = f.read()
                if oldRead != newRead:
                    comments += newRead + '\n'
                #oldRead = newRead
            break
        self._comments = comments.strip()




DomainModel.register(Runid)
