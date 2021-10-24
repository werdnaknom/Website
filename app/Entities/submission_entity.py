from app.Entities.entity import Entity, SUBMISSION
from app.Entities.runid_entity import Runid
from app.Entities.domain_model import DomainModel

from config import SUBMISSIONOPERATORS, SUBMISSIONFILTERS


class Submission(Entity):
    '''
    Has an ID, PBA, and Software and a list of associated submission ID
    '''
    def __init__(self, serial_number, testruns=[]):
        super(Submission, self).__init__(descriptor=serial_number,
                                         next_list=testruns,
                                         next_entity=Runid,
                                         filters_list=SUBMISSIONFILTERS,
                                         operators_list=SUBMISSIONOPERATORS)
        self._type = SUBMISSION

    @property
    def serial_number(self):
        return self.descriptor

    @classmethod
    def _from_dict(cls, adict):
        rework = Submission(serial_number=adict['serial_number'],
                            testruns=[Runid._from_dict(testrun) for testrun in adict.get('testruns', [])])
        rework.add_files(adict.get('files', []))
        return rework

    def _to_dict(self):
        to_dict = self._to_dataframe_json()
        to_dict['testruns'] = [tr.to_dict() for tr in self.get_next()]
        return to_dict

    def _to_dataframe_json(self):
        return {'serial_number': self.descriptor}

    '''
    def _apply_filters(self, key, operator, value):
        result = []
        if getattr(self.descriptor, operator)(value):
            result.append(self)
        return result
    

    def get_columns(self):
        return ['serial_number']

    def get_data(self):
        return [self.descriptor]
    '''

DomainModel.register(Submission)
