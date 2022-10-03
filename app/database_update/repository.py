from Entities.Entities import *
import typing as t


class Repository(object):

    def __init__(self, database):
        self.db = database

    def insert(self, entity: Entity):
        raise NotImplemented

    def retrieve_project(self, name: str) -> ProjectEntity:
        return self._retrieve_project(name=name)

    def _retrieve_project(self, name: str) -> ProjectEntity:
        raise NotImplemented

    def retrieve_pba(self, name: str) -> PBAEntity:
        return self._retrieve_pba(name=name)

    def _retrieve_pba(self, name: str) -> PBAEntity:
        raise NotImplemented

    def retrieve_rework(self, name: str) -> ReworkEntity:
        return self._retrieve_rework(name=name)

    def _retrieve_rework(self, name: str) -> ReworkEntity:
        raise NotImplemented

    def retrieve_serial_number(self, name: str) -> SubmissionEntity:
        return self._retrieve_serial_number(name=name)

    def _retrieve_serial_number(self, name: str) -> SubmissionEntity:
        raise NotImplemented

    def retrieve_runid(self, name: str) -> RunidEntity:
        return self._retrieve_runid(name=name)

    def _retrieve_runid(self, name: str) -> RunidEntity:
        raise NotImplemented

    def retrieve_test(self, name: str) -> AutomationTestEntity:
        return self._retrieve_test(name=name)

    def _retrieve_test(self, name: str) -> AutomationTestEntity:
        raise NotImplemented

    def retrieve_capture(self, name: str):
        return self._retrieve_capture(name=name)

    def _retrieve_capture(self, name: str):
        raise NotImplemented

    def retrieve_waveform(self, name: str) -> WaveformEntity:
        return self._retrieve_waveform(name=name)

    def _retrieve_waveform(self, name: str) -> WaveformEntity:
        raise NotImplemented
