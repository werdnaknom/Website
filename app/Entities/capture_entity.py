from app.Entities.entity import Entity, CAPTURE
from app.Entities.waveform_entity import Waveform
from app.Entities.domain_model import DomainModel

from config import CAPTUREFILTERS, CAPTUREOPERATORS

'''
CAPTURE.JSON
{   
    "initial x":                        7.1515000000361116095e-08,
    "x increment":                      8.0000000000000001674e-08, 
    "names":                    [       "PCIE 12V Main",
                                        "PCIE 3.3V Main",
                                        "PCIE 3.3V Aux",
                                        "PCIE 3.3V Current"
                                ],
    "compress":                         true,
    "meta":                     "{      Temperature Setpoint\":25,
                                        Temperature\":24.900000000000002132,
                                        Power Supply\":     [{\"Name\":\"PCIE-12 Main\",
                                                            \"Group\":\"Main\",
                                                            \"PS Channel\":1,
                                                            \"Slew\":200,
                                                            \"Voltage\":11.001459999999999795,
                                                            \"Current\":7.2441279999999999063e-05,
                                                            \"On Delay\":0,
                                                            \"Off Delay\":0,
                                                            \"On\":true,
                                                            \"Voltage Setpoint\":11},
                                                            {\"Name\":\"PCIE 3.3 Main\",
                                                            \"Group\":\"Main\",
                                                            \"PS Channel\":2,
                                                            \"Slew\":200,
                                                            \"Voltage\":3.000176000000000176,
                                                            \"Current\":9.8932870000000000662e-06,
                                                            \"On Delay\":0.020000000000000000416,
                                                            \"Off Delay\":0,
                                                            \"On\":true,
                                                            \"Voltage Setpoint\":3},
                                                            {\"Name\":\"\",\"Group\":\"Disabled\",
                                                            \"PS Channel\":3,
                                                            \"Slew\":1000,
                                                            \"SVoltage\":0.00044267280000000002165,
                                                            \"Current\":-6.2004040000000000717e-06,
                                                            \"On Delay\":0,
                                                            \"Off Delay\":0,
                                                            \"On\":false,
                                                            \"Voltage Setpoint\":3},
                                                            {\"Name\":\"PCIE 3.3 Aux\",
                                                            \"Group\":\"Main\",
                                                            \"PS Channel\":4,
                                                            \"Slew\":200,
                                                            \"Voltage\":3.0016690000000001426,
                                                            \"Current\":1.667176999999999909,
                                                            \"On Delay\":0,
                                                            \"Off Delay\":0,
                                                            \"On\":true,
                                                            \"Voltage Setpoint\":3
                                                            }]
                                        }"
}

'''


