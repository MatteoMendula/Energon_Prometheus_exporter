import time
from energon_prometheus_exporter.drivers import utils
from energon_prometheus_exporter.drivers import constants
from energon_prometheus_exporter.models.general_model import GeneralModel

# General Ubuntu x64 architecture Model 
# author: @MatteoMendula
# date: 2023-04-22

class Ubuntu64(GeneralModel):
    def __init__(self):
        super().__init__()

    def set_energy_metrics(self):
        in_psys_power_first = utils.run_command_and_get_output("cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl:1/energy_uj")     # micro Joules
        in_cpu_power_first = utils.run_command_and_get_output("cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/energy_uj")      # micro Joules             
        
        time.sleep(1)

        in_psys_power_second = utils.run_command_and_get_output("cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl:1/energy_uj")    # micro Joules
        in_cpu_power_second = utils.run_command_and_get_output("cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/energy_uj")     # micro Joules
        
        in_gpu_power = utils.run_command_and_get_output("nvidia-smi --query-gpu=power.draw --format=csv,noheader")                  # Watts (e.g. 19.67 W)
        
        if in_psys_power_first["error"] or in_cpu_power_first["error"] or in_psys_power_second["error"] or in_cpu_power_second["error"]:
            in_psys_power = float("nan")
            in_cpu_power = float("nan")
        else:
            in_psys_power = utils.parse_micro_joules_string_watts_float(in_psys_power_second["out_value"]) - utils.parse_micro_joules_string_watts_float(in_psys_power_first["out_value"])
            in_cpu_power = utils.parse_micro_joules_string_watts_float(in_cpu_power_second["out_value"]) - utils.parse_micro_joules_string_watts_float(in_cpu_power_first["out_value"])
        
        in_gpu_power = float("nan") if in_gpu_power["error"] else utils.parseToFloat(in_gpu_power["out_value"])

        self.energy_metrics = {}
        self.energy_metrics["_keys"] = ["total_power", "gpu_power", "cpu_power", "total_voltage", "cpu_voltage", "gpu_voltage"]

        self.energy_metrics["total_power"] = in_psys_power + in_gpu_power + in_cpu_power
        self.energy_metrics["cpu_power"] = in_cpu_power
        self.energy_metrics["gpu_power"] = in_gpu_power

        self.energy_metrics["total_voltage"] = float("nan")
        self.energy_metrics["cpu_voltage"] = float("nan")
        self.energy_metrics["gpu_voltage"] = float("nan")

    def set_cpu_frequency(self):
        cores_frequency = utils.run_command_and_grep_output("cat /proc/cpuinfo","^[c]pu MHz")
        if cores_frequency["error"] == True:
            return

        cores = cores_frequency["out_value"].split("\\n")
        self.cpu_frequency_metrics = {}
        self.cpu_frequency_metrics["_keys"] = []
        for index, core in enumerate(cores):
            if len(core) == 0:
                continue
            self.cpu_frequency_metrics["_keys"].append("core_{}".format(index))
            self.cpu_frequency_metrics["core_{}".format(index)] = utils.parseToFloat(core.split(":")[1])

    def set_battery_percentage(self):
        battery_percentage = utils.run_command_and_get_output("cat /sys/class/power_supply/BAT0/capacity")
        self.battery_percentage = constants.ERROR_WHILE_READING_VALUE if battery_percentage["error"] else utils.parseToFloat(battery_percentage["out_value"])

    def set_gpu_usage_percentage(self):

        gpu_load_command = "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader"
        _gpu_command_output = utils.run_command_and_get_output(gpu_load_command)
        if _gpu_command_output["error"] == True or len(_gpu_command_output["out_value"]) == 0:
            self.gpu_usage_percentage = constants.ERROR_WHILE_READING_VALUE
            return 
        
        # The GPU load is stored as a percentage 
        self.gpu_usage_percentage = utils.parseToFloat(_gpu_command_output["out_value"])

    def set_temperature_metrics(self):
        thermal_zones = utils.run_command_and_grep_output("ls /sys/class/thermal/", "thermal_zone")
        if thermal_zones["error"] == True:
            self.temperature_metrics = constants.ERROR_WHILE_READING_VALUE
            return

        self.temperature_metrics = {}
        self.temperature_metrics["_keys"] = []
        for zone in thermal_zones["out_value"].split("\\n"):
            if len(zone) == 0:
                continue
            self.temperature_metrics["_keys"].append(zone)
            temp = utils.run_command_and_get_output("cat /sys/class/thermal/" + zone + "/temp")
            if temp["error"] == True or len(temp["out_value"]) == 0:
                self.temperature_metrics["error"] = True
                self.temperature_metrics[zone] = constants.ERROR_WHILE_READING_VALUE
                continue
            self.temperature_metrics[zone] = temp["out_value"]
            
            print("Temperature: " + str(self.temperature_metrics[zone]))
            print("Temperature length: ", len(str(self.temperature_metrics[zone])))