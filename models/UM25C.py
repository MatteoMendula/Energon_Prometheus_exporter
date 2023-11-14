import utils
import time
import constants

from models.general_model import GeneralModel

# General UM25C bluetooth meter 
# author: @MatteoMendula
# date: 2023-12-11

class UM25C(GeneralModel):
    def __init__(self, actual_meter):
        super().__init__()
        self.actual_meter = actual_meter

    def set_energy_metrics(self):

        query_result = self.actual_meter.query()

        self.energy_metrics = {}
        self.energy_metrics["_keys"] = ["total_power", "gpu_power", "cpu_power", "total_voltage", "cpu_voltage", "gpu_voltage"]

        self.energy_metrics["total_power"] = query_result["Watts"] * 1000 # convert to mW
        self.energy_metrics["cpu_power"] = float("nan")
        self.energy_metrics["gpu_power"] = float("nan")

        self.energy_metrics["total_voltage"] = query_result["Volts"] * 1000 # convert to mV
        self.energy_metrics["cpu_voltage"] = float("nan")
        self.energy_metrics["gpu_voltage"] = float("nan")

    def set_cpu_frequency(self):
        self.cpu_frequency_metrics = {}
        self.cpu_frequency_metrics["_keys"] = []

    def set_battery_percentage(self):
        self.battery_percentage = float("nan")

    def set_gpu_usage_percentage(self):
        self.gpu_usage_percentage = float("nan")

    def set_temperature_metrics(self):
        self.temperature_metrics = {}
        self.temperature_metrics["_keys"] = []
        