from app.Entities.domain_model import DomainModel
from pathlib import Path

import os

PRODUCT = 'product'
ASSEMBLY = 'assembly'
REWORK = 'rework'
SUBMISSION = 'submission'
RUNID = 'runid'
TESTCATEGORY = 'testcategory'
WAVEFORM = 'waveform'
CAPTURE = 'capture'


class Entity(object):
    def __init__(self, descriptor, next_list=[], next_entity=None, filters_list=[], operators_list=[],
                 json_descriptors={}):
        self._descriptor = None
        self.descriptor = descriptor
        self.next_entity = next_entity
        self.next = []
        self.json_descriptors = {}
        self.dataframe_descriptors = {}
        self.add_json_descriptors(multi_json_dict=json_descriptors)
        self._filters = []
        self._operators = []
        self.add_next(next_list=next_list)
        self.filters = filters_list
        self.operators = operators_list
        self._type = None
        self._files = []
        self._storedTemperatures = []
        self._storedVoltages = {}

    ''' Functions Implemented by Subclasses! '''

    def get_type(self):
        return self._type

    @classmethod
    def from_dict(cls, adict):
        entity = cls._from_dict(adict=adict)
        entity.add_files(adict.get('files', []))
        entity.store_voltages(adict.get("storedVoltages", {}))
        entity.store_temperatures(adict.get('storedTemperatures', []))

        return entity

    @classmethod
    def _from_dict(cls, adict):
        raise NotImplementedError

    def to_dict(self):
        d = self._to_dict()
        d['files'] = [self.convert_to_windows_path_str(file) for file in self.get_files()]
        d['storedTemperatures'] = self.retrieve_stored_temperatures()
        d['storedVoltages'] = self.retrieve_stored_voltages()
        return d

    def _to_dict(self):
        raise NotImplementedError

    '''LIST HELPER FUNCTIONS'''

    def add_files(self, file_list):
        for file in file_list:
            if file not in self._files:
                self._files.append(Path(file))

    def get_files(self):
        # files = [Path(file) for file in self._files]
        # return files
        return self._files

    def files_to_dataframe_json(self):
        result_json = {}
        fmt = "file_{desc}_{filename}"
        for file in self.get_files():
            windows_path_str = self.convert_to_windows_path_str(file)
            file_df_name = fmt.format(desc=self.get_type(), filename=file.name)
            result_json[file_df_name] = windows_path_str
        return result_json

    @staticmethod
    def convert_to_windows_path_str(path):
        if not isinstance(path, Path):
            path = Path(path)
        if os.name == "posix":
            # Turn path to Windows Path on Docker host
            return r"/{}".format(path.resolve())
        else:
            return str(path.resolve())

    @staticmethod
    def convert_to_linux_path_str(path):
        if not isinstance(path, Path):
            path = Path(path)
        if os.name == "posix":
            # Turn path to Windows Path on Docker host
            return r"/{}".format(path.resolve())
        else:
            return str(path.resolve())

    @staticmethod
    def separate_key_from_operators(filter_key):
        if '__' not in filter_key:
            filter_key = filter_key + '__eq'
        key, operator = filter_key.split('__')
        return key, operator

    def applicable_filters(self, filters_dict):
        applicable_filters = []
        for filters_key in filters_dict.keys():
            key, operator = self.separate_key_from_operators(filters_key)
            if key in self.filters:
                applicable_filters.append(filters_key)
        return applicable_filters

    def list(self, filters=None):
        result = [self]
        if filters:
            entity_filters = self.applicable_filters(filters)
            if entity_filters:
                for key_op in entity_filters:
                    key, operator = self.separate_key_from_operators(key_op)

                    value = filters.pop(key_op)
                    if operator not in self.operators:
                        raise KeyError('"{}" not in {} operators.  Available operators are: {}'.format(operator,
                                                                                                       self.descriptor,
                                                                                                       self.operators))
                    operator = "__{}__".format(operator)
                    '''
                    print(self.__getattribute__(key), key, operator, value,
                          getattr(self.__getattribute__(key), operator)(value))
                    '''
                    if key == "dut":
                        result = [r for r in result if
                                  getattr(self.__getattribute__(key).upper(), operator)(value.upper())]
                    else:
                        result = [r for r in result if getattr(self.__getattribute__(key), operator)(value)]
            if filters:
                next_list = []
                for next_entity in self.get_next():
                    new_filters = filters.copy()
                    next_list.extend(next_entity.list(filters=new_filters))
                self.set_next(next_list)
                # print(self.get_next())
                if not self.get_next():
                    result = []
            return result
        else:
            return result

    def _get(self, entity_type):
        result = []
        if entity_type == self._type:
            result.extend([self])
        else:
            for entity in self.get_next():
                result.extend(entity._get(entity_type=entity_type))
        return result

    ''' PROPERTY FUNCTIONS'''

    @property
    def waveforms(self):
        return self._get(WAVEFORM)

    @property
    def pbas(self):
        return self._get(ASSEMBLY)

    @property
    def reworks(self):
        return self._get(REWORK)

    @property
    def reworks_string_list(self):
        reworks = self.reworks
        string_list = [str(r.descriptor) for r in reworks]
        return string_list

    @property
    def submissions(self):
        return self._get(SUBMISSION)

    @property
    def runids(self):
        return self._get(RUNID)

    @property
    def status_runids(self):
        runids = self.runids
        statuses = [runid.status for runid in runids]
        return statuses

    @property
    def tests(self):
        return self._get(TESTCATEGORY)

    @property
    def tests_unique(self):
        tests = self.tests
        unique = set([test.descriptor for test in tests])
        return list(unique)

    @property
    def captures(self):
        return self._get(CAPTURE)

    @property
    def submission_numbers(self):
        submissions = self.submissions
        numbers = set(sub.descriptor for sub in submissions)
        return list(numbers)

    @property
    def waveform_names(self):
        waveforms = self.waveforms
        names = set([wf.descriptor for wf in waveforms])
        return list(names)

    @property
    def filters(self):
        return self._filters

    @property
    def operators(self):
        return self._operators

    @filters.setter
    def filters(self, filters_list):
        result = self._check_list(new_list=filters_list,
                                  expected_element_type=str)
        self._filters = result

    def add_filters(self, filters):
        result = self._check_list(filters, expected_element_type=str)
        self._filters.extend(result)

    @operators.setter
    def operators(self, operators_list):
        result = self._check_list(new_list=operators_list,
                                  expected_element_type=str)
        self._operators = result

    def add_operators(self, operator_list):
        result = self._check_list(operator_list,
                                  expected_element_type=str)
        self._operators.extend(result)

    @property
    def descriptor(self):
        return self._descriptor

    @descriptor.setter
    def descriptor(self, descriptor):
        self._descriptor = descriptor

    @property
    def descriptor_comparison(self, comparison):
        raise NotImplementedError

    def get_next(self):
        return self.next

    def set_next(self, sub_entity_list):
        self.next = []
        self.add_next(next_list=sub_entity_list)

    def add_next(self, next_list):
        result = self._check_list(new_list=next_list,
                                  expected_element_type=self.get_next_entity())
        self.next.extend(result)

    def get_next_entity(self):
        return self.next_entity

    '''
    def get_columns(self):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError
    '''

    @staticmethod
    def _check_list(new_list, expected_element_type):
        result_list = []
        if not isinstance(new_list, list):
            raise TypeError("'{}' must be type list. Is type '{}'".format(new_list, type(new_list)))
        else:
            for element in new_list:
                if not isinstance(element, expected_element_type):
                    raise TypeError("'{}' must be type '{}'. Is type '{}'".format(new_list,
                                                                                  expected_element_type,
                                                                                  type(element)))
                else:
                    result_list.append(element)
        return result_list

    ''' JSON Functions '''

    def add_json_descriptor(self, name, json_dict):
        assert isinstance(name, str), 'json_descriptor name must be a string. You entered {}'.format(name)
        if name == 'power':
            # TODO: Need to do something with POWER!
            pass
        elif isinstance(json_dict, list):
            for i, value in enumerate(json_dict):
                fmt = "{}_{}"
                self.json_descriptors[fmt.format(name, i)] = value
        else:
            assert isinstance(json_dict, dict), 'json_descriptors must be a dict. You entered type "{}": "{}"' \
                .format(type(json_dict),
                        json_dict)
            self.json_descriptors[name] = json_dict

            json_dataframe = self.json_descriptor_to_dataframe_dict(name="{}_json".format(name),
                                                                    json_descriptor=json_dict)
            self.dataframe_descriptors[name] = json_dataframe
            self.add_filters(list(json_dataframe.keys()))
            # print(json_dataframe)

    def add_json_descriptors(self, multi_json_dict):
        if not isinstance(multi_json_dict, dict):
            raise TypeError('"{}" must be of type dict'.format(multi_json_dict))
        for key, value in multi_json_dict.items():
            self.add_json_descriptor(name=key, json_dict=value)

    def get_json(self, json_name):
        desc = self.json_descriptors.get(json_name, {})
        return desc

    def get_json_field(self, json_name, field, expected_type=""):
        json_file = self.get_json(json_name=json_name)
        result = json_file.get(field, expected_type)
        return result

    def _get_json_columns(self, header, value):
        columns = []
        fmt = '{header}_{value}'
        header = header.lower().replace(" ", "_")
        if not isinstance(value, dict) and not isinstance(value, list):
            columns.extend([header])
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    for key, v in item.items():
                        list_header = fmt.format(header=header, value=key).lower().replace(" ", "_")
                        list_header += "_" + str(i + 1)
                        columns.extend(self._get_json_columns(header=list_header, value=v))
                else:
                    list_header = header + "_" + str(i + 1)
                    columns.extend([list_header])
        elif isinstance(value, dict):
            for key, value in value.items():
                dict_header = fmt.format(header=header, value=key).lower().replace(" ", "_")
                columns.extend(self._get_json_columns(header=dict_header, value=value))
        return columns

    def _get_json_data(self, header, value):
        data = []
        if not isinstance(value, dict) and not isinstance(value, list):
            data.extend([value])
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    for key, v in item.items():
                        data.extend(self._get_json_data(header=header, value=v))
                else:
                    data.extend([item])
        elif isinstance(value, dict):
            for k, v in value.items():
                data.extend(self._get_json_data(header=k, value=v))
        return data

    def _to_dataframe_json(self):
        raise NotImplementedError

    def _build_entity_dataframe_json(self):
        json_dict = {}
        file_dict = {}
        json_dict = self._to_dataframe_json()
        for json_descriptor, json_content in self.json_descriptors.items():
            json_name = "{}_{}".format(json_descriptor, "json")
            flattened_jsons = self.json_descriptor_to_dataframe_dict(name=json_name,
                                                                     json_descriptor=json_content)
            json_dict.update(flattened_jsons)

        file_dict = self.files_to_dataframe_json()
        json_dict.update(file_dict)

        return json_dict

    def to_dataframe_json(self):
        result = []
        entity_json = self._build_entity_dataframe_json()
        if self.get_next():
            for sub_entity in self.get_next():
                sub_json_list = sub_entity.to_dataframe_json()
                for sub_entity_json in sub_json_list:
                    entity_json_copy = entity_json.copy()
                    entity_json_copy.update(sub_entity_json)
                    result.append(entity_json_copy)
        else:
            result.append(entity_json)
        return result

    @staticmethod
    def json_descriptor_to_dataframe_dict(name, json_descriptor):
        dataframe_dict = {}
        std_fmt = "{name}_{column_name}"
        if isinstance(json_descriptor, list):
            list_dict = Entity._list_json_descriptor(name=name, list_descriptor=json_descriptor)
            dataframe_dict.update(list_dict)
        elif isinstance(json_descriptor, dict):
            dict_dict = Entity._dict_json_descriptor(name=name, dict_descriptor=json_descriptor)
            dataframe_dict.update(dict_dict)
        else:
            raise KeyError("Unexpected Json descriptor type! {}".format(json_descriptor))
        return dataframe_dict

    @staticmethod
    def _list_json_descriptor(name, list_descriptor):
        dataframe_dict = {}
        list_fmt = "{key}_{index}"
        assert isinstance(list_descriptor, list), "{} must be a list!".format(list_descriptor)
        for i, list_item in enumerate(list_descriptor):
            if isinstance(list_item, dict):
                descriptor_dict = Entity.json_descriptor_to_dataframe_dict(name, json_descriptor=list_item)
                for key, value in descriptor_dict.items():
                    dataframe_dict[list_fmt.format(key=key, index=i + 1)] = value
            else:
                key = list_fmt.format(key=name, index=i + 1)
                dataframe_dict[key] = list_item
        return dataframe_dict

    @staticmethod
    def _dict_json_descriptor(name, dict_descriptor):
        dataframe_dict = {}
        dict_fmt = "{name}_{column_name}"
        assert isinstance(dict_descriptor, dict), "{} must be a dict!".format(dict_descriptor)
        for column, value in dict_descriptor.items():
            key_name = dict_fmt.format(name=name, column_name=column).lower().replace(" ", "_")
            if isinstance(value, dict):
                result = Entity._dict_json_descriptor(name=key_name,
                                                      dict_descriptor=value)
                dataframe_dict.update(result)
            elif isinstance(value, list):
                result = Entity._list_json_descriptor(name=key_name, list_descriptor=value)
                dataframe_dict.update(result)
            else:
                dataframe_dict[key_name] = value
        return dataframe_dict

    @property
    def get_temperatures(self):
        return self.retrieve_stored_temperatures()

    @property
    def storedTemperatures(self):
        return self._storedTemperatures

    def store_temperatures(self, temperatures):
        assert isinstance(temperatures, list), "{} is not a list!".format(temperatures)
        self._storedTemperatures = temperatures

    def retrieve_stored_temperatures(self):
        if self.storedTemperatures:
            return self.storedTemperatures
        else:
            temps = self._get_temperatures()
            if None in temps:
                temps.remove(None)
            self.store_temperatures(temperatures=temps)
            return self.storedTemperatures

    def get_voltage_rails_and_values(self):
        return self.retrieve_stored_voltages()

    @property
    def storedVoltages(self):
        return self._storedVoltages

    def store_voltages(self, voltages):
        assert isinstance(voltages, dict)
        self._storedVoltages = voltages

    def retrieve_stored_voltages(self):
        if self.storedVoltages:
            return self.storedVoltages
        else:
            volt_dict = self._get_voltage_rails_and_values()
            self.store_voltages(voltages=volt_dict)
            return self.storedVoltages

    def _get_temperatures(self):
        temps = set()
        for next in self.next:
            cap_list = next.retrieve_stored_temperatures()
            for temp in cap_list:
                temps.add(temp)
        return list(temps)

    def _get_voltage_rails_and_values(self):
        result_dict = {}
        for next in self.get_next():
            next_dict = next.retrieve_stored_voltages()
            for key, value in next_dict.items():
                if key in result_dict:
                    for voltage in value:
                        if voltage not in result_dict[key]:
                            result_dict[key].append(voltage)
                else:
                    result_dict[key] = value
        return result_dict

    def get_runids_by_test_name(self, testname):
        runids_by_name = [runid for runid in self.runids if testname in runid.tests_unique]
        return runids_by_name

    def get_test_by_name(self, testname):
        tests = [test for test in self.tests if test.descriptor == testname]
        return tests

    def get_test_metrics(self, testname, status=None):
        result_list = []

        for runid in self.get_runids_by_test_name(testname):
            if status:
                if runid.status == status:
                    row_values = self._get_runid_test_metrics(runid)
                    result_list.append(row_values)
            else:
                row_values = self._get_runid_test_metrics(runid)
                result_list.append(row_values)

        return result_list

    def _get_runid_test_metrics(self, runid):
        row_values = dict()

        row_values["Runid"] = runid.descriptor

        row_values["PBA"] = runid.pba

        row_values["Serial Number"] = runid.serial_number

        row_values['Temperatures'] = runid.get_temperatures

        row_values.update(runid.get_voltage_rails_and_values())

        row_values['Automation Status'] = runid.status

        row_values['Comments'] = runid.comments

        return row_values


DomainModel.register(Entity)
