from energon_prometheus_exporter.drivers import utils
from energon_prometheus_exporter.drivers import constants
from energon_prometheus_exporter.models.general_model import GeneralModel

# Jetson Nano Dev Kit Model 
# author: @MatteoMendula
# date: 2023-04-29

class JetsonAgxOrin(GeneralModel):
    def __init__(self):
        super().__init__()

    def set_energy_metrics(self):
        
        in_gpu_power = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon3/in1_input")
        in_cpu_power = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon3/in2_input")
        in_vin_sys_5v0_power = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon3/in3_input")
        in_nc1_power = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0041/hwmon/hwmon4/in1_input")
        in_vddq_vdd2_1v8aO_power = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0041/hwmon/hwmon4/in2_input")
        in_nc2_power = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0041/hwmon/hwmon4/in3_input")

        in_gpu_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon3/curr1_input")
        in_cpu_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon3/curr2_input")
        in_vin_sys_5v0_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0040/hwmon/hwmon3/curr3_input")
        in_nc1_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0041/hwmon/hwmon4/curr1_input")
        in_vddq_vdd2_1v8aO_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0041/hwmon/hwmon4/curr2_input")
        in_nc2_voltage = utils.run_command_and_get_output("cat /sys/bus/i2c/devices/1-0041/hwmon/hwmon4/curr3_input")

        in_total_power = constants.ERROR_WHILE_READING_VALUE
        if not (in_gpu_power["error"] or in_cpu_power["error"] or in_vin_sys_5v0_power["error"] or in_nc1_power["error"] or in_vddq_vdd2_1v8aO_power["error"] or in_nc2_power["error"]):
            in_total_power = utils.parseToFloat(in_gpu_power["out_value"]) + utils.parseToFloat(in_cpu_power["out_value"]) + utils.parseToFloat(in_vin_sys_5v0_power["out_value"]) + utils.parseToFloat(in_nc1_power["out_value"]) + utils.parseToFloat(in_vddq_vdd2_1v8aO_power["out_value"]) + utils.parseToFloat(in_nc2_power["out_value"])
        
        in_total_voltage = constants.ERROR_WHILE_READING_VALUE
        if not (in_gpu_voltage["error"] or in_cpu_voltage["error"] or in_vin_sys_5v0_voltage["error"] or in_nc1_voltage["error"] or in_vddq_vdd2_1v8aO_voltage["error"] or in_nc2_voltage["error"]):
            in_total_voltage = utils.parseToFloat(in_gpu_voltage["out_value"]) + utils.parseToFloat(in_cpu_voltage["out_value"]) + utils.parseToFloat(in_vin_sys_5v0_voltage["out_value"]) + utils.parseToFloat(in_nc1_voltage["out_value"]) + utils.parseToFloat(in_vddq_vdd2_1v8aO_voltage["out_value"]) + utils.parseToFloat(in_nc2_voltage["out_value"])

        self.energy_metrics = {}
        self.energy_metrics["_keys"] = ["total_power", "gpu_power", "cpu_power", "in_vin_sys_5v0_power", "in_nc1_power", "in_vddq_vdd2_1v8aO_power", "in_nc2_power", "total_voltage", "gpu_voltage", "cpu_voltage", "in_vin_sys_5v0_voltage", "in_nc1_voltage", "in_vddq_vdd2_1v8aO_voltage", "in_nc2_voltage"]

        self.energy_metrics["total_power"] = in_total_power
        self.energy_metrics["gpu_power"] = constants.ERROR_WHILE_READING_VALUE if in_gpu_power["error"] else utils.parseToFloat(in_gpu_power["out_value"])
        self.energy_metrics["cpu_power"] = constants.ERROR_WHILE_READING_VALUE if in_cpu_power["error"] else utils.parseToFloat(in_cpu_power["out_value"])
        self.energy_metrics["in_vin_sys_5v0_power"] = constants.ERROR_WHILE_READING_VALUE if in_vin_sys_5v0_power["error"] else utils.parseToFloat(in_vin_sys_5v0_power["out_value"])
        self.energy_metrics["in_nc1_power"] = constants.ERROR_WHILE_READING_VALUE if in_nc1_power["error"] else utils.parseToFloat(in_nc1_power["out_value"])
        self.energy_metrics["in_vddq_vdd2_1v8aO_power"] = constants.ERROR_WHILE_READING_VALUE if in_vddq_vdd2_1v8aO_power["error"] else utils.parseToFloat(in_vddq_vdd2_1v8aO_power["out_value"])
        self.energy_metrics["in_nc2_power"] = constants.ERROR_WHILE_READING_VALUE if in_nc2_power["error"] else utils.parseToFloat(in_nc2_power["out_value"])

        self.energy_metrics["total_voltage"] = in_total_voltage
        self.energy_metrics["cpu_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_cpu_voltage["error"] else utils.parseToFloat(in_cpu_voltage["out_value"])
        self.energy_metrics["gpu_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_gpu_voltage["error"] else utils.parseToFloat(in_gpu_voltage["out_value"])
        self.energy_metrics["in_vin_sys_5v0_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_vin_sys_5v0_voltage["error"] else utils.parseToFloat(in_vin_sys_5v0_voltage["out_value"])
        self.energy_metrics["in_nc1_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_nc1_voltage["error"] else utils.parseToFloat(in_nc1_voltage["out_value"])
        self.energy_metrics["in_vddq_vdd2_1v8aO_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_vddq_vdd2_1v8aO_voltage["error"] else utils.parseToFloat(in_vddq_vdd2_1v8aO_voltage["out_value"])
        self.energy_metrics["in_nc2_voltage"] = constants.ERROR_WHILE_READING_VALUE if in_nc2_voltage["error"] else utils.parseToFloat(in_nc2_voltage["out_value"])
                            
    def set_cpu_frequency(self):
        core_0 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq")
        core_1 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu1/cpufreq/cpuinfo_cur_freq")
        core_2 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_cur_freq")
        core_3 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_cur_freq")
        core_4 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu4/cpufreq/cpuinfo_cur_freq")
        core_5 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu5/cpufreq/cpuinfo_cur_freq")
        core_6 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu6/cpufreq/cpuinfo_cur_freq")
        core_7 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu7/cpufreq/cpuinfo_cur_freq")
        
        self.cpu_frequency_metrics = {}
        self.cpu_frequency_metrics["_keys"] = ["core_0", "core_1", "core_2", "core_3", "core_4", "core_5", "core_6", "core_7"]
        
        self.cpu_frequency_metrics["core_0"] = constants.ERROR_WHILE_READING_VALUE if core_0["error"] else utils.parseToFloat(core_0["out_value"])
        self.cpu_frequency_metrics["core_1"] = constants.ERROR_WHILE_READING_VALUE if core_1["error"] else utils.parseToFloat(core_1["out_value"])
        self.cpu_frequency_metrics["core_2"] = constants.ERROR_WHILE_READING_VALUE if core_2["error"] else utils.parseToFloat(core_2["out_value"])
        self.cpu_frequency_metrics["core_3"] = constants.ERROR_WHILE_READING_VALUE if core_3["error"] else utils.parseToFloat(core_3["out_value"])
        self.cpu_frequency_metrics["core_4"] = constants.ERROR_WHILE_READING_VALUE if core_4["error"] else utils.parseToFloat(core_4["out_value"])
        self.cpu_frequency_metrics["core_5"] = constants.ERROR_WHILE_READING_VALUE if core_5["error"] else utils.parseToFloat(core_5["out_value"])
        self.cpu_frequency_metrics["core_6"] = constants.ERROR_WHILE_READING_VALUE if core_6["error"] else utils.parseToFloat(core_6["out_value"])
        self.cpu_frequency_metrics["core_7"] = constants.ERROR_WHILE_READING_VALUE if core_7["error"] else utils.parseToFloat(core_7["out_value"])

    def set_gpu_usage_percentage(self):

        gpu_load_possible_commands = [ "cat /sys/devices/57000000.gpu/load", "cat /sys/devices/gpu.0/load", "cat /sys/devices/platform/host1x/57000000.gpu/load" ]
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
        cpu = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone0/temp")
        gpu = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone1/temp")
        cv0 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone2/temp")
        cv1 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone3/temp")
        cv2 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone4/temp")
        soc0 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone5/temp")
        soc1 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone6/temp")
        soc2 = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone7/temp")
        tj = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone8/temp")
        tboard_tegra = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone9/temp")
        tdiode_tegra = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone10/temp")

        if cpu["error"] or gpu["error"] or cv0["error"] or cv1["error"] or cv2["error"] or soc0["error"] or soc1["error"] or soc2["error"] or tj["error"] or tboard_tegra["error"] or tdiode_tegra["error"]:
            self.temperature_metrics = constants.ERROR_WHILE_READING_VALUE
            return
        
        self.temperature_metrics = {}
        self.temperature_metrics["_keys"] = ["cpu", "gpu", "cv0", "cv1", "cv2", "soc0", "soc1", "soc2", "tj", "tboard_tegra", "tdiode_tegra"]
        self.temperature_metrics["cpu"] = constants.ERROR_WHILE_READING_VALUE if cpu["error"] else utils.parseToFloat(cpu["out_value"])
        self.temperature_metrics["gpu"] = constants.ERROR_WHILE_READING_VALUE if gpu["error"] else utils.parseToFloat(gpu["out_value"])
        self.temperature_metrics["cv0"] = constants.ERROR_WHILE_READING_VALUE if cv0["error"] else utils.parseToFloat(cv0["out_value"])
        self.temperature_metrics["cv1"] = constants.ERROR_WHILE_READING_VALUE if cv1["error"] else utils.parseToFloat(cv1["out_value"])
        self.temperature_metrics["cv2"] = constants.ERROR_WHILE_READING_VALUE if cv2["error"] else utils.parseToFloat(cv2["out_value"])
        self.temperature_metrics["soc0"] = constants.ERROR_WHILE_READING_VALUE if soc0["error"] else utils.parseToFloat(soc0["out_value"])
        self.temperature_metrics["soc1"] = constants.ERROR_WHILE_READING_VALUE if soc1["error"] else utils.parseToFloat(soc1["out_value"])
        self.temperature_metrics["soc2"] = constants.ERROR_WHILE_READING_VALUE if soc2["error"] else utils.parseToFloat(soc2["out_value"])
        self.temperature_metrics["tj"] = constants.ERROR_WHILE_READING_VALUE if tj["error"] else utils.parseToFloat(tj["out_value"])
        self.temperature_metrics["tboard_tegra"] = constants.ERROR_WHILE_READING_VALUE if tboard_tegra["error"] else utils.parseToFloat(tboard_tegra["out_value"])
        self.temperature_metrics["tdiode_tegra"] = constants.ERROR_WHILE_READING_VALUE if tdiode_tegra["error"] else utils.parseToFloat(tdiode_tegra["out_value"])

    def set_battery_percentage(self):
        self.battery_percentage = -1