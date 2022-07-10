import typing as t
from dataclasses import dataclass

from Entities.Entities import RunidEntity, Entity
from flask import request, url_for, send_from_directory, send_file

from database_functions.mongodatabase_functions import MongoDatabaseFunctions


@dataclass
class FlaskPage():
    entity: Entity

    @staticmethod
    def get_previous_url():
        previous = request.referrer
        return previous

    def get_page_title(self) -> str:
        raise NotImplementedError

    def get_product(self) -> str:
        return self.entity.project

    def get_pba(self) -> str:
        return self.entity.pba

    def get_rework(self) -> str:
        return self.entity.rework

    def get_serial(self) -> str:
        return self.entity.serial

    def get_runid(self) -> str:
        return self.entity.runid

    def count_captures(self) -> int:
        raise NotImplementedError

    def get_temperatures(self) -> str:
        raise NotImplementedError


@dataclass
class RunidPage(FlaskPage):
    repo: MongoDatabaseFunctions
    title: str = None

    def __post_init__(self):
        self.title = "{product} Runid {runid}".format(product=self.get_product(),
                                                      runid=self.get_runid())

    def get_page_title(self) -> str:
        return self.title

    def get_runid(self):
        return self.entity.get_id()

    def get_status(self):
        return self.entity.status.status

    def count_captures(self) -> int:
        return self.repo.count_captures_by_runid(runid=self.entity.runid)

    def get_temperatures(self) -> str:
        return "0, 25, 60"

    def get_test_station(self) -> str:
        return self.entity.testrun.test_station.upper()

    def get_runtime(self) -> str:
        return self.entity.get_runtime()

    def get_configuration(self) -> str:
        return self.entity.testrun.configuration

    def get_power(self) -> float:
        return self.entity.power.max_power

    def get_technician(self) -> str:
        technician = self.entity.testrun.technician
        if technician != "":
            return technician.title()
        else:
            return "Test Runner"

    def get_user_comments(self) -> str:
        return "Test Comments go here"
        # return self.entity.comments.get_comments()

    def _get_distinct_test_categories(self) -> t.List[str]:
        result = self.repo.get_runid_test_categories(runid=self.entity.runid)
        return result

    def display_distinct_test_categories(self) -> str:
        test_categories = self._get_distinct_test_categories()
        display_str = ", ".join(test_categories)
        return display_str

    def get_if_waveforms(self, test_category=None) -> bool:
        if test_category:
            wfm_count = self.repo.count_waveforms_by_runid(runid=self.entity.runid,
                                                           test_category=test_category)
        else:
            wfm_count = self.repo.count_waveforms_by_runid(runid=self.entity.runid)

        return wfm_count > 0

    def get_testpoint_information_headers(self):
        return ["Channel", "Test Point", "Probe", "Calibration Status", "Probe Range", "Image"]

    def get_testpoint_information(self) -> t.Tuple[t.List, t.List]:
        testpoint_table = []
        testpoints: t.Dict = self.entity.testrun.test_points
        probe_list: t.List[t.Dict] = self.entity.system_info.probes
        for testpoint, probe in zip(testpoints.values(), probe_list):
            testpoint_list = [probe['channel'], testpoint, probe["part_number"], probe["cal_status"],
                              "{range}{units}".format(range=probe["dynamic_range"], units=probe["units"]),
                              "https://cdn.pixabay.com/photo/2018/07/31/22/08/lion-3576045_1280.jpg"]
            testpoint_table.append(testpoint_list)

        return testpoint_table

    def get_runid_image(self) -> str:
        return url_for('static', filename="assets/images/dummy/img-5-lg.jpg")
        # return send_from_directory(r"F:\Output DATABASE", "987_aux2main.png")

    def get_runid_thumbnail(self) -> str:
        # return url_for('static', filename="assets/images/dummy/img-5.jpg")
        return send_from_directory(r"F:\Output DATABASE", "987_aux2main.png")
        # return url_for('', filename="F:\Output DATABASE\987_aux2main.png")
