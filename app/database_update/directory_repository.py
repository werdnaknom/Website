import typing

from .repository import *
from config import DirectoryConfig as DC
from pathlib import Path
import logging
from string import ascii_lowercase
import json
from flask import current_app

from Entities.Entities.error_entity import ErrorEntity
from .error_repository import ErrorHandler

from Entities.WaveformFunctions.waveform_analysis import WaveformAnalysis

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class DirectoryRepository(Repository):

    def __init__(self, error_handler: ErrorHandler, directory: str = DC.DATABASE_NAME):
        self.error_handler = error_handler
        db = Path(directory)
        super().__init__(database=db)
        self.depth = len(self.db.parents)
        logger.info(f"{self.db} at depth {self.depth}")

    def _directory_glob(self, match_pattern: str) -> t.Iterable[Path]:
        return self.db.glob(match_pattern)

    def list_project_paths(self, query: dict = dict) -> t.Iterable[Path]:
        pattern = DC.DIR_FMT_PROJECT.format(project=query.get("product", "*"))
        logger.info(f"Project Searching with glob: {pattern}")
        return self._directory_glob(match_pattern=pattern)

    def list_pba_paths(self, query: dict = dict) -> t.Iterable[Path]:
        pattern = DC.DIR_FMT_PBA.format(project=query.get("product", "*"), pba=query.get("pba", "*"))
        logger.info(f"PBA Searching with glob: {pattern}")
        return self._directory_glob(match_pattern=pattern)

    def list_rework_paths(self, query: dict = dict) -> t.Iterable[Path]:
        pattern = DC.DIR_FMT_REWORK.format(project=query.get("product", "*"), pba=query.get("pba", "*"),
                                           rework=query.get("rework", "*"))
        logger.info(f"Rework Searching with glob: {pattern}")
        return self._directory_glob(match_pattern=pattern)

    def list_serial_number_paths(self, query: dict = dict) -> t.Iterable[Path]:
        pattern = DC.DIR_FMT_SERIAL.format(project=query.get("product", "*"), pba=query.get("pba ", " * "),
                                           rework=query.get("rework", "*"),
                                           serial_number=query.get("serial", "*"))
        logger.info(f"Serial Searching with glob: {pattern}")
        return self._directory_glob(match_pattern=pattern)

    def list_runid_paths(self, query: dict = dict) -> t.Iterable[Path]:
        pattern = DC.DIR_FMT_RUNID.format(project=query.get("product", "*"), pba=query.get("pba", "*"),
                                          rework=query.get("rework", "*"),
                                          serial_number=query.get("serial", "*"),
                                          runid=query.get("runid", "*"))
        logger.info(f"Runid Searching with glob: {pattern}")
        return self._directory_glob(match_pattern=pattern)

    def list_test_paths(self, query: dict = dict) -> t.Iterable[Path]:
        logger.info(f"test paths query: {query}")
        pattern = DC.DIR_FMT_TEST.format(project=query.get("product", "*"), pba=query.get("pba", "*"),
                                         rework=query.get("rework", "*"),
                                         serial_number=query.get("serial", "*"),
                                         runid=query.get("runid", "*"), test=query.get("test", "*"))
        logger.info(f"Automation Tests Searching with glob: {pattern}")
        return self._directory_glob(match_pattern=pattern)

    def list_capture_paths(self, query: dict = dict) -> t.Iterable[Path]:
        logger.info(f"{__name__}: {query}")
        pattern = DC.DIR_FMT_CAPTURE.format(project=query.get("product", "*"), pba=query.get("pba", "*"),
                                            rework=query.get("rework", "*"),
                                            serial_number=query.get("serial", "*"),
                                            runid=query.get("runid", "*"), test=query.get("test", "*"),
                                            capture=query.get("capture", "*"))
        logger.info(f"Capture Paths Searching with glob: {pattern}")
        return self._directory_glob(match_pattern=pattern)

    def list_host_paths(self, query: dict = dict) -> t.Iterable[Path]:
        pattern = DC.DIR_FMT_SCRIPTS_HOST.format(project=query.get("product", "*"),
                                                 pba=query.get("pba", "*"),
                                                 rework=query.get("rework", "*"),
                                                 serial_number=query.get("serial", "*"),
                                                 runid=query.get("runid", "*"), test="Script",
                                                 capture=query.get("capture", "*"),
                                                 host=query.get("host", "*"))
        logger.info(f"Host Paths Searching with glob: {pattern}")
        return self._directory_glob(match_pattern=pattern)

    def _get_parents(self, path: Path) -> t.List[Path]:
        parents = list(path.parents)
        return parents

    def _get_entity_path_from_parents(self, cur_dir: Path, depth: int) -> Path:
        parents = list(cur_dir.parents)
        len_parents = len(parents)
        entity_depth = -(self.depth + 1 + depth)
        entity_path = parents[entity_depth]
        logger.info(f"Entity {entity_path.name}' found from {parents} of length {len_parents}")
        return entity_path

    def _query_error_check(self, iterable):
        return iterable[0]

    def _get_project_from_parents(self, cur_dir: Path) -> str:
        entity = self._get_entity_path_from_parents(cur_dir=cur_dir, depth=DC.PROJECT_DEPTH)
        return entity.name

    def _get_pba_from_parents(self, cur_dir: Path) -> str:
        entity = self._get_entity_path_from_parents(cur_dir=cur_dir, depth=DC.PBA_DEPTH)
        return entity.name

    def _get_rework_from_parents(self, cur_dir: Path) -> int:
        entity = self._get_entity_path_from_parents(cur_dir=cur_dir, depth=DC.REWORK_DEPTH)
        rework = self._convert_dir_name_to_int(dir_name=entity.name)
        return rework

    def _get_serial_from_parents(self, cur_dir: Path) -> str:
        entity = self._get_entity_path_from_parents(cur_dir=cur_dir, depth=DC.SERIAL_DEPTH)
        return entity.name

    def _get_runid_from_parents(self, cur_dir: Path) -> str:
        entity = self._get_entity_path_from_parents(cur_dir=cur_dir, depth=DC.RUNID_DEPTH)
        return entity.name

    def _get_test_from_parents(self, cur_dir: Path) -> str:
        entity = self._get_entity_path_from_parents(cur_dir=cur_dir, depth=DC.TEST_DEPTH)
        return entity.name

    def _get_capture_from_parents(self, cur_dir: Path) -> str:
        entity = self._get_entity_path_from_parents(cur_dir=cur_dir, depth=DC.CAPTURE_DEPTH)
        return entity.name

    def _query_directory_single(self, pattern):
        query = list(self.db.glob(pattern))
        return self._query_error_check(query)

    def _retrieve_project(self, name: str) -> ProjectEntity:
        pattern = DC.DIR_FMT_PROJECT.format(project=name)
        path = self._query_directory_single(pattern)
        return self.from_directory_project(path=path)

    def from_directory_project(self, path: Path) -> ProjectEntity:
        entity = ProjectEntity(name=path.name)
        return entity

    def _retrieve_pba(self, name: str) -> PBAEntity:
        pattern = DC.DIR_FMT_PBA.format(project=name)
        path = self._query_directory_single(pattern)
        return self.from_directory_pba(path=path)

    def from_directory_pba(self, path: Path) -> PBAEntity:
        project = self._get_project_from_parents(cur_dir=path)
        logger.info(f"Creating PBA from {path}")
        entity = PBAEntity(part_number=path.name,
                           project=project)
        logger.info(f"Created {entity}")
        return entity

    def _convert_dir_name_to_int(self, dir_name: str) -> int:
        dir_int = dir_name.lower().strip(ascii_lowercase)
        dir_int = int(dir_int)
        logger.info(f"{dir_name} converted to int {dir_int}")
        return dir_int

    def _retrieve_rework(self, name: str) -> ReworkEntity:
        pattern = DC.DIR_FMT_REWORK.format(project=name)
        path = self._query_directory_single(pattern)
        return self.from_directory_rework(path=path)

    def from_directory_rework(self, path: Path) -> ReworkEntity:
        pba = self._get_pba_from_parents(cur_dir=path)
        rework = self._convert_dir_name_to_int(path.name)
        entity = ReworkEntity(pba=pba,
                              rework=rework)
        return entity

    def _retrieve_serial_number(self, name: str) -> SubmissionEntity:
        pattern = DC.DIR_FMT_SERIAL.format(project=name)
        path = self._query_directory_single(pattern)
        return self.from_directory_serial(path=path)

    def from_directory_serial(self, path: Path) -> SubmissionEntity:
        pba = self._get_pba_from_parents(cur_dir=path)
        rework = self._get_rework_from_parents(cur_dir=path)
        entity = SubmissionEntity(submission=path.name,
                                  rework=rework,
                                  pba=pba)
        return entity

    def _retrieve_runid(self, name: str) -> RunidEntity:
        pattern = DC.DIR_FMT_PROJECT.format(project=name)
        path = self._query_directory_single(pattern)
        return self.from_directory_runid(path=path)

    def _get_runid_location(self, path: Path):
        # TODO::
        return "OR"

    def from_directory_status(self, path: Path) -> StatusFileEntity:
        try:
            with open(path, "r") as file:
                read = file.read()
                jdict = json.loads(read)

            status = jdict["Status"]
            time = jdict["Time"]
            info = jdict["Info"]
            runtime = jdict["Runtime"]

            rhours = runtime["Hours"]
            rmin = runtime["Minutes"]
            rsec = runtime["Seconds"]
            rtotal_sec = runtime["Total Seconds"]

            sfe = StatusFileEntity(status=status, time=time, info=info, runtime_hours=rhours, runtime_minutes=rmin,
                                   runtime_seconds=rsec, runtime_total_seconds=rtotal_sec)
            return sfe
        except Exception as e:
            self.error_handler.write_error(traceback=e,
                                           path=str(path.resolve()),
                                           message=f"Runid Status File Error at {path}")
            return None

    def from_directory_system_info(self, path: Path) -> SystemInfoFileEntity:
        try:
            with open(path, 'r') as file:
                read = file.read()
                jdict = json.loads(read)

            probes_list = jdict["Probes"]
            probe_entities = []
            for probe in probes_list:
                channel = int(probe.get("Channel", "").strip()[-1])
                probe_part_number = probe.get("Type", "").strip()
                serial_number = probe.get("Serial Number", "").strip()
                probe_units = probe.get("Units", "").strip()
                cal_status = probe.get("Cal Status", "").strip()
                degauss = probe.get("Degauss Cycle State", "").strip()
                degauss = degauss == "PASS"
                dynamic_range = probe.get("Dynamic Range", 0)
                probe_entity = ProbesFileEntity(channel=channel, part_number=probe_part_number,
                                                serial_number=serial_number, units=probe_units,
                                                cal_status=cal_status, deguass=degauss, dynamic_range=dynamic_range)
                probe_entities.append(probe_entity)

            scope = jdict["Scope Serial Number"]
            power = jdict["Power Supply Serial Number"]
            ats_ver = jdict.get("ATS Version", "No Version")
            sife = SystemInfoFileEntity(probes=probe_entities, scope_serial_number=scope,
                                        power_supply_serial_number=power,
                                        ats_version=ats_ver)
            return sife
        except Exception as e:
            error_entity = self.error_handler.write_error(traceback=e,
                                                          path=str(path.resolve()),
                                                          message=f"System Info Exception found at {path}")
            return None

    def from_directory_testrun(self, path: Path) -> TestRunFileEntity:
        try:
            with open(path, 'r') as file:
                read = file.read()
                jdict = json.loads(read)

            dut = jdict["DUT"]
            pba = jdict["PBA"]
            rework = jdict["Rework"]
            serial = jdict["Serial Number"]
            tech = jdict["Technician"]
            station = jdict["Test Station"]
            testpoint_list = jdict["Test Points"]
            testpoint_dict = {}
            for index, testpoint in enumerate(testpoint_list):
                testpoint_dict[str(index)] = testpoint
            test_config = jdict.get("Configuration", "")
            board_id = jdict.get("Board ID", -999999)

            trfe = TestRunFileEntity(dut=dut, pba=pba, rework=rework, serial_number=serial, technician=tech,
                                     test_station=station,
                                     configuration=test_config, board_id=board_id,
                                     test_points=testpoint_dict)
            return trfe
        except Exception as e:
            error_entity = self.error_handler.write_error(traceback=e,
                                                          path=str(path.resolve()),
                                                          message=f"Testrun Exception Found at {path}")
            return None

    def from_directory_comments(self, path: Path) -> CommentsFileEntity:
        try:
            with open(path) as file:
                read = file.read()
                cfe = CommentsFileEntity(comments=read)
        except Exception as e:
            self.error_handler.write_error(traceback=e,
                                           path=str(path.resolve()),
                                           message=f"Comment file not found at {path}")
            cfe = CommentsFileEntity(comments="")
        return cfe

    def from_directory_power(self, csv_path: Path, json_path: Path) -> RunidPowerCSVFileEntity:
        try:
            with open(json_path, 'r') as file:
                read = file.read()
                json_headers = json.loads(read)
            column_headers = []
            column_datatypes = []
            for header in json_headers:
                col_header = header["Header"]
                if col_header:
                    column_headers.append(header["Header"])
                    column_datatypes.append(header["Type"])
            csv_df = pd.read_csv(csv_path, sep=",", names=column_headers, index_col=False)
            try:
                ''' CSV DF CLEANUP '''
                for datatype, col_header in zip(column_datatypes, column_headers):
                    if datatype == "timestamp":
                        csv_df[col_header] = pd.to_datetime(csv_df[col_header])
                    elif datatype == "float":
                        csv_df[col_header] = csv_df[col_header].astype(float)
                    elif datatype == "integer":
                        csv_df[col_header] = csv_df[col_header].astype(int)
                    elif datatype == "string":
                        csv_df[col_header] = pd.Categorical(csv_df[col_header])

                max_power = round(csv_df["Total Power"].max(), 2)

                if "DUT Power State" in csv_df.columns:
                    power_states = csv_df.groupby("DUT Power State")["Total Power"].agg(['max', "mean"]).round(
                        3).to_dict(
                        'index')
                else:
                    power_states = {"Power": csv_df["Total Power"].agg(['max', 'mean']).round(3).to_dict()}
            except KeyError as e:
                self.error_handler.write_error(traceback=e,
                                               path=str(csv_path.resolve()),
                                               message=f"{csv_path} failed due to KeyError")
                power_states = {}
                max_power = 0

            rpcfe = RunidPowerCSVFileEntity(dataframe=power_states, max_power=max_power)
            return rpcfe
        except Exception as e:
            self.error_handler.write_error(traceback=e,
                                           path=str(json_path.resolve()),
                                           message=f"Runid Power CSV/JSON not found at {csv_path}/{json_path}")
            return None

    def from_directory_runid(self, path: Path) -> RunidEntity:
        try:
            runid = int(path.name)
            location = self._get_runid_location(path=path)
            project = self._get_project_from_parents(cur_dir=path)
            pba = self._get_pba_from_parents(cur_dir=path)
            rework = self._get_rework_from_parents(cur_dir=path)
            serial = self._get_serial_from_parents(cur_dir=path)
            power = {}
            valid = "Unknown"
            for file in path.iterdir():
                if file.is_file():
                    if DC.COMMENT_FILENAME in file.name:
                        comments = self.from_directory_comments(path=file)
                    elif DC.POWER_CSV_FILENAME in file.name:
                        power[DC.POWER_CSV_FILENAME] = file
                    elif DC.POWER_JSON_FILENAME in file.name:
                        power[DC.POWER_JSON_FILENAME] = file
                    elif "settings.xml" in file.name:
                        pass
                    elif DC.STATUS_JSON_FILENAME in file.name:
                        status = self.from_directory_status(path=file)
                        if status.status == "Aborted":
                            valid = "Invalid"
                    elif "steps.xml" in file.name:
                        pass
                    elif DC.SYSTEMINFO_JSON_FILENAME in file.name:
                        system_info = self.from_directory_system_info(path=file)
                    elif DC.TESTRUN_JSON_FILENAME in file.name:
                        testrun = self.from_directory_testrun(path=file)

            power = self.from_directory_power(json_path=power[DC.POWER_JSON_FILENAME],
                                              csv_path=power[DC.POWER_CSV_FILENAME])
            entity = RunidEntity(runid=runid, location=location, project=project, pba=pba, rework=rework, serial=serial,
                                 status=status,
                                 system_info=system_info,
                                 testrun=testrun,
                                 comments=comments,
                                 power=power,
                                 valid=valid)
            return entity
        except Exception as e:
            self.error_handler.write_error(traceback=e,
                                           path=str(path.resolve()),
                                           message=f"Failed to create Runid Entity at {path}")
            return None

    def _retrieve_test(self, name: str) -> AutomationTestEntity:
        pattern = DC.DIR_FMT_TEST.format(project=name)
        path = self._query_directory_single(pattern)
        return self.from_directory_test(path=path)

    def from_directory_test(self, path: Path) -> AutomationTestEntity:
        name = path.name
        entity = AutomationTestEntity(name=name)
        return entity

    def from_directory_capture_settings(self, path) -> CaptureSettingsEntity:
        capture_json_path = path.joinpath("capture.json")
        try:
            with open(capture_json_path, 'r') as file:
                read = file.read()
                jdict = json.loads(read)

            init_x = jdict["initial x"]
            x_incr = jdict["x increment"]
            compress = jdict['compress']
            names = jdict['names']

            cse = CaptureSettingsEntity(initial_x=init_x, compress=compress, x_increment=x_incr,
                                        waveform_names=names)

            return cse
        except Exception as e:
            self.error_handler.write_error(traceback=e,
                                           path=str(path.resolve()),
                                           message=f"Capture json file not found at {path}")
            return None

    def from_directory_environment_settings(self, path) -> CaptureEnvironmentFileEntity:
        environment_json_path = path.joinpath("temperature power settings.json")
        try:
            with open(environment_json_path, 'r') as file:
                read = file.read()
                jdict = json.loads(read)

            setpoint = jdict['Chamber Setpoint']
            dut_on = jdict["DUT On"]
            channels = jdict['Power Supply Channels']
            psu_channels = {}
            for i, ch in enumerate(channels):
                channel_name = ch["Channel Name"]
                channel_on = ch["Channel On"]
                channel_group = ch["Group"]
                channel_setpoint = ch["Voltage Setpoint"]
                channel_slew = ch["Slew Rate"]
                channel_on_delay = ch["On Delay"]
                channel_off_delay = ch["Off Delay"]
                psc = PowerSupplyChannel(channel=i, channel_name=channel_name, channel_on=channel_on,
                                         group=channel_group,
                                         voltage_setpoint=channel_setpoint, slew_rate=channel_slew,
                                         on_delay=channel_on_delay,
                                         off_delay=channel_off_delay)
                psu_channels[str(psc.channel)] = psc
            efe = CaptureEnvironmentFileEntity(chamber_setpoint=setpoint, dut_on=dut_on,
                                               power_supply_channels=psu_channels)

            return efe
        except Exception as e:
            self.error_handler.write_error(traceback=e,
                                           path=str(environment_json_path.resolve()),
                                           message=f"Environment file not found at {path}")
            return None

    def from_directory_capture_image(self, path: Path) -> PathTranslator:
        capture_image_path = path.joinpath("capture.png")
        capture_path = PathTranslator(path_str=str(capture_image_path.resolve()),
                                      path_name="capture_image")
        return capture_path

    def _from_directory_wavefrom_capture(self, path) -> WaveformCaptureEntity:
        try:
            automation_test = self._get_test_from_parents(cur_dir=path)
            capture = int(path.name)
            runid = self._get_runid_from_parents(cur_dir=path)
            capture_settings = self.from_directory_capture_settings(path=path)
            environment_settings = self.from_directory_environment_settings(path=path)
            capture_image = self.from_directory_capture_image(path=path)
            new_entity = WaveformCaptureEntity(capture=capture, runid=runid, test_category=automation_test,
                                               capture_settings=capture_settings, environment=environment_settings,
                                               capture_image=capture_image)
            return new_entity
        except Exception as e:
            self.error_handler.write_error(traceback=e,
                                           path=str(path.resolve()),
                                           message=f"Waveform Capture failed to create!")
            return None

    def _from_directory_linkpartner_entity(self, path: Path) -> LPTrafficFileEntity:
        lp_file_path = path.joinpath("Link Partner.json")
        try:
            with open(lp_file_path, 'r') as file:
                read = file.read()
                jdict = json.loads(read)

            ports: t.List[Port] = []

            for i, port in enumerate(jdict):
                slot = port["Slot"]
                bdf = slot["Bus Dev Func"]
                connection = slot["Connection"]
                crc = slot["CRC"]
                device_id = slot["Device ID"]
                etrack_id = slot["Etrack ID"]
                link = slot['Link']
                mac = slot['MAC Address']
                name = slot["Name"]
                packet_size = slot["Packet Size"]
                pattern = slot["Pattern"]
                rmac_addr = slot["Remote MAC Address"]
                rev_id = slot["Revision ID"]
                rx_bps = slot["RX Bits Per Second"]
                rx_error = slot["RX Errors"]
                rx_pkt = slot["RX Packets"]
                speed = slot["Speed"]
                state = slot["State"]
                slot_num = slot['Slot']
                sub_id = slot["Subsystem ID"]
                sub_vendor_id = slot["Subsystem Vendor ID"]
                tx_bps = slot["TX Bits Per Second"]
                tx_err = slot["TX Errors"]
                tx_pkt = slot["TX Packets"]
                vendor_id = slot["Vendor ID"]
                p = Port(port=i, bdf=bdf, connection=connection, crc=crc, device_id=device_id, etrack_id=etrack_id,
                         link=link, mac_addr=mac, device_name=name, packet_size=packet_size, pattern=pattern,
                         remote_mac_addr=rmac_addr, rev_id=rev_id, rx_bps=rx_bps, rx_errors=rx_error, rx_packets=rx_pkt,
                         tx_bps=tx_bps, tx_errors=tx_err, tx_packets=tx_pkt, slot=slot_num, speed=speed, state=state,
                         subsystem_id=sub_id, subsystem_vendor_id=sub_vendor_id, vendor_id=vendor_id,
                         target_speed=speed)
                ports.append(p)

            lptfe = LPTrafficFileEntity(ports=ports)
            return lptfe
        except Exception as e:
            self.error_handler.write_error(traceback=e,
                                           path=str(lp_file_path.resolve()),
                                           message=f"Failed to create Link Partner Traffic File at {lp_file_path}")
            return None

    def _from_directory_dut_entity(self, path: Path) -> DUTTrafficFileEntity:
        dut_file_path = path.joinpath("DUT.json")
        try:
            with open(dut_file_path, 'r') as file:
                read = file.read()
                jdict = json.loads(read)

            ports: t.List[Port] = []

            for i, port in enumerate(jdict):
                slot = port["Slot"]
                bdf = slot["Bus Dev Func"]
                connection = slot["Connection"]
                crc = slot["CRC"]
                device_id = slot["Device ID"]
                etrack_id = slot["Etrack ID"]
                link = slot['Link']
                mac = slot['MAC Address']
                name = slot["Name"]
                packet_size = slot["Packet Size"]
                pattern = slot["Pattern"]
                rmac_addr = slot["Remote MAC Address"]
                rev_id = slot["Revision ID"]
                rx_bps = slot["RX Bits Per Second"]
                rx_error = slot["RX Errors"]
                rx_pkt = slot["RX Packets"]
                speed = slot["Speed"]
                state = slot["State"]
                slot_num = slot["Slot"]
                sub_id = slot["Subsystem ID"]
                sub_vendor_id = slot["Subsystem Vendor ID"]
                tx_bps = slot["TX Bits Per Second"]
                tx_err = slot["TX Errors"]
                tx_pkt = slot["TX Packets"]
                vendor_id = slot["Vendor ID"]
                p = Port(port=i, bdf=bdf, connection=connection, crc=crc, device_id=device_id, etrack_id=etrack_id,
                         link=link, mac_addr=mac, device_name=name, packet_size=packet_size, pattern=pattern,
                         remote_mac_addr=rmac_addr, rev_id=rev_id, rx_bps=rx_bps, rx_errors=rx_error, rx_packets=rx_pkt,
                         tx_bps=tx_bps, tx_errors=tx_err, tx_packets=tx_pkt, slot=slot_num, speed=speed, state=state,
                         subsystem_id=sub_id, subsystem_vendor_id=sub_vendor_id, vendor_id=vendor_id,
                         target_speed=speed)
                ports.append(p)

            dtfe = DUTTrafficFileEntity(ports=ports)
            return dtfe
        except Exception as e:
            self.error_handler.write_error(traceback=e,
                                           path=str(dut_file_path.resolve()),
                                           message=f"Failed to create DUT Traffic File at {dut_file_path}")
            return None

    def _from_directory_ethagent_capture(self, path: Path) -> EthAgentCaptureEntity:
        try:
            automation_test = self._get_test_from_parents(cur_dir=path)
            capture = int(path.name)
            runid = self._get_runid_from_parents(cur_dir=path)
            environment_settings = self.from_directory_environment_settings(path=path)
            lp = self._from_directory_linkpartner_entity(path=path)
            dut = self._from_directory_dut_entity(path=path)

            ethagent = EthAgentCaptureEntity(capture=capture, runid=runid, test_category=automation_test,
                                             environment=environment_settings, lp=lp, dut=dut)
            return ethagent
        except Exception as e:
            self.error_handler.write_error(traceback=e,
                                           path=str(path.resolve()),
                                           message=f"EthAgent Capture failed to create!")
            return None

    def from_directory_capture(self, path: Path):  # Capture Entities!
        automation_test = self._get_test_from_parents(cur_dir=path)
        if automation_test == "EthAgent":
            return self._from_directory_ethagent_capture(path=path)
        elif automation_test == "Scripts":
            print("SCRIPTS!!")
        else:
            capture_entity = self._from_directory_wavefrom_capture(path=path)
            return capture_entity

    def _get_waveform_name_from_binary_channel(self, channel: Path, capture_entity: WaveformCaptureEntity) -> str:
        ch_int = int(channel.name[2]) - 1
        file_name = capture_entity.capture_settings.waveform_names
        wf_name = file_name[ch_int]
        return wf_name

    def from_runid_directory_add_waveforms(self, path: Path) -> t.List[WaveformEntity]:
        wfm_list = []
        wfm_analysis = WaveformAnalysis()
        testrun: TestRunFileEntity = self.from_directory_testrun(path.joinpath("testrun.json"))
        system_info: SystemInfoFileEntity = self.from_directory_system_info(path=path.joinpath("System Info.json"))
        for i, glob_binary in enumerate(
                ["CH1.bin", "CH2.bin", "CH3.bin", "CH4.bin", "CH5.bin", "CH6.bin", "CH7.bin", "CH8.bin"]):
            try:
                testpoint = testrun.test_points[str(i)]
                probe_units = system_info.get_probe(i).units
                runid = int(path.name)
                for binary_path in path.rglob(glob_binary):
                    capture_settings = self.from_directory_capture_settings(path=binary_path.parent)
                    compress = False  # capture_settings.compress
                    capture = int(self._get_capture_from_parents(cur_dir=binary_path))
                    test_automation = self._get_test_from_parents(cur_dir=binary_path)
                    wf_y = wfm_analysis.read_binary_waveform(binary_path, compressed=compress)
                    wf_x = wfm_analysis.create_waveform_x_coords(x_increment=capture_settings.x_increment,
                                                                 length=wf_y.size)
                    downsample = wfm_analysis.min_max_downsample_2d(wf_x=wf_x, wf_y=wf_y, size=500)
                    wfm = WaveformEntity(testpoint=testpoint, runid=runid, capture=capture,
                                         test_category=test_automation,
                                         units=probe_units, location=str(binary_path.resolve()),
                                         scope_channel=i + 1,
                                         downsample=downsample)

                    # TODO:: Have the waveform creation task do this itself!
                    target = wfm_analysis.find_cutoff_target_by_percentile(wf=wf_y)
                    ss_wfm = wfm_analysis.find_steady_state_waveform_by_percentile(wf=wf_y)
                    downsample_ss_index = wfm.steady_state_index(expected_voltage=target * 0.9)
                    wfm.steady_state_mean = round(ss_wfm.mean(), 4)
                    wfm.set_steady_state_index(index=downsample_ss_index)
                    wfm.max = round(wf_y.max(), 4)
                    wfm.min = round(wf_y.min(), 4)
                    wfm.steady_state_max = round(ss_wfm.max(), 4)
                    wfm.steady_state_min = round(ss_wfm.min(), 4)
                    wfm.steady_state_pk2pk = round(ss_wfm.ptp(),4)
                    wfm_list.append(wfm)
            except Exception as e:
                self.error_handler.write_error(traceback=e,
                                               path=str(path.resolve()),
                                               message=f"Waveform Entity failed to create!")
        return wfm_list
