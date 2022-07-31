import typing as t

from database_functions.database_functions import DatabaseFunctions
from config import Config
from app.extensions import mongo


class MongoDatabaseFunctions(DatabaseFunctions):

    @staticmethod
    def list_products():
        cursor = mongo.db[Config.PRODUCT].distinct("name")
        r = list(cursor)
        return r

    @staticmethod
    def find_product(product: str) -> t.Dict:
        cursor = mongo.db[Config.PRODUCT].find_one({"name": product})
        return cursor

    @staticmethod
    def find_pbas_by_product(product: str) -> t.List[str]:
        cursor = mongo.db[Config.PBA].distinct("part_number", {"project": product})
        return cursor

    @staticmethod
    def count_pbas_by_product(product: str) -> int:
        pbas = MongoDatabaseFunctions.find_pbas_by_product(product)
        return pbas

    @staticmethod
    def count_captures_by_runid(runid: int, test_category: str = None) -> int:
        search = {"runid": runid}
        if test_category:
            search["test_category"] = test_category
        cursor = mongo.db[Config.CAPTURE].count_documents(search)
        return cursor

    @staticmethod
    def find_pba_entity_by_product(product: str) -> t.List[t.Dict]:
        cursor = mongo.db[Config.PBA].find({"project": product})
        r = list(cursor)
        return r

    @staticmethod
    def find_reworks_by_pba(pba: str) -> t.List[int]:
        cursor = mongo.db[Config.REWORK].find({"pba": pba}, {"_id": 0, "rework": 1})
        r = list(cursor)
        return r

    @staticmethod
    def count_reworks_by_product(product: str) -> t.List[str]:
        count = 0
        pbas = MongoDatabaseFunctions.find_pbas_by_product(product)
        for pba in pbas:
            reworks = MongoDatabaseFunctions.find_reworks_by_pba(pba)
            count += len(reworks)
        return count

    @staticmethod
    def find_rework_entities_by_product(product: str) -> t.List[t.Dict]:
        reworks = []
        pbas = MongoDatabaseFunctions.find_pbas_by_product(product)
        for pba in pbas:
            reworks.extend(MongoDatabaseFunctions.find_rework_entity_by_pba(pba))

        return reworks

    @staticmethod
    def find_rework_entity_by_pba(pba: str) -> t.List[t.Dict]:
        cursor = mongo.db[Config.REWORK].find({"pba": pba})
        r = list(cursor)
        return r

    @staticmethod
    def find_runids_by_product(product: str) -> t.List[str]:
        cursor = mongo.db[Config.RUNID].find({"project": product}, {"_id": 1})
        r = list(cursor)
        return r

    @staticmethod
    def find_runid_by_id(id: str) -> t.List[t.Dict]:
        result = mongo.db[Config.RUNID].find_one({"_id": id})
        return result

    @staticmethod
    def find_runid_entities_by_product(product: str) -> t.List[t.Dict]:
        cursor = mongo.db[Config.RUNID].find({"project": product})
        r = list(cursor)
        return r

    @staticmethod
    def get_runid_test_categories(runid: int):
        cursor = mongo.db[Config.CAPTURE].distinct("test_category", {"runid": runid})
        return cursor

    @staticmethod
    def find_waveform_capture_entities_by_product(product: str) -> t.List[t.Dict]:
        captures = []
        runids = mongo.db[Config.RUNID].distinct("runid", {"project": product})
        for runid in runids:
            cursor = mongo.db[Config.CAPTURE].find({"runid": runid, "test_category": "Aux To Main"})
            r = list(cursor)
            captures.extend(r)
        return captures

    @staticmethod
    def get_runid_temperatures(runid: str):
        pipeline = [
            {"$match": {"runid": runid}},
            {"$project": {
                "_id": 0,
                "environment.chamber_setpoint": 1,
            }},
            {"$group": {
                "_id": None,
                "temperatures": {"$addToSet": "$environment.chamber_setpoint"}
            }}
        ]
        # print(temperature_pipeline)
        results = mongo.db[Config.CAPTURE].aggregate(pipeline)
        return results

    @staticmethod
    def get_runid_voltages_by_channel(runid: str, channel: str):
        pipeline = [
            {"$match": {"runid": runid}},
            {"$project": {
                "_id": channel,
                "environment.power_supply_channels.{}".format(channel): 1,
            }},
            {"$group": {
                "_id": {"channel": "$environment.power_supply_channels.{}.channel_name".format(channel),
                        "group": "$environment.power_supply_channels.{}.group".format(channel),
                        "channel_on": "$environment.power_supply_channels.{}.channel_on".format(channel)
                        },
                "voltages": {"$addToSet": "$environment.power_supply_channels.{}.voltage_setpoint".format(channel)},
                "slew_rates": {"$addToSet": "$environment.power_supply_channels.{}.slew_rate".format(channel)},
            }}
        ]
        results = mongo.db[Config.CAPTURE].aggregate(pipeline)
        return results

    @staticmethod
    def get_runid_capture_data(runid: str):
        temperature_pipeline = [
            {"$match": {"runid": runid}},
            {"$project": {
                "_id": 0,
                "environment.chamber_setpoint": 1,
            }},
            {"$group": {
                "_id": None,
                "temperatures": {"$addToSet": "$environment.chamber_setpoint"}
            }}

        ]
        # print(temperature_pipeline)
        temperature_result = list(mongo.db[Config.CAPTURE].aggregate(temperature_pipeline))[0]
        temperature_list = temperature_result["temperatures"]
        channel_results = []

        for channel in [0, 1, 2, 3]:
            ch_pipeline = [
                {"$match": {"runid": runid}},
                {"$project": {
                    "_id": channel,
                    "environment.power_supply_channels.{}".format(channel): 1,
                }},
                {"$group": {
                    "_id": {"channel": "$environment.power_supply_channels.{}.channel_name".format(channel),
                            "group": "$environment.power_supply_channels.{}.group".format(channel),
                            "channel_on": "$environment.power_supply_channels.{}.channel_on".format(channel)
                            },
                    "voltages": {"$addToSet": "$environment.power_supply_channels.{}.voltage_setpoint".format(channel)},
                    "slew_rates": {"$addToSet": "$environment.power_supply_channels.{}.slew_rate".format(channel)},
                }}
            ]
            # print(ch_pipeline)
            ch_result = mongo.db[Config.CAPTURE].aggregate(ch_pipeline)
            channel_results.extend(list(ch_result))
        return temperature_list, channel_results

    @staticmethod
    def get_runid_capture_waveforms(runid: str, temperatures: t.List[int], voltages, test_category: str):
        captures = mongo.db[Config.CAPTURE].find({"runid": runid})
        '''
        print(captures)
        for capture in captures:
            print(capture["_id"])
        '''
        return captures

    @staticmethod
    def get_waveforms_by_runid(runid: int):
        print("RUNID: ", runid)
        waveforms = mongo.db[Config.WAVEFORM].find({"runid": runid}, {'downsample': 1, "_id": 0})
        return waveforms

    @staticmethod
    def get_waveforms_by_captures(runid: int, capture_list: t.List[int]):
        waveforms = mongo.db[Config.WAVEFORM].find({"runid": runid, "capture": {"$in": capture_list}},
                                                   {"downsample": 1, "_id": 0})
        return waveforms

    @staticmethod
    def get_waveforms_for_aux_to_main_graph(runid: int, temperatures: t.List[int], voltages: t.Dict,
                                            scope_channels: t.List[int]) -> t.List:
        CAPTURE_LIST = "captures"
        match_dict = {
            "runid": runid,
            "environment.chamber_setpoint": {"$in": temperatures},
        }
        for ch, voltage_list in voltages.items():
            if voltage_list:
                key_str = f"environment.power_supply_channels.{ch}.voltage_setpoint".format(ch)
                search_str = {"$in": voltage_list}
                match_dict[key_str] = search_str
        capture_pipeline = [
            {"$match": match_dict},
            {"$group":
                 {"_id": {"runids": "$runid"},
                  CAPTURE_LIST: {"$addToSet": "$capture"}}
             }]
        # print(capture_pipeline)
        captures_cursor = mongo.db[Config.CAPTURE].aggregate(capture_pipeline)
        captures = list(captures_cursor)[0][CAPTURE_LIST]

        waveforms = MongoDatabaseFunctions.get_waveforms_by_captures(runid=runid, capture_list=captures)

        return waveforms

    @staticmethod
    def get_runid_capture_image_and_information(runid: str, capture: int):
        # TODO:: Not finished
        runid = int(runid[3:])
        capture = list(mongo.db[Config.CAPTURE].find({"runid": runid, "capture": capture},
                                                     {"waveform_names": 1, "environment": 1, "capture_image": 1, }))
        return capture

    @staticmethod
    def get_runid_images_for_grid(runid: str):
        runid = int(runid[3:])
        pipeline = [
            {"$match": {"runid": runid}},
            {"$group": {"_id": {"test": "$test_category"},
                        # "images": {"$addToSet": "$capture_image.path_str"},
                        "all": {"$push": {
                            "capture_id": "$_id",
                            "image": "$capture_image.path_str",
                            "environment": "$environment"
                        }}}},
        ]
        result = mongo.db[Config.CAPTURE].aggregate(pipeline)
        return list(result)
