import utils
import time
import constants
from models.general_model import GeneralModel

# Jetson Nano Xavier Kit Model 
# author: @AndAgio
# date: 2023-04-01

class JetsonXavierDevKit(GeneralModel):
    def __init__(self):
        super().__init__()

    def set_energy_metrics(self):
        
        in_gpu_power = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/in1_input")
        in_cpu_power = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/in2_input")
        in_soc_power = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/in3_input")
        in_cv_power = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/in4_input")
        in_vddrq_power = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/in5_input")
        in_sys5v_power = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/in6_input")

        in_gpu_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/curr1_input")
        in_cpu_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/curr2_input")
        in_soc_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/curr3_input")
        in_cv_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/curr4_input")
        in_vddrq_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/curr5_input")
        in_sys5v_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221/7-0040/hwmon/hwmon5/curr_input")

        in_total_power = constants.ERROR_WHILE_READING_VALUE
        if not (in_gpu_power["error"] or in_cpu_power["error"] or in_soc_power["error"] or in_cv_power["error"] or in_vddrq_power["error"] or in_sys5v_power["error"]):
            in_total_power = utils.parseToFloat(in_gpu_power["out_value"]) + utils.parseToFloat(in_cpu_power["out_value"]) + utils.parseToFloat(in_soc_power["out_value"]) + utils.parseToFloat(in_cv_power["out_value"]) + utils.parseToFloat(in_vddrq_power["out_value"]) + utils.parseToFloat(in_sys5v_power["out_value"])
        
        in_total_voltage = constants.ERROR_WHILE_READING_VALUE
        if not (in_gpu_voltage["error"] or in_cpu_voltage["error"] or in_soc_voltage["error"] or in_cv_voltage["error"] or in_vddrq_voltage["error"] or in_sys5v_voltage["error"]):
            in_total_voltage = utils.parseToFloat(in_gpu_voltage["out_value"]) + utils.parseToFloat(in_cpu_voltage["out_value"]) + utils.parseToFloat(in_soc_voltage["out_value"]) + utils.parseToFloat(in_cv_voltage["out_value"]) + utils.parseToFloat(in_vddrq_voltage["out_value"]) + utils.parseToFloat(in_sys5v_voltage["out_value"])

        self.energy_metrics = {}
        self.energy_metrics["_keys"] = ["total_power", "gpu_power", "cpu_power", "soc_power", "cv_power", "vddrq_power", "sys5v_power", "total_voltage", "gpu_voltage", "cpu_voltage", "soc_voltage", "cv_voltage", "vddrq_voltage", "sys5v_voltage"]

        self.energy_metrics["total_power"] = in_total_power
        self.energy_metrics["gpu_power"] = constants.ERROR_WHILE_READING_VALUE if in_gpu_power["error"] else utils.parseToFloat(in_gpu_power["out_value"])
        self.energy_metrics["cpu_power"] = constants.ERROR_WHILE_READING_VALUE if in_cpu_power["error"] else utils.parseToFloat(in_cpu_power["out_value"])
        self.energy_metrics["soc_power"] = constants.ERROR_WHILE_READING_VALUE if in_soc_power["error"] else utils.parseToFloat(in_soc_power["out_value"])
        self.energy_metrics["cv_power"] = constants.ERROR_WHILE_READING_VALUE if in_cv_power["error"] else utils.parseToFloat(in_cv_power["out_value"])
        self.energy_metrics["vddrq_power"] = constants.ERROR_WHILE_READING_VALUE if in_vddrq_power["error"] else utils.parseToFloat(in_vddrq_power["out_value"])
        self.energy_metrics["sys5v_power"] = constants.ERROR_WHILE_READING_VALUE if in_sys5v_power["error"] else utils.parseToFloat(in_sys5v_power["out_value"])

        self.energy_metrics["total_voltage"] = in_total_voltage
        self.energy_metrics["cpu_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_cpu_voltage["error"] else utils.parseToFloat(in_cpu_voltage["out_value"])
        self.energy_metrics["gpu_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_gpu_voltage["error"] else utils.parseToFloat(in_gpu_voltage["out_value"])
        self.energy_metrics["soc_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_soc_voltage["error"] else utils.parseToFloat(in_soc_voltage["out_value"])
        self.energy_metrics["cv_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_cv_voltage["error"] else utils.parseToFloat(in_cv_voltage["out_value"])
        self.energy_metrics["vddrq_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_vddrq_voltage["error"] else utils.parseToFloat(in_vddrq_voltage["out_value"])
        self.energy_metrics["sys5v_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_sys5v_voltage["error"] else utils.parseToFloat(in_sys5v_voltage["out_value"])


    def set_cpu_frequency(self):
        core_0 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq")
        core_1 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu1/cpufreq/cpuinfo_cur_freq")
        core_2 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_cur_freq")
        core_3 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_cur_freq")
        core_4 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_cur_freq")
        core_5 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_cur_freq")
        
        self.cpu_frequency_metrics = {}
        self.cpu_frequency_metrics["_keys"] = ["core_0", "core_1", "core_2", "core_3", "core_4", "core_5"]
        
        self.cpu_frequency_metrics["core_0"] = constants.ERROR_WHILE_READING_VALUE if core_0["error"] else utils.parseToFloat(core_0["out_value"])
        self.cpu_frequency_metrics["core_1"] = constants.ERROR_WHILE_READING_VALUE if core_1["error"] else utils.parseToFloat(core_1["out_value"])
        self.cpu_frequency_metrics["core_2"] = constants.ERROR_WHILE_READING_VALUE if core_2["error"] else utils.parseToFloat(core_2["out_value"])
        self.cpu_frequency_metrics["core_3"] = constants.ERROR_WHILE_READING_VALUE if core_3["error"] else utils.parseToFloat(core_3["out_value"])
        self.cpu_frequency_metrics["core_4"] = constants.ERROR_WHILE_READING_VALUE if core_4["error"] else utils.parseToFloat(core_4["out_value"])
        self.cpu_frequency_metrics["core_5"] = constants.ERROR_WHILE_READING_VALUE if core_5["error"] else utils.parseToFloat(core_5["out_value"])

    def set_gpu_usage_percentage(self):

        gpu_load_possible_commands = [ "cat /sys/devices/gpu.0/load" ]
        _gpu_command_output = None

        for command in gpu_load_possible_commands:
            _gpu_command_output = utils.run_command_and_get_output(command)
            if _gpu_command_output["error"] == False and len(_gpu_command_output["out_value"]) > 0:
                break

        if _gpu_command_output["error"] == True:
            self.gpu_usage_percentage = constants.ERROR_WHILE_READING_VALUE
            return 
    
        # The GPU load is stored as a percentage * 10, e.g 256 = 25.6%
        self.gpu_usage_percentage = utils.parseToFloat(_gpu_command_output["out_value"]) / 10

    def set_temperature_metrics(self):
        ao = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone0/temp")
        cpu = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone1/temp")
        gpu = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone2/temp")
        pll = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone3/temp")
        pmic = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone4/temp")
        fan = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone5/temp")

        if ao["error"] or cpu["error"] or gpu["error"] or pll["error"] or pmic["error"] or fan["error"]:
            self.temperature_metrics = constants.ERROR_WHILE_READING_VALUE
            return
        
        self.temperature_metrics = {}
        self.temperature_metrics["_keys"] = ["ao", "cpu", "gpu", "pll", "pmic", "fan"]
        self.temperature_metrics["ao"] = utils.parseToFloat(ao["out_value"])
        self.temperature_metrics["cpu"] = utils.parseToFloat(cpu["out_value"])
        self.temperature_metrics["gpu"] = utils.parseToFloat(gpu["out_value"])
        self.temperature_metrics["pll"] = utils.parseToFloat(pll["out_value"])
        self.temperature_metrics["pmic"] = utils.parseToFloat(pmic["out_value"])
        self.temperature_metrics["fan"] = utils.parseToFloat(fan["out_value"])

    def set_battery_percentage(self):
        self.battery_percentage = -1
