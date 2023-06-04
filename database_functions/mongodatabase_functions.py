import typing as t

from database_functions.database_functions import DatabaseFunctions
from config import Config
from app.extensions import mongo
from Entities.Entities import TestpointEntity


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
    def find_runid_by_id(id: str) -> t.Dict:
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
        temperature_result = list(mongo.db[Config.CAPTURE].aggregate(temperature_pipeline))
        if len(temperature_result) == 0:
            temperature_list = []
        else:
            temperature_result = temperature_result[0]
            temperature_list = temperature_result["temperatures"]
        channel_results = []

        for channel_number in [0, 1, 2, 3]:
            ch_pipeline = [
                {"$match": {"runid": runid}},
                {"$project": {
                    "_id": channel_number,
                    "environment.power_supply_channels.{}".format(channel_number): 1,
                }},
                {"$group": {
                    "_id": {
                        "channel": "$environment.power_supply_channels.{}.channel_name".format(channel_number),
                        "group": "$environment.power_supply_channels.{}.group".format(channel_number),
                        "channel_on": "$environment.power_supply_channels.{}.channel_on".format(channel_number)
                    },
                    "voltages": {
                        "$addToSet": "$environment.power_supply_channels.{}.voltage_setpoint".format(channel_number)},
                    "slew_rates": {
                        "$addToSet": "$environment.power_supply_channels.{}.slew_rate".format(channel_number)},
                }}
            ]
            # print(ch_pipeline)
            ch_result = mongo.db[Config.CAPTURE].aggregate(ch_pipeline)
            for channel in ch_result:
                channel["_id"]["channel_number"] = channel_number
                channel_results.append(channel)
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
        # print("RUNID: ", runid)
        waveforms = mongo.db[Config.WAVEFORM].find({"runid": runid}, {'downsample': 1, "_id": 0})
        return waveforms

    @staticmethod
    def get_waveforms_by_captures(runid: int, capture_list: t.List[int], test_category: str):
        find_query = {
            "runid": runid,
            "capture": {"$in": capture_list},
            "test_category": test_category
        }
        waveforms = mongo.db[Config.WAVEFORM].find(find_query,
                                                   {"downsample": 1, "_id": 0, "testpoint": 1})
        return waveforms

    @staticmethod
    def get_waveforms_for_aux_to_main_graph(test_category: str, runid: int, temperatures: t.List[int], voltages: t.Dict,
                                            scope_channels: t.List[int]) -> t.List:
        CAPTURE_LIST = "captures"
        match_dict = {
            "runid": runid,
            "environment.chamber_setpoint": {"$in": temperatures},
        }
        for ch, voltage_list in voltages.items():
            if voltage_list:
                if type(voltage_list) != list:
                    voltage_list = [voltage_list]
                # print(voltage_list)
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
        waveforms = []
        for capture in captures_cursor:
            captures = capture[CAPTURE_LIST]
            capture_waveforms = MongoDatabaseFunctions.get_waveforms_by_captures(runid=runid, capture_list=captures,
                                                                                 test_category=test_category)
            waveforms.extend(capture_waveforms)

        return waveforms

    @staticmethod
    def get_one_runid(runid_id):
        cursor = mongo.db[Config.RUNID].find_one({"_id": runid_id})
        return cursor

    @staticmethod
    def get_runid_capture_image_and_information(runid: str, capture: int):
        # TODO:: Not finished
        runid = int(runid[3:])
        capture = list(mongo.db[Config.CAPTURE].find({"runid": runid, "capture": capture},
                                                     {"waveform_names": 1, "environment": 1, "capture_image": 1, }))
        return capture

    @staticmethod
    def get_runid_images_for_grid(runid: str):
        # TODO:: Make it so runids aren't ints
        runid = int(runid[3:])
        pipeline = [
            {"$match": {"runid": runid}},
            {"$group": {"_id": {"test": "$test_category"},
                        # "images": {"$addToSet": "$capture_image.path_str"},
                        "all": {"$push": {
                            "capture_id": "$_id",
                            "capture": "$capture",
                            "image": "$capture_image.path_str",
                            "environment": "$environment"
                        }}}},
            {"$sort": {"test.all.capture_id": 1}}
        ]
        # TODO:: The sort doesn't work!
        result = mongo.db[Config.CAPTURE].aggregate(pipeline)
        return list(result)

    @staticmethod
    def get_waveform_names_by_product(product: str, runid: str = None) -> t.List[str]:
        # TODO:: THIS HASN'T BEEN VERIFIED AT ALL
        pipeline = [
            {"$match": {"project": product}},
            {"$lookup": {
                "from": Config.WAVEFORM,
                # "localField": "runid",
                # "foreignField": "runid",
                "let": {"id": "$runid"},
                "as": "waveforms",
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$runid", "$$id"]}}},
                    {"$project": {"testpoint": 1, "_id": 0}}
                ],
            }},
            {"$project": {"waveforms": 1, "runid": 1, "_id": 0}}

        ]
        cursor = mongo.db[Config.RUNID].aggregate(pipeline)
        testpoint_set = set()
        for runid_dict in cursor:
            # print(runid_dict)
            testpoints = runid_dict["_id"]["waveforms"]
            # testpoints.add(runid_dict["_id"]["waveforms"])
            # print(testpoint_set.update(testpoints))
        result = list(testpoint_set)
        result.sort()
        return result

    @staticmethod
    def get_runid_waveform_names_by_product(product: str, runid: str = None) -> t.List[str]:
        pipeline = [
            {"$match": {"project": product}},
            # {"$group": {"_id": "$testrun.testpoints"}},
            # {"$addFields": {"waveforms": {"$objectToArray": "$testrun.test_points"}}},
            {"$addFields": {"waveforms": {"$objectToArray": "$testrun.test_points"}}},
            {"$project": {"waveforms": 1, "runid": 1, "_id": 0}},
            # {"$unwind": "$waveforms"}
            {"$group": {
                "_id": {"waveforms": "$waveforms.v"},
            }}

        ]
        cursor = mongo.db[Config.RUNID].aggregate(pipeline)
        testpoint_set = set()
        for runid_dict in cursor:
            testpoints = runid_dict["_id"]["waveforms"]
            # testpoints.add(runid_dict["_id"]["waveforms"])
            testpoint_set.update(testpoints)

        result = list(testpoint_set)
        result.sort()

        return result

    @staticmethod
    def get_testpoints_by_product(product: str):
        # Returns cursor with dicts
        return list(mongo.db[Config.TESTPOINT].find({"product": product}))

    @staticmethod
    def upsert_testpoint_metrics(product: str, testpoint: str, edge_rail: bool, nominal_value: float,
                                 min_value: float, max_value: float, bandwidth_mhz: float, poweron_time_ms: float,
                                 valid_voltage: float, current_rail: bool, associated_rail: str, poweron_order: int):
        tpe = TestpointEntity(product=product,
                              testpoint=testpoint,
                              edge_rail=edge_rail,
                              current_rail=current_rail,
                              associated_rail=associated_rail,
                              nominal_value=nominal_value,
                              min_value=min_value,
                              max_value=max_value,
                              bandwidth_mhz=bandwidth_mhz,
                              valid_value=valid_voltage,
                              poweron_time_ms=poweron_time_ms,
                              poweron_order=poweron_order
                              )
        # Define the filter to find the testpoint if it exists
        tpe_filter = {"_id": tpe.get_id()}

        # define the new testpoint to replace the existing one
        new_testpoint = tpe.to_mongo()
        print(new_testpoint)

        cursor = mongo.db[Config.TESTPOINT].replace_one(tpe_filter, new_testpoint, upsert=True)
        '''
        print('Matched Count:', cursor.matched_count)
        print('Modified Count:', cursor.modified_count)
        print('Upserted ID:', cursor.upserted_id)
        '''

    @staticmethod
    def get_testpoints_for_product_by_runid(product, testpoint) -> t.List:
        pipeline = [
            {"$match": {"project": product}},
            {"$lookup": {
                "from": Config.WAVEFORM,
                # "localField": "runid",
                # "foreignField": "runid",
                "let": {"id": "$runid"},
                "as": "tests",
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$runid", "$$id"]},
                                "testpoint": testpoint}},
                    {"$project": {"_id": 1, "test_category": 1}},
                    {"$group": {"_id": {"test_category": "$test_category"},
                                "waveforms": {"$push": {"_id": "$_id"}}}},
                ],
            }},
            {"$project": {"tests": 1, "runid": 1, "_id": 0}}
        ]
        cursor = mongo.db[Config.RUNID].aggregate(pipeline)
        return cursor

    @staticmethod
    def update_runid_validity(runid_id, validity):
        query = {"_id": runid_id}
        new_valid = {"$set": {"valid": validity}}
        updated_runid = mongo.db[Config.RUNID].update_one(query, new_valid)
        return updated_runid


'''
    @staticmethod
    def get_testpoint_by_product(testpont: str, product: str):
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
'''
