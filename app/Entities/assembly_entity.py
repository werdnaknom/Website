from app.Entities.entity import Entity, ASSEMBLY
from app.Entities.rework_entity import Rework

from app.Entities.domain_model import DomainModel

from config import ASSEMBLYFILTERS, ASSEMBLYOPERATORS


class SpeedAssembly(Entity):
    def __init__(self, pba, versions=[]):
        super(SpeedAssembly, self).__init__(descriptor=pba,
                                            next_list=versions,
                                            next_entity=Rework,
                                            filters_list=ASSEMBLYFILTERS,
                                            operators_list=ASSEMBLYOPERATORS)
        self._type = ASSEMBLY
        self._base, self._dash = self._ipn_separate()

    @property
    def pba(self):
        return self.descriptor

    @property
    def dash(self):
        return self._dash

    @property
    def base(self):
        return self._base

    def _ipn_separate(self):
        if self.descriptor.find("-") > 0:
            base, dash = self.descriptor.split("-")
        else:
            base = self.descriptor
            dash = ""
        return base, dash

    @classmethod
    def _from_dict(cls, adict):
        assembly = SpeedAssembly(pba=adict['pba'],
                                 versions=[Rework._from_dict(ver) for ver in adict.get("versions", [])])

        return assembly

    def _to_dict(self):
        to_dict = self._to_dataframe_json()
        to_dict['versions'] = [version.to_dict() for version in self.get_next()]
        return to_dict

    def _to_dataframe_json(self):
        dataframe_json = {'pba': self.descriptor,
                          'base': self.base,
                          'dash': self.dash
                          }
        return dataframe_json


DomainModel.register(SpeedAssembly)
