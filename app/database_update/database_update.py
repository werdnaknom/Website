import logging
import typing as t

from .directory_repository import DirectoryRepository
from .error_repository import MongoErrorHandler
from .mongo_repository import MongoRepository
from app.extensions import mongo
from Entities.Entities import *

from config import DirectoryConfig

logger = logging.getLogger(__name__)


def upload(entity: Entity, repo):
    logger.info(f"Uploading {entity.descriptor} to repo")
    repo.insert_entity(entity=entity)


def directory_to_mongo(error_repo, mongo_repo, path_iter: t.Iterable[Path], from_dict_func, entity: Entity):
    for path in path_iter:
        try:
            logger.info(f"Uploading {entity.get_type()} from {path}")
            new_entity = from_dict_func(path)
            upload(new_entity, repo=mongo_repo)
        except Exception as e:
            error_repo.write_error(traceback=e,
                                   path=str(path.resolve()),
                                   message=f"Failed to create {entity.get_type()}")


def capture_to_mongo(error_repo, mongo_repo, path_iter: t.Iterable[Path], from_dict_func):
    for path in path_iter:
        try:
            logger.info(f"Uploading Capture Entity from {path}")
            new_entity = from_dict_func(path)
            upload(new_entity, repo=mongo_repo)
        except Exception as e:
            error_repo.write_error(traceback=e,
                                   path=str(path.resolve()),
                                   message=f"Failed to create capture entity")


def waveforms_to_mongo(error_repo, mongo_repo, path_iter: t.Iterable[Path], from_dict_func, entity: Entity):
    for path in path_iter:
        try:
            logger.info(f"Uploading {entity.get_type()} from {path}")
            new_entity_list = from_dict_func(path)
            for new_entity in new_entity_list:
                upload(new_entity, repo=mongo_repo)
        except Exception as e:
            error_repo.write_error(traceback=e,
                                   path=str(path.resolve()),
                                   message=f"Failed to create {entity.get_type()}")


def update_database(query):
    harddrives = DirectoryConfig.HARDDRIVE_DIRECTORIES
    error_repo = MongoErrorHandler()
    mongo_repo = mongo

    for base_directory in harddrives:
        directory_repo = DirectoryRepository(error_handler=error_repo,
                                             directory=base_directory)

        ordered_keys = ["product", "pba", "rework", "serial", "runid"]
        pattern = ""
        for key in ordered_keys:
            print("RUNNING DATABASE UPDATE:", )
            if key == "product":
                pattern = query[key]
            else:
                pattern += "/" + query[key]
            globs = directory_repo._directory_glob(match_pattern=pattern)
            if key == "product":
                entity = ProjectEntity
                func = directory_repo.from_directory_project
                directory_to_mongo(error_repo, mongo_repo, globs, func, entity)
            elif key == "pba":
                func = directory_repo.from_directory_pba
                entity = PBAEntity
                directory_to_mongo(error_repo, mongo_repo, globs, func, entity)
            elif key == "rework":
                func = directory_repo.from_directory_rework
                entity = ReworkEntity
                directory_to_mongo(error_repo, mongo_repo, globs, func, entity)
            elif key == "serial":
                func = directory_repo.from_directory_serial
                entity = SubmissionEntity
                directory_to_mongo(error_repo, mongo_repo, globs, func, entity)
            elif key == "runid":
                func = directory_repo.from_directory_runid
                entity = RunidEntity
                directory_to_mongo(error_repo, mongo_repo, globs, func, entity)
                ''' Test '''
                iter = directory_repo.list_test_paths(query=query)
                func = directory_repo.from_directory_test
                entity = AutomationTestEntity
                directory_to_mongo(error_repo, mongo_repo, iter, func, entity)

                ''' Captures '''
                iter = directory_repo.list_capture_paths(query=query)
                func = directory_repo.from_directory_capture
                capture_to_mongo(error_repo, mongo_repo, iter, func)

                ''' Waveforms '''
                iter = directory_repo.list_runid_paths(query=query)
                func = directory_repo.from_runid_directory_add_waveforms
                entity = WaveformEntity
                waveforms_to_mongo(error_repo, mongo_repo, iter, func, entity)
    return "Complete!"


def run_me(base_directory: str = DirectoryConfig.ATS2_OR):
    error_repo = MongoErrorHandler()
    directory_repo = DirectoryRepository(error_handler=error_repo,
                                         directory=base_directory)
    mongo_repo = MongoRepository()

    ''' PROJECT '''
    iter = directory_repo.list_project_paths()
    func = directory_repo.from_directory_project
    entity = ProjectEntity
    directory_to_mongo(error_repo, mongo_repo, iter, func, entity)

    ''' PBA '''
    iter = directory_repo.list_pba_paths()
    func = directory_repo.from_directory_pba
    entity = PBAEntity
    directory_to_mongo(error_repo, mongo_repo, iter, func, entity)

    ''' REWORK '''
    iter = directory_repo.list_rework_paths()
    func = directory_repo.from_directory_rework
    entity = ReworkEntity
    directory_to_mongo(error_repo, mongo_repo, iter, func, entity)

    ''' Serial '''
    iter = directory_repo.list_serial_number_paths()
    func = directory_repo.from_directory_serial
    entity = SubmissionEntity
    directory_to_mongo(error_repo, mongo_repo, iter, func, entity)

    ''' Runid '''
    iter = directory_repo.list_runid_paths()
    func = directory_repo.from_directory_runid
    entity = RunidEntity
    directory_to_mongo(error_repo, mongo_repo, iter, func, entity)

    ''' Test '''
    iter = directory_repo.list_test_paths()
    func = directory_repo.from_directory_test
    entity = AutomationTestEntity
    directory_to_mongo(error_repo, mongo_repo, iter, func, entity)

    ''' Captures '''
    iter = directory_repo.list_capture_paths()
    func = directory_repo.from_directory_capture
    capture_to_mongo(error_repo, mongo_repo, iter, func)

    ''' Waveforms '''
    iter = directory_repo.list_runid_paths()
    func = directory_repo.from_runid_directory_add_waveforms
    entity = WaveformEntity
    waveforms_to_mongo(error_repo, mongo_repo, iter, func, entity)
