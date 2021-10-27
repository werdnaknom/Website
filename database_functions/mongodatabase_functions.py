from database_functions.database_functions import DatabaseFunctions
from config import Config
from app.extensions import mongo



class MongoDatabaseFunctions(DatabaseFunctions):

    @staticmethod
    def list_products():
        r = mongo.db[Config.PRODUCT].distinct("name")
        r = list(r)
        return r

    @staticmethod
    def find_product(product: str):
        r = mongo.db[Config.PRODUCT].find_one({"name": product})
        return r