class Capture(Entity):
    def __init__(self, capture, waveforms=[], images=[]):
        super(Capture, self).__init__(descriptor=capture,
                                      next_list=waveforms,
                                      next_entity=Waveform,
                                      filters_list=CAPTUREFILTERS,
                                      operators_list=CAPTUREOPERATORS)
        self.images = images
        self.json_descriptors = {}
        self._type = CAPTURE

    @classmethod
    def _from_dict(cls, adict):
        sc = Capture(capture=adict['capture'],
                     waveforms=[Waveform._from_dict(wf) for wf in adict.get('waveforms', [])],
                     images=adict.get('images', []))
        desc = adict.get("json_descriptors", {})
        for key, value in desc.items():
            sc.add_json_descriptor(name=key, json_dict=value)
        return sc

    def _to_dict(self):
        to_dict = self._to_dataframe_json()
        to_dict['json_descriptors'] = self.json_descriptors
        to_dict['waveforms'] = [wf.to_dict() for wf in self.get_next()]
        return to_dict

    def _to_dataframe_json(self):
        return {'capture': self.descriptor,
                'images': self.images}

    @property
    def capture(self):
        return self.descriptor

    @property
    def initial_x(self):
        value = self.get_json_field(json_name="capture", field="initial x", expected_type="")
        return value

    @property
    def x_increment(self):
        value = self.get_json_field(json_name="capture", field="x increment", expected_type="")
        return value

    @property
    def waveform_names(self):
        value = self.get_json_field(json_name="capture", field="names", expected_type=[])
        return value

    @property
    def compress(self):
        value = self.get_json_field(json_name="capture", field="compress", expected_type="")
        if value == "true":
            value = True
        else:
            value = False
        return value

    def _get_temperatures(self):
        return [self.temperature_setpoint]

    @property
    def temperature(self):
        return self.temperature_setpoint

    @property
    def temp(self):
        return self.temperature_setpoint

    @property
    def temperature_setpoint(self):
        value = self.get_json_field(json_name="temperature_power_settings", field="Chamber Setpoint",
                                    expected_type=None)
        return value

    @property
    def power_supply(self):
        value = self.get_json_field(json_name="temperature_power_settings", field="Power Supply Channels",
                                    expected_type=[])
        return value

    def get_power_ch(self, channel):
        power_list = self.power_supply
        assert channel <= len(power_list), '"{}" is out of bounds for power channel list: "{}".'.format(channel,
                                                                                                        power_list)
        return power_list[channel - 1]

    def power_channel_field(self, channel, field, empty_result=""):
        power_ch_dict = self.get_power_ch(channel=channel)
        value = power_ch_dict.get(field, empty_result)
        return value

    @property
    def power_1_name(self):
        return self.power_channel_field(channel=1, field="Channel Name")

    @property
    def power_1_group(self):
        return self.power_channel_field(channel=1, field="Group")

    @property
    def power_1_channel(self):
        return self.power_channel_field(channel=1, field="PS Channel")

    @property
    def power_1_slew(self):
        return self.power_channel_field(channel=1, field="Slew Rate", empty_result=0)

    @property
    def power_1_voltage(self):
        return self.power_channel_field(channel=1, field="Voltage Setpoint", empty_result=0)

    @property
    def power_1_current(self):
        return self.power_channel_field(channel=1, field="Current", empty_result=0)

    @property
    def power_1_on_delay(self):
        return self.power_channel_field(channel=1, field="On Delay", empty_result=0)

    @property
    def power_1_off_delay(self):
        return self.power_channel_field(channel=1, field="Off Delay", empty_result=0)

    @property
    def power_1_voltage_setpoint(self):
        return self.power_channel_field(channel=1, field="Voltage Setpoint", empty_result=0)

    @property
    def power_2_name(self):
        return self.power_channel_field(channel=2, field="Channel Name")

    @property
    def power_2_group(self):
        return self.power_channel_field(channel=2, field="Group")

    @property
    def power_2_channel(self):
        return self.power_channel_field(channel=2, field="PS Channel")

    @property
    def power_2_slew(self):
        return self.power_channel_field(channel=2, field="Slew Rate")

    @property
    def power_2_voltage(self):
        return self.power_channel_field(channel=2, field="Voltage Setpoint", empty_result=0)

    @property
    def power_2_current(self):
        return self.power_channel_field(channel=2, field="Current", empty_result=0)

    @property
    def power_2_on_delay(self):
        return self.power_channel_field(channel=2, field="On Delay", empty_result=0)

    @property
    def power_2_off_delay(self):
        return self.power_channel_field(channel=2, field="Off Delay", empty_result=0)

    @property
    def power_2_voltage_setpoint(self):
        return self.power_channel_field(channel=2, field="Voltage Setpoint", empty_result=0)

    @property
    def power_3_name(self):
        return self.power_channel_field(channel=3, field="Channel Name")

    @property
    def power_3_group(self):
        return self.power_channel_field(channel=3, field="Group")

    @property
    def power_3_channel(self):
        return self.power_channel_field(channel=3, field="PS Channel")

    @property
    def power_3_slew(self):
        return self.power_channel_field(channel=3, field="Slew Rate")

    @property
    def power_3_voltage(self):
        return self.power_channel_field(channel=3, field="Voltage Setpoint", empty_result=0)

    @property
    def power_3_current(self):
        return self.power_channel_field(channel=3, field="Current", empty_result=0)

    @property
    def power_3_on_delay(self):
        return self.power_channel_field(channel=3, field="On Delay", empty_result=0)

    @property
    def power_3_off_delay(self):
        return self.power_channel_field(channel=3, field="Off Delay", empty_result=0)

    @property
    def power_3_voltage_setpoint(self):
        return self.power_channel_field(channel=3, field="Voltage Setpoint", empty_result=0)

    @property
    def power_4_name(self):
        return self.power_channel_field(channel=4, field="Channel Name")

    @property
    def power_4_group(self):
        return self.power_channel_field(channel=4, field="Group")

    @property
    def power_4_channel(self):
        return self.power_channel_field(channel=4, field="PS Channel")

    @property
    def power_4_slew(self):
        return self.power_channel_field(channel=4, field="Slew Rate")

    @property
    def power_4_voltage(self):
        return self.power_channel_field(channel=4, field="Voltage Setpoint", empty_result=0)

    @property
    def power_4_current(self):
        return self.power_channel_field(channel=4, field="Current", empty_result=0)

    @property
    def power_4_on_delay(self):
        return self.power_channel_field(channel=4, field="On Delay", empty_result=0)

    @property
    def power_4_off_delay(self):
        return self.power_channel_field(channel=4, field="Off Delay", empty_result=0)

    @property
    def power_4_voltage_setpoint(self):
        return self.power_channel_field(channel=4, field="Voltage Setpoint", empty_result=0)

    '''
    def get_columns(self):
        fmt = "{filename}_{column_name}"
        columns = ["capture", 'image']
        for file_name, d in self.json_descriptors.items():
            file_name = file_name + '_json'
            for key, v in d.items():
                if key not in IGNORED_COLUMNS:
                    header = fmt.format(filename=file_name, column_name=key).lower().replace(" ", "_")
                    columns.extend(self._get_json_columns(header=header, value=v))
        #print(columns)
        return columns

    def get_data(self):
        data = [self.descriptor, self.images]
        for file_name, d in self.json_descriptors.items():
            for key, v in d.items():
                if key not in IGNORED_COLUMNS:
                    data.extend(self._get_json_data(header=file_name, value=v))
        return data
    '''

    def get_channel_nominal_power(self, channel):
        voltage_attr = "power_{}_voltage".format(channel)
        current_attr = "power_{}_current".format(channel)
        voltage = getattr(self, voltage_attr)
        current = getattr(self, current_attr)
        power = voltage * current
        return power

    @property
    def nominal_power(self):
        power_len = len(self.power_supply)
        power = sum([self.get_channel_nominal_power(channel=ch) for ch in range(1, power_len + 1)])
        return power

    def get_number_of_voltage_channels(self):
        return len(self.power_supply)

    def channel_name_group_voltages(self, channel):
        return {"Name": getattr(self, "power_{}_name".format(channel)),
                "Group": getattr(self, "power_{}_group".format(channel)),
                "Voltage": getattr(self, "power_{}_voltage".format(channel))
                }

    def _get_voltage_rails_and_values(self):
        capture_channels = {}
        for ps_channel in range(1, self.get_number_of_voltage_channels() + 1):
            channel = self.channel_name_group_voltages(ps_channel)
            if channel['Group'] != "Disabled":
                name = channel['Name']
                voltage = channel['Voltage']
                capture_channels[name] = [voltage]
        return capture_channels

    @property
    def ports(self):
        dut = [key.replace("dut_", "") for key in self.json_descriptors.keys() if key.startswith("dut")]

        # TODO:: CHECK IF DUT and LP Are equal!
        # lp = [key.replace("link_partner_","") for key in self.json_descriptors.keys() if key.startswith("link_partner")]
        # assert dut == lp
        return dut

    @property
    def num_ports(self):
        dut = len([key for key in self.json_descriptors.keys() if key.startswith("dut")])

        # TODO:: CHECK IF DUT and LP Are equal!
        # lp = len([key for key in self.json_descriptors.keys() if key.startswith("link_partner")])
        # assert dut == lp
        return dut


DomainModel.register(Capture)
