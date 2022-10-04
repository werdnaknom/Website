import logging

from pymongo import MongoClient

from .repository import *
from config import MongoConfig as MC
from app.extensions import mongo

logger = logging.getLogger(__name__)


class MongoRepository(Repository):

    def __init__(self):
        mongo_uri = MC.MONGO_URI
        # self.client = MongoClient(mongo_uri)
        self.client = mongo
        # db = self.client[MC.DATABASE_NAME]
        # print(MC.DATABASE_NAME)
        # print(MC.MONGO_URI)
        # print(db)
        super(MongoRepository, self).__init__(database=self.client)

    def _retrieve_project(self, name: str) -> ProjectEntity:
        pass

    def insert_entity(self, entity: Entity):
        # TODO:: Update to find the actual _id instead of just count found.
        # TODO:: Then return the found _ID
        col = self.client.db[entity.get_type()]
        found = col.count_documents({"_id": entity.get_id()})
        # found = list(col.find({"_id": entity.get_id()}, {"_id":1}))
        # if found:
        #   return found
        if not found:
            # print("NOT FOUND, INSERTING", entity.to_dict())
            r = col.insert_one(document=entity.to_mongo())
            logger.info(f"Inserted {entity.descriptor} at {r.inserted_id}")
            # return r.inserted_ids
