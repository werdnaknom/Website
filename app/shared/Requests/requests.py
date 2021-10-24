from __future__ import annotations

import collections
import os
import typing as t
import string
import random

import pandas as pd


from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


class RequestObject(object):

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__


class InvalidRequestObject(RequestObject):
    '''
    Can be converted to a "False" boolean for request validation.
    Contains validation errors to track why the request was invalid
    '''

    def __init__(self):
        self.errors = []

    def add_error(self, parameter, message):
        self.errors.append({'parameter': parameter,
                            'message': message})

    def has_errors(self):
        return len(self.errors) > 0

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__


class ValidRequestObject(RequestObject):
    '''
    Valid request object that can be a "True" boolean for request validation
    methods must be overridden by children or raises NotImplementedError
    '''

    @classmethod
    def from_dict(cls, adict):
        raise NotImplementedError

class TestRequest(ValidRequestObject):
    df: pd.DataFrame

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def to_dict(self):
        return {"dataframe": self.df.to_dict()}

    @classmethod
    def from_dict(cls, adict:dict) -> TestRequest:
        df = pd.DataFrame.from_dict(adict.get("dataframe", {}))
        return TestRequest(df=df)




class PostProcessingRequest(ValidRequestObject):

    def __init__(self, test_name: str, data_filename: str, data_file_path: str,
                 user_input_filename: str, user_input_file_path: str,
                 filter_by:str):
        self.test_name = test_name
        self.data_filename = data_filename
        self.data_file_path = data_file_path
        self.user_input_filename = user_input_filename
        self.user_input_file_path = user_input_file_path
        self.filter_by = filter_by

    @classmethod
    def save_file(cls, file: FileStorage) -> t.Tuple[str, str]:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename, file_path

    @classmethod
    def _random_name_generator(cls, name_length: int = 20):
        name = ''.join(random.sample(string.ascii_letters, name_length))
        return name

    @classmethod
    def save_duplicate_file(cls, file:FileStorage) -> t.Tuple[str,str]:
        name = cls._random_name_generator(name_length=20)
        filename = secure_filename(f"config_{name}.xlsx")
        file_path = os.path.join(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        file.save(file_path)
        return filename, file_path

    @classmethod
    def save_dataframe(cls, df: pd.DataFrame) -> t.Tuple[str, str]:
        name = cls._random_name_generator(name_length=20)
        filename = secure_filename(f"data_{name}.csv")
        file_path = os.path.join(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        df.to_csv(file_path)
        return filename, file_path

    def to_dict(self):
        return {"test_name": self.test_name,
                "data_filename": self.data_filename,
                "data_file_path": self.data_file_path,
                "user_input_filename": self.user_input_filename,
                "user_input_file_path": self.user_input_file_path,
                "filter_by": self.filter_by}

    @classmethod
    def from_dict(cls, adict):
        r = cls(**adict)
        return r


class ListRequestObject(ValidRequestObject):

    def __init__(self, filters=None):
        self.filters = filters

    @classmethod
    def from_dict(cls, adict):
        invalid_req = InvalidRequestObject()

        if 'filters' in adict and not isinstance(adict['filters'],
                                                 collections.Mapping):
            invalid_req.add_error('filters', 'Is not iterable')

        if invalid_req.has_errors():
            return invalid_req

        return ListRequestObject(filters=adict.get('filters', None))


class UpdatePickleRequestObject(ListRequestObject):
    pass
