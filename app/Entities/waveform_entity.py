from app.Entities.entity import Entity, WAVEFORM
from app.Entities.domain_model import DomainModel

from zipfile import ZipFile
from pathlib import Path

# import numpy as np

from config import WAVEFORMFILTERS, WAVEFORMOPERATORS


class Waveform(Entity):

    def __init__(self, testpoint, channel, location):
        super(Waveform, self).__init__(descriptor=testpoint,
                                       next_entity=None,
                                       next_list=[],
                                       filters_list=WAVEFORMFILTERS,
                                       operators_list=WAVEFORMOPERATORS)
        self._scope_channel = channel
        self._location = Path(location)
        self._type = WAVEFORM
        self.__reader = None
        self._units = None
        self._compressed = True
        self._initial_x = None
        self._increment_x = None
        self._probel_cal_status = None
        self._probe_serial_number = None
        self._probe_type = None
        self.__wf = None
        self._wf_mean = None
        self._wf_max = None
        self._wf_min = None
        self._wf_pk2pk = None
        self._on_percent = 0.5

    '''
    def read_waveform(self):
        if not self.get_compressed():
            raise TypeError("Waveform not compressed!")
        f = ZipFile(self.location, 'r')
        f_name = f.namelist()
        w = f.read(f_name[0])
        f.close()
        dt = np.dype(float)
        wf = np.frombuffer(w, dtype=dt)
        return wf
    

    def set_waveform(self, wf):
        assert isinstance(wf, np.ndarray)
        self.__wf = wf
    
    
    def get_waveform(self):
        if self.__wf:
            return self.__wf
        else:
            wf = self.read_waveform()
            self.set_waveform(wf)
            return self.__wf
    

    def set_on_percent(self, on_percent):
        self._on_percent = on_percent

    @property
    def on_percent(self):
        return self._on_percent

    @staticmethod
    def _waveform_on_mean_by_location(wf, on_percent=0.5):
        waveform_cutoff = int(wf.size / (1 / on_percent))
        wf_mean = wf[waveform_cutoff:].mean()
        return wf_mean

    def get_waveform_mean(self):
        if self._wf_mean:
            return self._wf_mean
        else:
            wf = self.get_waveform()
            wf_mean = self._waveform_on_mean_by_location(wf, on_percent=self.on_percent)
            self.set_waveform_mean(wf_mean)

    def set_waveform_mean(self, value):
        self._wf_mean = value

    def set_waveform_max(self, value):
        self._wf_max = value

    def set_waveform_min(self, value):
        self._wf_min = value

    def set_waveform_pk2pk(self, value):
        self._wf_pk2pk = value
    '''

    @property
    def probe_cal_status(self):
        return self._probel_cal_status

    @property
    def probe_serial_number(self):
        return self._probe_serial_number

    @property
    def probe_type(self):
        return self._probe_type

    def set_probe_cal_status(self, status):
        self._probel_cal_status = status

    def set_probe_serial_number(self, sn):
        self._probe_serial_number = sn

    def set_probe_type(self, probe_type):
        self._probe_type = probe_type

    def set_incremement_x(self, increment_x):
        self._increment_x = increment_x

    @property
    def increment_x(self):
        return self._increment_x

    def set_initial_x(self, initial_x):
        self._initial_x = initial_x

    def probe_information(self):
        result = {}
        result["Calibration Status"] = self.probe_cal_status
        result["Serial Number"] = self.probe_serial_number
        result["Probe"] = self.probe_type
        result["Units"] = self.units
        return result

    @property
    def initial_x(self):
        return self._initial_x

    def set_compressed(self, compressed=True):
        assert isinstance(compressed, bool)
        self._compressed = compressed

    def get_compressed(self):
        return self._compressed

    @property
    def units(self):
        return self._units

    @classmethod
    def _from_dict(cls, adict):
        wf = Waveform(testpoint=adict['testpoint'],
                      channel=adict['scope_channel'],
                      location=adict['location'])
        desc = adict.get("json_descriptors", {})
        for key, value in desc.items():
            wf.add_json_descriptor(name=key, json_dict=value)
        wf.add_files(adict.get('files', []))
        return wf

    def _to_dict(self):
        to_dict = self._to_dataframe_json()
        to_dict['json_descriptors'] = self.json_descriptors
        return to_dict

    def _to_dataframe_json(self):
        return {'testpoint': self.descriptor,
                'scope_channel': self.scope_channel,
                'location': self.convert_to_windows_path_str(self.location),
                }

    @property
    def testpoint(self):
        return self.descriptor

    @property
    def location(self):
        return self._location

    @property
    def scope_channel(self):
        return self._scope_channel

    '''
    def _apply_filters(self, key, operator, value):
        result = []
        if key == 'testpoint':
            testpoint = self.descriptor()
            if getattr(testpoint, operator)(value):
                result.append(self)
        else:
            raise KeyError('key "{}" is not supported'.format(key))
        return result
    '''

    def setReader(self, reader):
        self.__reader = reader

    def read(self):
        return self.__reader.read()

    '''
    def get_columns(self):
        return ['testpoint',
                'scope_channel',
                'location',
                ]

    def get_data(self):
        return [self.descriptor,
                self.scope_channel,
                self.location]
    '''


class VoltageWaveform(Waveform):
    def __init__(self, testpoint, channel, location):
        super(VoltageWaveform, self).__init__(testpoint=testpoint, channel=channel, location=location)
        self._units = "V"


class CurrentWaveform(Waveform):
    def __init__(self, testpoint, channel, location):
        super(CurrentWaveform, self).__init__(testpoint=testpoint, channel=channel, location=location)
        self._units = "A"


DomainModel.register(Waveform)
