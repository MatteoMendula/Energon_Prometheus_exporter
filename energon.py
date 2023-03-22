import utils
import constants
from models import jetson_nano_dev_kit

class Energon:
    def __init__(self):
        self.name = 'Energon Prometheus Exporter'
        self.version = '0.0.1'
        self.detected_model = self.detect_model()
        self.n_cores = self.get_n_cores()
        self.network_interfaces = self.get_network_interfaces()["available_networks"]


    def detect_model(self):
        out = utils.run_command_and_get_output("lshw -C systemshw -C system")
        if out["error"]:
            return "Error in getting model %s" % out["out_value"]
        if "nvidia jetson nano developer kit" in out["out_value"].lower():
            return constants.JETSON_NANO_DEV_KIT
        else:  
            return constants.UNKNOWN_MODEL
        
    def get_energy_metrics(self):
        energy_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            energy_metrics["error"] = True
            energy_metrics["total"] = constants.ERROR_MODEL_NOT_SUPPORTED
            energy_metrics["cpu"] = constants.ERROR_MODEL_NOT_SUPPORTED
            energy_metrics["gpu"] = constants.ERROR_MODEL_NOT_SUPPORTED
            return energy_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_energy_metrics(energy_metrics)
        
    def get_cpu_frequency_metrics(self):
        cpu_frquency_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            cpu_frquency_metrics["error"] = True
            cpu_frquency_metrics["core_0"] = constants.ERROR_MODEL_NOT_SUPPORTED
            cpu_frquency_metrics["core_1"] = constants.ERROR_MODEL_NOT_SUPPORTED
            cpu_frquency_metrics["core_2"] = constants.ERROR_MODEL_NOT_SUPPORTED
            cpu_frquency_metrics["core_3"] = constants.ERROR_MODEL_NOT_SUPPORTED
            return cpu_frquency_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_cpu_frequency(cpu_frquency_metrics)
        
    def get_cpu_load_metrics(self):
        cpu_load_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            cpu_load_metrics["error"] = True
            cpu_load_metrics["total"] = constants.ERROR_MODEL_NOT_SUPPORTED
            cpu_load_metrics["core_0"] = constants.ERROR_MODEL_NOT_SUPPORTED
            cpu_load_metrics["core_1"] = constants.ERROR_MODEL_NOT_SUPPORTED
            cpu_load_metrics["core_2"] = constants.ERROR_MODEL_NOT_SUPPORTED
            cpu_load_metrics["core_3"] = constants.ERROR_MODEL_NOT_SUPPORTED
            return cpu_load_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_cpu_load_percentage(cpu_load_metrics)

    def get_n_cores(self):
        n_core = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            n_core["error"] = True
            n_core["n_cpus"] = constants.ERROR_MODEL_NOT_SUPPORTED
            return n_core

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_n_cpus(n_core)

    def get_storage_metrics(self):
        storage_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            storage_metrics["error"] = True
            storage_metrics["total"] = constants.ERROR_MODEL_NOT_SUPPORTED
            storage_metrics["used"] = constants.ERROR_MODEL_NOT_SUPPORTED
            storage_metrics["available"] = constants.ERROR_MODEL_NOT_SUPPORTED
            return storage_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_storage_metrics(storage_metrics)
        
    def get_ram_metrics(self):
        ram_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            ram_metrics["error"] = True
            ram_metrics["total"] = constants.ERROR_MODEL_NOT_SUPPORTED
            ram_metrics["free"] = constants.ERROR_MODEL_NOT_SUPPORTED
            ram_metrics["available"] = constants.ERROR_MODEL_NOT_SUPPORTED
            return ram_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_ram_metrics(ram_metrics)
        
    def get_gpu_load(self):
        gpu_load = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            gpu_load["error"] = True
            gpu_load["total"] = constants.ERROR_MODEL_NOT_SUPPORTED
            return gpu_load

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_gpu_metrics(gpu_load)
        
    def get_temperature_metrics(self):
        temperature_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            temperature_metrics["error"] = True
            temperature_metrics["ao"] = constants.ERROR_MODEL_NOT_SUPPORTED
            temperature_metrics["cpu"] = constants.ERROR_MODEL_NOT_SUPPORTED
            temperature_metrics["gpu"] = constants.ERROR_MODEL_NOT_SUPPORTED
            temperature_metrics["pll"] = constants.ERROR_MODEL_NOT_SUPPORTED
            temperature_metrics["pmic"] = constants.ERROR_MODEL_NOT_SUPPORTED
            temperature_metrics["fan"] = constants.ERROR_MODEL_NOT_SUPPORTED

            return temperature_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_temperature_metrics(temperature_metrics)

    def get_network_interfaces(self):
        network_interfaces = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            network_interfaces["error"] = True
            network_interfaces["available_networks"] = []
            return network_interfaces

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_network_interfaces(network_interfaces)

    def get_network_metrics(self):
        network_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            network_metrics["error"] = True
            network_metrics["rx"] = constants.ERROR_MODEL_NOT_SUPPORTED
            network_metrics["tx"] = constants.ERROR_MODEL_NOT_SUPPORTED
            return network_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_network_metrics(network_metrics, self.network_interfaces)

if __name__ == '__main__':
    energon = Energon()
    detected_model = energon.detected_model
    n_core = energon.n_cores
    network_interfaces = energon.network_interfaces
    energy_metrics = energon.get_energy_metrics()
    cpu_frequency_metrics = energon.get_cpu_frequency_metrics()
    cpu_load_metrics = energon.get_cpu_load_metrics()
    storage_metrics = energon.get_storage_metrics()
    ram_metrics = energon.get_ram_metrics()
    gpu_load = energon.get_gpu_load()
    temperature_metrics = energon.get_temperature_metrics()
    network_metrics = energon.get_network_metrics()

    print("detected_model: ", detected_model)
    print("n_core: ", n_core)
    print("network_interfaces: ", network_interfaces)
    print("energy_metrics: ", energy_metrics)
    print("cpu_frequency_metrics: ", cpu_frequency_metrics)
    print("cpu_load_metrics: ", cpu_load_metrics)
    print("storage_metrics: ", storage_metrics)
    print("ram_metrics: ", ram_metrics)
    print("gpu_load: ", gpu_load)
    print("temperature_metrics: ", temperature_metrics)
    print("network_metrics: ", network_metrics)
