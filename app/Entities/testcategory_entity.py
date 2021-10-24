from app.Entities.entity import Entity, TESTCATEGORY
from .capture_entity import Capture
from app.Entities.domain_model import DomainModel

from config import TESTCATEGORYFILTERS, TESTCATEGORYOPERATORS


class TestCategory(Entity):
    '''
    Has a dut, parent class to many tests which return lists of waveforms
    '''
    def __init__(self, test_category, captures=[]):
        super(TestCategory, self).__init__(descriptor=test_category,
                                           next_list=captures,
                                           next_entity=Capture,
                                           filters_list=TESTCATEGORYFILTERS,
                                           operators_list=TESTCATEGORYOPERATORS)
        self._type = TESTCATEGORY

    @property
    def test_category(self):
        return self.descriptor

    @classmethod
    def _from_dict(cls, adict):
        tc = TestCategory(test_category=adict['test_category'],
                          captures=[Capture._from_dict(sub) for sub in adict['captures']])
        return tc

    def _to_dict(self):
        to_dict = self._to_dataframe_json()
        to_dict['captures'] = [c.to_dict() for c in self.get_next()]
        return to_dict

    def _to_dataframe_json(self):
        return {"test_category": self.descriptor}

    def _get_temperatures(self):
        temps = set()
        for capture in self.captures:
            cap_list = capture.retrieve_stored_temperatures()
            for temp in cap_list:
                temps.add(temp)
        return list(temps)


    def _get_voltage_rails_and_values(self):
        result_dict = {}
        for next in self.get_next():
            next_dict = next.retrieve_stored_voltages()
            for key, value in next_dict.items():
                if key in result_dict:
                    for voltage in value:
                        if voltage not in result_dict[key]:
                            result_dict[key].append(voltage)
                else:
                    result_dict[key] = value
        return result_dict

    '''
    def _apply_filters(self, key, operator, value):
        result = []
        if getattr(self.descriptor, operator)(value):
            result.append(self)
        return result
    

    def get_columns(self):
        return ['test_category']

    def get_data(self):
        return [self.descriptor]
    '''

"""
class StartUpTestCategory(TestCategory):
    '''
    Has a dut and a list of waveforms
    '''
    def __init__(self, captures=[]):
        super().__init__(test_category="startup", captures=captures)


class TrafficTestCategory(TestCategory):
    '''
    Has a dut and a list of waveforms
    '''
    def __init__(self, captures=[]):
        super().__init__(test_category="traffic", captures=captures)

DomainModel.register(StartUpTestCategory)
DomainModel.register(TrafficTestCategory)
"""


DomainModel.register(TestCategory)
