from app.Entities.entity import Entity, REWORK
from app.Entities.submission_entity import Submission
from app.Entities.domain_model import DomainModel

from config import REWORKOPERATORS, REWORKFILTERS


class Rework(Entity):
    '''
    Has an ID, PBA, and Software and a list of associated submission ID
    '''
    def __init__(self, rework, submissions=[], software=""):
        super(Rework, self).__init__(descriptor=rework,
                                     next_list=submissions,
                                     next_entity=Submission,
                                     filters_list=REWORKFILTERS,
                                     operators_list=REWORKOPERATORS)
        self.software = software
        self._type = REWORK

    @property
    def rework(self):
        return self.descriptor

    @classmethod
    def _from_dict(cls, adict):
        rework = Rework(rework=adict['rework'],
                        software=adict.get('software', ""),
                        submissions=[Submission._from_dict(sub) for sub in adict.get("submissions", [])])
        rework.add_files(adict.get('files', []))
        return rework

    def _to_dict(self):
        to_dict = self._to_dataframe_json()
        to_dict['submissions'] = [subid.to_dict() for subid in self.get_next()]
        return to_dict

    def _to_dataframe_json(self):
        return {'rework': self.descriptor,
                'software': self.software}

    '''
    def _apply_filters(self, key, operator, value):
        result = []
        if getattr(self.descriptor, operator)(value):
            result.append(self)
        return result
    

    def get_columns(self):
        return ['rework',
                'software',
                ]

    def get_data(self):
        return [self.descriptor,
                self.software]
    '''

DomainModel.register(Rework)
