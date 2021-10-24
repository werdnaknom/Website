from app.Entities.entity import Entity
from app.Entities.assembly_entity import SpeedAssembly
from app.Entities.domain_model import DomainModel

from config import PRODUCTFILTERS, PRODUCTOPERATORS


class Product(Entity):
    '''
    Has a dut, ID, and list of associated PBAs.
    Returns a list of associated PBAs
    '''

    def __init__(self, descriptor, board_assemblies=[]):
        super(Product, self).__init__(descriptor=descriptor,
                                      next_list=board_assemblies,
                                      next_entity=SpeedAssembly,
                                      filters_list=PRODUCTFILTERS,
                                      operators_list=PRODUCTOPERATORS)
        self._storedDataframe = None

    def save_Dataframe(self, dataframe):
        self._storedDataframe = dataframe

    def get_dataFrame(self):
        if self._storedDataframe:
            return self._storedDataframe
        else:
            df = self.to_dataframe_json()
            self.save_Dataframe(dataframe=df)
            return df

    @property
    def dut(self):
        return self.descriptor

    @classmethod
    def _from_dict(cls, adict):
        product = Product(descriptor=adict['dut'],
                          board_assemblies=[SpeedAssembly._from_dict(assembly)
                                            for assembly
                                            in adict.get('board_assemblies', [])])
        product.save_Dataframe(adict.get("dataframe", None))

        return product

    def _to_dict(self):
        to_dict = self._to_dataframe_json()
        to_dict['board_assemblies'] = [assembly.to_dict() for assembly in self.get_next()]
        to_dict['dataframe'] = self.get_dataFrame()
        return to_dict

    def _to_dataframe_json(self):
        return {"dut": self.descriptor}

    '''
    def _apply_filters(self, key, operator, value):
        result = []
        if getattr(self.descriptor, operator)(value):
            result.append(self)
        return result
    

    def get_columns(self):
        return ['dut']

    def get_data(self):
        return [self.descriptor]
    '''


DomainModel.register(Product)
