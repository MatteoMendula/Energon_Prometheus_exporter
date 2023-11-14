import time
from energon_prometheus_exporter.drivers import utils
from energon_prometheus_exporter.drivers import constants

class GeneralModel:
    def __init__(self):
        self.network_interfaces = constants.ERROR_MODEL_NOT_SUPPORTED
        self.network_metrics = constants.ERROR_MODEL_NOT_SUPPORTED
        self.link_quality = constants.ERROR_MODEL_NOT_SUPPORTED
        self.energy_metrics = constants.ERROR_MODEL_NOT_SUPPORTED
        self.n_proc = constants.ERROR_MODEL_NOT_SUPPORTED
        self.cpu_usage_percentage = constants.ERROR_MODEL_NOT_SUPPORTED
        self.cpu_frequency_metrics = constants.ERROR_MODEL_NOT_SUPPORTED
        self.storage_metrics = constants.ERROR_MODEL_NOT_SUPPORTED
        self.temperature_metrics = constants.ERROR_MODEL_NOT_SUPPORTED
        self.ram_metrics = constants.ERROR_MODEL_NOT_SUPPORTED
        self.battery_percentage = constants.ERROR_MODEL_NOT_SUPPORTED
        self.gpu_usage_percentage = constants.ERROR_MODEL_NOT_SUPPORTED

    def set_network_interfaces(self):
        _network_interfaces = utils.run_command_and_get_output("ls /sys/class/net/")
        self.network_interfaces = constants.ERROR_WHILE_READING_VALUE if _network_interfaces["error"] else _network_interfaces["out_value"].split("\n")

    def set_network_metrics(self):
        self.set_network_interfaces()
        self.network_metrics = {}
        self.network_metrics["_keys"] = []
        for interface in self.network_interfaces:
            rx_packets = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/rx_packets")
            tx_packets = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/tx_packets")
            rx_bytes = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/rx_bytes")
            tx_bytes = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/tx_bytes")
            rx_errors = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/rx_errors")
            tx_errors = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/tx_errors")
            rx_dropped = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/rx_dropped")
            tx_dropped = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/tx_dropped")

            interface_name = utils.clean_metric_name_to_prometheus_format(interface)
            self.network_metrics["_keys"].append(interface_name)

            self.network_metrics[interface_name] = {}
            self.network_metrics[interface_name]["rx_packets"] = constants.ERROR_WHILE_READING_VALUE if rx_packets["error"] else utils.parseToFloat(rx_packets["out_value"])
            self.network_metrics[interface_name]["tx_packets"] = constants.ERROR_WHILE_READING_VALUE if tx_packets["error"] else utils.parseToFloat(tx_packets["out_value"])
            self.network_metrics[interface_name]["rx_bytes"] = constants.ERROR_WHILE_READING_VALUE if rx_bytes["error"] else utils.parseToFloat(rx_bytes["out_value"])
            self.network_metrics[interface_name]["tx_bytes"] = constants.ERROR_WHILE_READING_VALUE if tx_bytes["error"] else utils.parseToFloat(tx_bytes["out_value"])
            self.network_metrics[interface_name]["rx_errors"] = constants.ERROR_WHILE_READING_VALUE if rx_errors["error"] else utils.parseToFloat(rx_errors["out_value"])
            self.network_metrics[interface_name]["tx_errors"] = constants.ERROR_WHILE_READING_VALUE if tx_errors["error"] else utils.parseToFloat(tx_errors["out_value"])
            self.network_metrics[interface_name]["rx_dropped"] = constants.ERROR_WHILE_READING_VALUE if rx_dropped["error"] else utils.parseToFloat(rx_dropped["out_value"])
            self.network_metrics[interface_name]["tx_dropped"] = constants.ERROR_WHILE_READING_VALUE if tx_dropped["error"] else utils.parseToFloat(tx_dropped["out_value"])

    def set_link_quality(self):
        self.set_network_interfaces()
        self.link_quality = {}
        self.link_quality["_keys"] = []

        for _interface_name in self.network_interfaces:
            if not _interface_name.startswith("w"):
                continue

            interface_name = utils.clean_metric_name_to_prometheus_format(_interface_name)
            
            link_quality = utils.run_command_and_get_output("iwconfig " + interface_name)
            data = {}
            data["link_quality"] = constants.ERROR_WHILE_READING_VALUE
            data["signal_level"] = constants.ERROR_WHILE_READING_VALUE
            data["bit_rate"] = constants.ERROR_WHILE_READING_VALUE
            if not link_quality["error"] and len(link_quality["out_value"]) > 0:
                self.link_quality["_keys"].append(interface_name)
                rows = link_quality["out_value"].split("\n")
                for row in rows:
                    _row = row.strip()
                    if _row.startswith("Link Quality"):
                        data["link_quality"] = _row.split("=")[1].split(" ")[0].split("/")[0]   # x/70
                        data["signal_level"] = _row.split("=")[2].split(" ")[0]                 # dBm
                    if _row.startswith("Bit Rate"):
                        data["bit_rate"] = _row.split("=")[1].split(" ")[0]                     # Mb/s

            self.link_quality[interface_name] = constants.ERROR_WHILE_READING_VALUE if link_quality["error"] else data

        return self.link_quality

    def set_energy_metrics(self):
        pass

    def set_n_proc(self):
        _n_proc = utils.run_command_and_get_output("nproc")
        self.n_proc = constants.ERROR_WHILE_READING_VALUE if _n_proc["error"] else utils.parseToFloat(_n_proc["out_value"])
    
    def set_cpu_usage_percentage(self):
        
        _cpu_load_1 = utils.run_command_and_get_output("cat /proc/stat")
        if _cpu_load_1["error"] == True:
            self.cpu_usage_percentage = constants.ERROR_WHILE_READING_VALUE
            return 

        def get_idle_and_total_cpu_load(proc_stat_out_value):
            matched_lines = [line for line in proc_stat_out_value.split('\n') if line.startswith("cpu")]

            result_metrics = {}
            result_metrics["idle"] = {}
            result_metrics["total"] = {}


            for index, line in enumerate(matched_lines):
                metrics = [utils.parseToFloat(amount) for amount in line.split()]
                idle = metrics[4]
                total = sum(metrics[1:])
                if index == 0:
                    result_metrics["total"]["total"] = total
                    result_metrics["idle"]["total"] = idle
                else:
                    result_metrics["total"]["core_{}".format(index-1)] = total
                    result_metrics["idle"]["core_{}".format(index-1)] = idle

            return result_metrics
            
        first_read = get_idle_and_total_cpu_load(_cpu_load_1["out_value"])

        time.sleep(1)

        _cpu_load_2 = utils.run_command_and_get_output("cat /proc/stat")
        if _cpu_load_2["error"] == True:
            self.cpu_usage_percentage = constants.ERROR_WHILE_READING_VALUE
            return 
        
        second_read = get_idle_and_total_cpu_load(_cpu_load_2["out_value"])

        self.cpu_usage_percentage = {}
        self.cpu_usage_percentage["_keys"] = []
        for key in first_read["total"].keys():
            self.cpu_usage_percentage["_keys"].append(key)
            self.cpu_usage_percentage[key] = (1 - (second_read["idle"][key] - first_read["idle"][key]) / (second_read["total"][key] - first_read["total"][key])) * 100

    def set_cpu_frequency(self):
        pass

    def set_storage_metrics(self):
        _storage_metrics = utils.run_command_and_get_output("df -h /")
        if _storage_metrics["error"] == True:
            self.storage_metrics["out_value"] = constants.ERROR_WHILE_READING_VALUE
            return 
        
        matched_lines = [line for line in _storage_metrics["out_value"].split('\n') if line.startswith("/dev")]
        self.storage_metrics = {}
        self.storage_metrics["_keys"] = []
        self.storage_metrics["devices"] = {}
        self.storage_metrics["total"] = 0
        self.storage_metrics["used"] = 0
        self.storage_metrics["available"] = 0
        self.storage_metrics["usage_percentage"] = 0

        # parse every metric in MB
        for line in matched_lines:
            # keeping track of all storage devices
            device_name = utils.clean_metric_name_to_prometheus_format(line.split()[0])
            self.storage_metrics["_keys"].append(device_name)
            self.storage_metrics["devices"][device_name] = {}
            self.storage_metrics["devices"][device_name]["total"] = utils.parseToFloat(line.split()[1]) * utils.getConversionToMBCoefficient(line.split()[1])
            self.storage_metrics["devices"][device_name]["used"] = utils.parseToFloat(line.split()[2]) * utils.getConversionToMBCoefficient(line.split()[2])
            self.storage_metrics["devices"][device_name]["available"] = utils.parseToFloat(line.split()[3]) * utils.getConversionToMBCoefficient(line.split()[3])
            self.storage_metrics["devices"][device_name]["usage_percentage"] = (self.storage_metrics["devices"][device_name]["used"] / self.storage_metrics["devices"][device_name]["total"]) * 100

            # summing up all available storage
            self.storage_metrics["total"] = self.storage_metrics["total"] + utils.parseToFloat(line.split()[1])
            self.storage_metrics["used"] = self.storage_metrics["used"] + utils.parseToFloat(line.split()[2])
            self.storage_metrics["available"] = self.storage_metrics["available"] + utils.parseToFloat(line.split()[3])
            self.storage_metrics["usage_percentage"] = (self.storage_metrics["used"] / self.storage_metrics["total"]) * 100
    
    def set_temperature_metrics(self):
        pass

    def set_ram_metrics(self):
        _ram_metrics = utils.run_command_and_get_output("cat /proc/meminfo")

        if _ram_metrics["error"] == True:
            self.ram_metrics["out_value"] = constants.ERROR_WHILE_READING_VALUE
            return 
        
        matched_lines = [line for line in _ram_metrics["out_value"].split('\n') if line.startswith("Mem")]
        self.ram_metrics = {}
        self.ram_metrics["_keys"] = ["total", "used", "available", "usage_percentage"]
        self.ram_metrics["total"] = utils.parseToFloat(matched_lines[0].split()[1])
        self.ram_metrics["used"] = utils.parseToFloat(matched_lines[1].split()[1])
        self.ram_metrics["available"] = utils.parseToFloat(matched_lines[2].split()[1])
        self.ram_metrics["usage_percentage"] = (self.ram_metrics["used"] / self.ram_metrics["total"]) * 100

    def set_battery_percentage(self):
        pass

    def set_gpu_usage_percentage(self):
        pass

    def refresh_all_metrics(self):
        self.set_network_interfaces()
        self.set_network_metrics()
        self.set_link_quality()
        self.set_energy_metrics()
        self.set_n_proc()
        self.set_cpu_usage_percentage()
        self.set_cpu_frequency()
        self.set_storage_metrics()
        self.set_temperature_metrics()
        self.set_ram_metrics()
        self.set_battery_percentage()
        self.set_gpu_usage_percentage()