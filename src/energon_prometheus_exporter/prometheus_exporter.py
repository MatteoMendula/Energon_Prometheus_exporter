import time
import argparse
from prometheus_client import start_http_server, Gauge, Info
from energon_prometheus_exporter.drivers import driver
# import actualMeter
# example: sudo python3 prometheus_exporter.py 00:15:A3:00:55:02

parser = argparse.ArgumentParser()

parser.add_argument(
    "-p",
    "--port",
    nargs="?",
    default=9877,
    type=int,
    help="Port of the server",
)
args = parser.parse_args()

class EnergonPrometheusExporter:

    def __init__(self, app_port=9877, polling_interval_seconds=0.05):
        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds

        # Start up the server to expose the metrics.
        self.energon = driver.Energon()
        self.energon.instantiated_model.refresh_all_metrics()

        # ----------------- Try to instanciate actual meter -----------------
        # self.is_actual_meter_connected, self.actual_meter = self.TryToInstanciateActualMeter()

        # ----------------- Prometheus metrics to collect -----------------
        # static metrics
        self.device_info = Info("energon_device_info", "Device info")

        # power metrics
        self.total_in_power = Gauge("energon_total_in_power_mW", "Current total power consumption in milliwatts")
        self.cpu_in_power = Gauge("energon_cpu_in_power_mW", "Current cpu power consumption in milliwatts")
        self.gpu_in_power = Gauge("energon_gpu_in_power_mW", "Current gpu power consumption in milliwatts")
        # voltage metrics   
        self.total_in_voltage = Gauge("energon_total_in_voltage_mV", "Current total voltage in millivolts")
        self.cpu_in_voltage = Gauge("energon_cpu_in_voltage_mV", "Current cpu voltage in millivolts")
        self.gpu_in_voltage = Gauge("energon_gpu_in_voltage_mV", "Current gpu voltage in millivolts")
        # battery
        self.battery_percentage = Gauge("energon_battery_percentage", "Current battery percentage")

        # network metrics
        self.network_metrics_to_save = []
        self.network_metrics_to_save.append("rx_packets")
        self.network_metrics_to_save.append("rx_bytes")
        self.network_metrics_to_save.append("rx_errors")
        self.network_metrics_to_save.append("rx_dropped")
        self.network_metrics_to_save.append("tx_packets")
        self.network_metrics_to_save.append("tx_bytes")
        self.network_metrics_to_save.append("tx_errors")
        self.network_metrics_to_save.append("tx_dropped")

        for network_interface_name in self.energon.instantiated_model.network_metrics["_keys"]:
            for network_metric in self.network_metrics_to_save:
                setattr(self, "network_metrics_{}_{}".format(network_interface_name, network_metric), Gauge("energon_network_metrics_{}_{}".format(network_interface_name, network_metric), "Network metrics {} {}".format(network_interface_name, network_metric)))
        
        for network_interface_name in self.energon.instantiated_model.network_metrics["_keys"]:
            if not network_interface_name.startswith("w"):
                continue
            setattr(self, "network_quality_{}_link_quality".format(network_interface_name), Gauge("energon_network_quality_{}_link_quality_x_over_70".format(network_interface_name), "Network metrics {} - link_quality [x/70]".format(network_interface_name)))
            setattr(self, "network_quality_{}_signal_level".format(network_interface_name), Gauge("energon_network_quality_{}_signal_level_dBm".format(network_interface_name), "Network metrics {} - signal_level [dBm]".format(network_interface_name)))
            setattr(self, "network_quality_{}_bit_rate".format(network_interface_name), Gauge("energon_network_quality_{}_bit_rate_Mbs".format(network_interface_name), "Network metrics {} - bit_rate [Mb/s]".format(network_interface_name)))
        
        # cpu frequency metrics
        for core in self.energon.instantiated_model.cpu_frequency_metrics["_keys"]:
            setattr(self, "cpu_{}_frequency".format(core), Gauge("energon_cpu_{}_MHz".format(core), "CPU {} frequency in MHz".format(core)))

        # cpu usage metrics
        self.cpu_total_usage_percentage = Gauge("energon_cpu_total_usage_percentage", "CPU total usage in %")
        for core in self.energon.instantiated_model.cpu_usage_percentage["_keys"]:
            if core == "total":
                continue
            setattr(self, "cpu_{}_usage_percentage".format(core), Gauge("energon_cpu_{}_usage_percentage".format(core), "CPU {} usage in %".format(core)))

        # storage metrics
        for device_name in self.energon.instantiated_model.storage_metrics["devices"]:
            setattr(self, "storage_{}_total".format(device_name), Gauge("energon_storage_{}_total_bytes".format(device_name), "Storage {} total in bytes".format(device_name)))
            setattr(self, "storage_{}_used".format(device_name), Gauge("energon_storage_{}_used_bytes".format(device_name), "Storage {} used in bytes".format(device_name)))
            setattr(self, "storage_{}_available".format(device_name), Gauge("energon_storage_{}_available_bytes".format(device_name), "Storage {} available in bytes".format(device_name)))
            setattr(self, "storage_{}_percent_used".format(device_name), Gauge("energon_storage_{}_percent_used_percentage".format(device_name), "Storage {} percent used in %".format(device_name)))
        self.storage_total = Gauge("energon_storage_total_bytes", "Storage total in bytes")
        self.storage_used = Gauge("energon_storage_used_bytes", "Storage used in bytes")
        self.storage_available = Gauge("energon_storage_available_bytes", "Storage available in bytes")
        self.storage_percent_used = Gauge("energon_storage_percent_used_percentage", "Storage percent used in %")

        # ram metrics 
        self.ram_total = Gauge("energon_ram_total_bytes", "RAM total in bytes")
        self.ram_used = Gauge("energon_ram_used_bytes", "RAM used in bytes")
        self.ram_available = Gauge("energon_ram_available_bytes", "RAM available in bytes")
        self.ram_percent_used = Gauge("energon_ram_used_percentage", "RAM percent used in %")

        # gpu metrics
        self.gpu_total_usage_percentage = Gauge("energon_gpu_total_usage_percentage", "GPU total percent used in %")

        # temperature metrics
        for temp_metric in self.energon.instantiated_model.temperature_metrics["_keys"]:
            setattr(self, "temperature_{}".format(temp_metric), Gauge("energon_temperature_{}_mC".format(temp_metric), "Temperature {} in mC".format(temp_metric)))

        # actual metrics
        self.total_actual_watts = Gauge("energon_total_actual_watts", "Total actual watts")
        self.total_actual_volts = Gauge("energon_total_actual_volts", "Total actual volts")
        self.total_actual_amps = Gauge("energon_total_actual_amps", "Total actual amps")

    # def TryToInstanciateActualMeter(self):
    #     actual_meter = None
    #     is_actual_meter_connected = False
    #     if (len( sys.argv ) > 1 and (bool(re.match(regex, sys.argv[1])))):
    #         print("TryToInstanciateActualMeter at", sys.argv[1])
    #         regex = r"[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}"
    #         connection_address = sys.argv[1]
    #         try:
    #             actual_meter = actualMeter.UM25C(connection_address)
    #             is_actual_meter_connected = True
    #         except:
    #             print("Actual meter not connected")

    #     return (is_actual_meter_connected, actual_meter)
    
    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.energon.instantiated_model.refresh_all_metrics()
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        print("-------- fetching metrics ---------")
        
        self.device_info.info(
            {
                "detected_model": self.energon.detected_model, 
                "n_proc": str(int(self.energon.instantiated_model.n_proc)), 
                "network_interfaces": ' '.join(str(e) for e in self.energon.instantiated_model.network_interfaces)
            }
        )


        # power metrics
        self.total_in_power.set(self.energon.instantiated_model.energy_metrics["total_power"])
        self.cpu_in_power.set(self.energon.instantiated_model.energy_metrics["cpu_power"])
        self.gpu_in_power.set(self.energon.instantiated_model.energy_metrics["gpu_power"])

        self.total_in_voltage.set(self.energon.instantiated_model.energy_metrics["total_voltage"])
        self.cpu_in_voltage.set(self.energon.instantiated_model.energy_metrics["cpu_voltage"])
        self.gpu_in_voltage.set(self.energon.instantiated_model.energy_metrics["gpu_voltage"])

        # battery
        self.battery_percentage.set(self.energon.instantiated_model.battery_percentage)

        # network metrics
        for network_interface_name in self.energon.instantiated_model.network_metrics["_keys"]:
            for network_metric in self.network_metrics_to_save:
                # handle new network interface
                if not hasattr(self, "network_metrics_{}_{}".format(network_interface_name, network_metric)):
                    setattr(self, "network_metrics_{}_{}".format(network_interface_name, network_metric), Gauge("energon_network_metrics_{}_{}".format(network_interface_name, network_metric), "Network metrics {} {}".format(network_interface_name, network_metric)))
                getattr(self, "network_metrics_{}_{}".format(network_interface_name, network_metric)).set(self.energon.instantiated_model.network_metrics[network_interface_name][network_metric])

        for network_interface_name in self.energon.instantiated_model.network_metrics["_keys"]:
            if not network_interface_name.startswith("w"):
                continue
            # handle new network interface
            if not hasattr(self, "network_quality_{}_link_quality".format(network_interface_name)):
                setattr(self, "network_quality_{}_link_quality".format(network_interface_name), Gauge("energon_network_quality_{}_link_quality_x_over_70/70".format(network_interface_name), "Network metrics {} - link_quality [x/70]".format(network_interface_name)))
            if not hasattr(self, "network_quality_{}_signal_level".format(network_interface_name)):
                setattr(self, "network_quality_{}_signal_level".format(network_interface_name), Gauge("energon_network_quality_{}_signal_level_dBm".format(network_interface_name), "Network metrics {} - signal_level [dBm]".format(network_interface_name)))
            if not hasattr(self, "network_quality_{}_bit_rate".format(network_interface_name)):
                setattr(self, "network_quality_{}_bit_rate".format(network_interface_name), Gauge("energon_network_quality_{}_bit_rate_Mbs".format(network_interface_name), "Network metrics {} - bit_rate [Mb/s]".format(network_interface_name)))
            getattr(self, "network_quality_{}_link_quality".format(network_interface_name)).set(self.energon.instantiated_model.link_quality[network_interface_name]["link_quality"])
            getattr(self, "network_quality_{}_signal_level".format(network_interface_name)).set(self.energon.instantiated_model.link_quality[network_interface_name]["signal_level"])
            getattr(self, "network_quality_{}_bit_rate".format(network_interface_name)).set(self.energon.instantiated_model.link_quality[network_interface_name]["bit_rate"])

        # cpu frequency metrics
        for core in self.energon.instantiated_model.cpu_frequency_metrics["_keys"]:
            getattr(self, "cpu_{}_frequency".format(core)).set(self.energon.instantiated_model.cpu_frequency_metrics[core])

        # cpu usage metrics
        for core in self.energon.instantiated_model.cpu_usage_percentage["_keys"]:
            if core == "total":
                continue
            getattr(self, "cpu_{}_usage_percentage".format(core)).set(self.energon.instantiated_model.cpu_usage_percentage[core])
        self.cpu_total_usage_percentage.set(self.energon.instantiated_model.cpu_usage_percentage["total"])

        # storage metrics
        for device_name in self.energon.instantiated_model.storage_metrics["_keys"]:
            getattr(self, "storage_{}_total".format(device_name)).set(self.energon.instantiated_model.storage_metrics["devices"][device_name]["total"])
            getattr(self, "storage_{}_used".format(device_name)).set(self.energon.instantiated_model.storage_metrics["devices"][device_name]["used"])
            getattr(self, "storage_{}_available".format(device_name)).set(self.energon.instantiated_model.storage_metrics["devices"][device_name]["available"])
            getattr(self, "storage_{}_percent_used".format(device_name)).set(self.energon.instantiated_model.storage_metrics["devices"][device_name]["usage_percentage"])
        self.storage_total.set(self.energon.instantiated_model.storage_metrics["total"])
        self.storage_used.set(self.energon.instantiated_model.storage_metrics["used"])
        self.storage_available.set(self.energon.instantiated_model.storage_metrics["available"])
        self.storage_percent_used.set(self.energon.instantiated_model.storage_metrics["usage_percentage"])

        # ram metrics
        self.ram_total.set(self.energon.instantiated_model.ram_metrics["total"])
        self.ram_used.set(self.energon.instantiated_model.ram_metrics["used"])
        self.ram_available.set(self.energon.instantiated_model.ram_metrics["available"])
        self.ram_percent_used.set(self.energon.instantiated_model.ram_metrics["usage_percentage"])

        # gpu metrics
        self.gpu_total_usage_percentage.set(self.energon.instantiated_model.gpu_usage_percentage)

        # temperature metrics
        for temp_metric in self.energon.instantiated_model.temperature_metrics["_keys"]:
            getattr(self, "temperature_{}".format(temp_metric)).set(self.energon.instantiated_model.temperature_metrics[temp_metric])

    def run(self):
        """Run the metrics server"""
        print("Starting energon prometheus server")
        start_http_server(self.app_port)
        print("Energon prometheus server running on port " + str(self.app_port))
        self.run_metrics_loop()

if __name__ == "__main__":
    server = EnergonPrometheusExporter(app_port=args.port)
    server.run()
