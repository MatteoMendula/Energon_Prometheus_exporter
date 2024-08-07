from energon_prometheus_exporter.drivers import utils
from energon_prometheus_exporter.drivers import constants
from energon_prometheus_exporter.models.general_model import GeneralModel

# Jetson Nano Dev Kit Model 
# author: @MatteoMendula
# date: 2023-04-29

class JetsonOrinNano(GeneralModel):
    def __init__(self):
        super().__init__()
        self.detected_model = constants.JETSON_ORIN_NANO

    def set_energy_metrics(self):
        in_tot_power = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon0/curr1_input")
        in_cpu_gpu_power = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon0/curr2_input")
        in_soc_power = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon0/curr3_input")
        
        in_tot_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon0/in1_input")
        in_cpu_gpu_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon0/in2_input")
        in_soc_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon0/in3_input")

        self.energy_metrics = {}
        self.energy_metrics["_keys"] = ["total_power", "gpu_power", "cpu_power", "cpu_gpu_power", "soc_power", "total_voltage", "gpu_voltage", "cpu_voltage", "cpu_gpu_voltage", "soc_voltage"]

        self.energy_metrics["total_power"] = constants.ERROR_WHILE_READING_VALUE if in_tot_power["error"] else utils.parseToFloat(in_tot_power["out_value"])
        self.energy_metrics["cpu_gpu_power"] = constants.ERROR_WHILE_READING_VALUE if in_cpu_gpu_power["error"] else utils.parseToFloat(in_cpu_gpu_power["out_value"])
        self.energy_metrics["soc_power"] = constants.ERROR_WHILE_READING_VALUE if in_soc_power["error"] else utils.parseToFloat(in_soc_power["out_value"])
        self.energy_metrics["gpu_power"] = -1
        self.energy_metrics["cpu_power"] =  -1

        self.energy_metrics["total_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_tot_voltage["error"] else utils.parseToFloat(in_tot_voltage["out_value"])
        self.energy_metrics["cpu_gpu_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_cpu_gpu_voltage["error"] else utils.parseToFloat(in_cpu_gpu_voltage["out_value"])
        self.energy_metrics["soc_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_soc_voltage["error"] else utils.parseToFloat(in_soc_voltage["out_value"])
        self.energy_metrics["gpu_voltage"] = -1
        self.energy_metrics["cpu_voltage"] =  -1
                  
    def set_cpu_frequency(self):
        core_0 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq")
        core_1 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu1/cpufreq/cpuinfo_cur_freq")
        core_2 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_cur_freq")
        core_3 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_cur_freq")
        core_4 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu4/cpufreq/cpuinfo_cur_freq")
        core_5 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu5/cpufreq/cpuinfo_cur_freq")
        
        self.cpu_frequency_metrics = {}
        self.cpu_frequency_metrics["_keys"] = ["core_0", "core_1", "core_2", "core_3", "core_4", "core_5"]
        
        self.cpu_frequency_metrics["core_0"] = constants.ERROR_WHILE_READING_VALUE if core_0["error"] else utils.parseToFloat(core_0["out_value"])
        self.cpu_frequency_metrics["core_1"] = constants.ERROR_WHILE_READING_VALUE if core_1["error"] else utils.parseToFloat(core_1["out_value"])
        self.cpu_frequency_metrics["core_2"] = constants.ERROR_WHILE_READING_VALUE if core_2["error"] else utils.parseToFloat(core_2["out_value"])
        self.cpu_frequency_metrics["core_3"] = constants.ERROR_WHILE_READING_VALUE if core_3["error"] else utils.parseToFloat(core_3["out_value"])
        self.cpu_frequency_metrics["core_4"] = constants.ERROR_WHILE_READING_VALUE if core_4["error"] else utils.parseToFloat(core_4["out_value"])
        self.cpu_frequency_metrics["core_5"] = constants.ERROR_WHILE_READING_VALUE if core_5["error"] else utils.parseToFloat(core_5["out_value"])

    def set_gpu_usage_percentage(self):

        gpu_load_possible_commands = [ "cat /sys/devices/platform/17000000.gpu/load" ]
        _gpu_command_output = None

        for command in gpu_load_possible_commands:
            _gpu_command_output = utils.run_command_and_get_output(command)
            if _gpu_command_output["error"] == False and len(_gpu_command_output["out_value"]) > 0 and not "No such file or directory" in _gpu_command_output["out_value"]:
                break

        if _gpu_command_output["error"] == True:
            self.gpu_usage_percentage = constants.ERROR_WHILE_READING_VALUE
            return 
    
        # The GPU load is stored as a percentage * 10, e.g 256 = 25.6%
        self.gpu_usage_percentage = utils.parseToFloat(_gpu_command_output["out_value"]) / 10

    def set_temperature_metrics(self):
        cpu = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone0/temp")
        gpu = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone1/temp")
        cv0 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone2/temp")
        cv1 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone3/temp")
        cv2 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone4/temp")
        soc0 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone5/temp")
        soc1 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone6/temp")
        soc2 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone7/temp")
        tj = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone8/temp")

        if cpu["error"] or gpu["error"] or cv0["error"] or cv1["error"] or cv2["error"] or soc0["error"] or soc1["error"] or soc2["error"] or tj["error"]:
            self.temperature_metrics = constants.ERROR_WHILE_READING_VALUE
            return
        
        self.temperature_metrics = {}
        self.temperature_metrics["_keys"] = ["cpu", "gpu", "cv0", "cv1", "cv2", "soc0", "soc1", "soc2", "tj"]
        self.temperature_metrics["cpu"] = constants.ERROR_WHILE_READING_VALUE if cpu["error"] else utils.parseToFloat(cpu["out_value"])
        self.temperature_metrics["gpu"] = constants.ERROR_WHILE_READING_VALUE if gpu["error"] else utils.parseToFloat(gpu["out_value"])
        self.temperature_metrics["cv0"] = constants.ERROR_WHILE_READING_VALUE if cv0["error"] else utils.parseToFloat(cv0["out_value"])
        self.temperature_metrics["cv1"] = constants.ERROR_WHILE_READING_VALUE if cv1["error"] else utils.parseToFloat(cv1["out_value"])
        self.temperature_metrics["cv2"] = constants.ERROR_WHILE_READING_VALUE if cv2["error"] else utils.parseToFloat(cv2["out_value"])
        self.temperature_metrics["soc0"] = constants.ERROR_WHILE_READING_VALUE if soc0["error"] else utils.parseToFloat(soc0["out_value"])
        self.temperature_metrics["soc1"] = constants.ERROR_WHILE_READING_VALUE if soc1["error"] else utils.parseToFloat(soc1["out_value"])
        self.temperature_metrics["soc2"] = constants.ERROR_WHILE_READING_VALUE if soc2["error"] else utils.parseToFloat(soc2["out_value"])
        self.temperature_metrics["tj"] = constants.ERROR_WHILE_READING_VALUE if tj["error"] else utils.parseToFloat(tj["out_value"])

    def set_battery_percentage(self):
        self.battery_percentage = -1