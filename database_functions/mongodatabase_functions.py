import typing as t

from database_functions.database_functions import DatabaseFunctions
from config import Config
from app.extensions import mongo


class MongoDatabaseFunctions(DatabaseFunctions):

    @staticmethod
    def list_products():
        cursor = mongo.db[Config.PRODUCT].distinct("name")
        r = list(cursor)
        return r

    @staticmethod
    def find_product(product: str) -> t.Dict:
        cursor = mongo.db[Config.PRODUCT].find_one({"name": product})
        return cursor

    @staticmethod
    def find_pbas_by_product(product: str) -> t.List[str]:
        cursor = mongo.db[Config.PBA].distinct("part_number", {"project": product})
        return cursor

    @staticmethod
    def count_pbas_by_product(product: str) -> int:
        pbas = MongoDatabaseFunctions.find_pbas_by_product(product)
        return pbas

    @staticmethod
    def find_pba_entity_by_product(product: str) -> t.List[t.Dict]:
        cursor = mongo.db[Config.PBA].find({"project": product})
        r = list(cursor)
        return r

    @staticmethod
    def find_reworks_by_pba(pba: str) -> t.List[int]:
        cursor = mongo.db[Config.REWORK].find({"pba": pba}, {"_id": 0, "rework": 1})
        r = list(cursor)
        return r

    @staticmethod
    def count_reworks_by_product(product: str) -> t.List[str]:
        count = 0
        pbas = MongoDatabaseFunctions.find_pbas_by_product(product)
        for pba in pbas:
            reworks = MongoDatabaseFunctions.find_reworks_by_pba(pba)
            count += len(reworks)
        return count

    @staticmethod
    def find_rework_entities_by_product(product: str) -> t.List[t.Dict]:
        reworks = []
        pbas = MongoDatabaseFunctions.find_pbas_by_product(product)
        for pba in pbas:
            reworks.extend(MongoDatabaseFunctions.find_rework_entity_by_pba(pba))

        return reworks

    @staticmethod
    def find_rework_entity_by_pba(pba: str) -> t.List[t.Dict]:
        cursor = mongo.db[Config.REWORK].find({"pba": pba})
        r = list(cursor)
        return r

    @staticmethod
    def find_runids_by_product(product: str) -> t.List[str]:
        cursor = mongo.db[Config.RUNID].find({"project": product}, {"_id": 1})
        r = list(cursor)
        return r

    @staticmethod
    def find_runid_entities_by_product(product:str) -> t.List[t.Dict]:
        cursor = mongo.db[Config.RUNID].find({"project": product})
        r = list(cursor)
        return r

