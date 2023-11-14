from energon_prometheus_exporter.drivers import utils
from energon_prometheus_exporter.drivers import constants
from energon_prometheus_exporter.models import general_model, jetson_nano_dev_kit, jetson_xavier_dev_kit, ubuntu_64, jetson_agx_xavier, jetson_agx_orin

# Energon - A Prometheus exporter for energy consumption metrics of embedded devices
# This class is the main class of the project. It is responsible for detecting the model of the device and calling the appropriate functions to get the metrics.
# author: @MatteoMendula
# date: 2023-04-23

class Energon:
    def __init__(self):
        self.name = 'Energon Prometheus Exporter'
        self.version = '0.0.1'
        self.detected_model = self.detect_model()
        self.instantiated_model = None
        self.instantiate_model()


    def detect_model(self):
        # check if the device is a Jetson Nano Developer Kit first
        out = utils.run_command_and_get_output("lshw -C systemshw -C system")
        if out["error"]:
            return "Error in getting model %s" % out["out_value"]
        if "nvidia jetson nano developer kit" in out["out_value"].lower():
            return constants.JETSON_NANO_DEV_KIT
        if "nvidia jetson xavier nx developer kit" in out["out_value"].lower():
            return constants.JETSON_XAVIER_DEV_KIT
        if "jetson-agx" in out["out_value"].lower():
            return constants.JETSON_AGX_XAVIER
        if "jetson agx orin" in out["out_value"].lower():
            return constants.JETSON_AGX_ORIN
        
        # check if the device is a Ubuntu 64 bit
        out = utils.run_command_and_get_output("cat /etc/os-release")
        architecture = utils.run_command_and_get_output("uname -m")
        if "ubuntu" in out["out_value"] and "x86_64" in architecture["out_value"].lower():
            return constants.UBUNTU_64
        
        return constants.UNKNOWN_MODEL
        
    def instantiate_model(self):
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            self.instantiated_model = jetson_nano_dev_kit.JetsonNanoDevKit()
        elif self.detected_model == constants.JETSON_XAVIER_DEV_KIT:
            self.instantiated_model = jetson_xavier_dev_kit.JetsonXavierDevKit()
        elif self.detected_model == constants.JETSON_AGX_XAVIER:
            self.instantiated_model = jetson_agx_xavier.JetsonAgxXavier()
        elif self.detected_model == constants.JETSON_AGX_ORIN:
            self.instantiated_model = jetson_agx_orin.JetsonAgxOrin()
        elif self.detected_model == constants.UBUNTU_64:
            self.instantiated_model = ubuntu_64.Ubuntu64()
        else:
            self.instantiated_model = general_model.GeneralModel()
        
   
if __name__ == '__main__':
    energon = Energon()
    detected_model = energon.detected_model
    energon.instantiated_model.refresh_all_metrics()
    network_interfaces = energon.instantiated_model.network_interfaces
    network_metrics = energon.instantiated_model.network_metrics
    link_quality = energon.instantiated_model.link_quality
    energy_metrics = energon.instantiated_model.energy_metrics
    n_proc = energon.instantiated_model.n_proc
    cpu_usage_percentage = energon.instantiated_model.cpu_usage_percentage
    cpu_frequency_metrics = energon.instantiated_model.cpu_frequency_metrics
    storage_metrics = energon.instantiated_model.storage_metrics
    temperature_metrics = energon.instantiated_model.temperature_metrics
    ram_metrics = energon.instantiated_model.ram_metrics
    battery_percentage = energon.instantiated_model.battery_percentage
    gpu_usage_percentage = energon.instantiated_model.gpu_usage_percentage

    print("detected_model: ", detected_model)
    print("network_interfaces: ", network_interfaces)
    print("network_metrics: ", network_metrics)
    print("link_quality: ", link_quality)
    print("energy_metrics: ", energy_metrics)
    print("n_proc: ", n_proc)
    print("cpu_usage_percentage: ", cpu_usage_percentage)
    print("cpu_frequency_metrics: ", cpu_frequency_metrics)
    print("storage_metrics: ", storage_metrics)
    print("temperature_metrics: ", temperature_metrics)
    print("ram_metrics: ", ram_metrics)
    print("battery_percentage: ", battery_percentage)
    print("gpu_usage_percentage: ", gpu_usage_percentage)
    
