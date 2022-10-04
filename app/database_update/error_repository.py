import logging
import os

import pymongo

from Entities.Entities.error_entity import ErrorEntity
from config import MongoConfig as MC

logger = logging.getLogger(__name__)


class ErrorHandler():

    def __init__(self):
        pass

    def _insert_error(self, error: ErrorEntity):
        raise NotImplemented

    def write_error(self, traceback: Exception, message: str, path: str = None):
        raise traceback
        logger.warning(f"REPO ERROR HANDLER LOG: {message}")
        ee = ErrorEntity(error_traceback=str(traceback), error_msg=message, path=path)
        self._insert_error(error=ee)
        return ee


class MongoErrorHandler(ErrorHandler):

    def __init__(self):
        mongo_uri = MC.MONGO_URI
        client = pymongo.MongoClient(mongo_uri)
        self.db = client[MC.DATABASE_NAME]
        self.error_collection = self.db[ErrorEntity.get_type()]
        super(MongoErrorHandler, self).__init__()

    def _insert_error(self, error: ErrorEntity):
        logger.info(f"Inserting error: {error}")
        self.error_collection.insert_one(document=error.to_mongo())
