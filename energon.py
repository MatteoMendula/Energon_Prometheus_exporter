import utils
import constants
from models import jetson_nano_dev_kit

class Energon:
    def __init__(self):
        self.name = 'Energon Prometheus Exporter'
        self.version = '0.0.1'
        self.detected_model = self.detect_model()

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
            energy_metrics["error"] = False
            energy_metrics["total"] = "Error: Model not supported"
            energy_metrics["cpu"] = "Error: Model not supported"
            energy_metrics["gpu"] = "Error: Model not supported"
            return energy_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_energy_metrics(energy_metrics)
        
    def get_cpu_frequency_metrics(self):
        cpu_frquency_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            cpu_frquency_metrics["error"] = False
            cpu_frquency_metrics["core_0"] = "Error: Model not supported"
            cpu_frquency_metrics["core_1"] = "Error: Model not supported"
            cpu_frquency_metrics["core_2"] = "Error: Model not supported"
            cpu_frquency_metrics["core_3"] = "Error: Model not supported"
            return cpu_frquency_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_cpu_frequency(cpu_frquency_metrics)
        
    def get_cpu_load_metrics(self):
        cpu_load_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            cpu_load_metrics["error"] = False
            cpu_load_metrics["total"] = "Error: Model not supported"
            cpu_load_metrics["core_0"] = "Error: Model not supported"
            cpu_load_metrics["core_1"] = "Error: Model not supported"
            cpu_load_metrics["core_2"] = "Error: Model not supported"
            cpu_load_metrics["core_3"] = "Error: Model not supported"
            return cpu_load_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_cpu_load_percentage(cpu_load_metrics)

    def n_proc(self):
        n_proc = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            n_proc["error"] = False
            n_proc["n_cpus"] = "Error: Model not supported"
            return n_proc

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_n_cpus(n_proc)

    def get_storage_metrics(self):
        storage_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            storage_metrics["error"] = False
            storage_metrics["total"] = "Error: Model not supported"
            storage_metrics["used"] = "Error: Model not supported"
            storage_metrics["available"] = "Error: Model not supported"
            return storage_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_storage_metrics(storage_metrics)
        
    def get_ram_metrics(self):
        ram_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            ram_metrics["error"] = False
            ram_metrics["total"] = "Error: Model not supported"
            ram_metrics["free"] = "Error: Model not supported"
            ram_metrics["available"] = "Error: Model not supported"
            return ram_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_ram_metrics(ram_metrics)
        
    def get_gpu_load(self):
        gpu_load = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            gpu_load["error"] = False
            gpu_load["total"] = "Error: Model not supported"
            return gpu_load

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_gpu_metrics(gpu_load)
        
    def get_temperature_metrics(self):
        temperature_metrics = {}

        if not self.detected_model in constants.COMPLIANT_MODELS:
            temperature_metrics["error"] = False
            temperature_metrics["ao"] = "Error: Model not supported"
            temperature_metrics["cpu"] = "Error: Model not supported"
            temperature_metrics["gpu"] = "Error: Model not supported"
            temperature_metrics["pll"] = "Error: Model not supported"
            temperature_metrics["pmic"] = "Error: Model not supported"
            temperature_metrics["fan"] = "Error: Model not supported"

            return temperature_metrics

        # ----------------- JETSON_NANO_DEV_KIT -----------------
        if self.detected_model == constants.JETSON_NANO_DEV_KIT:
            return jetson_nano_dev_kit.get_jetson_nano_dev_kit_temperature_metrics(temperature_metrics)

if __name__ == '__main__':
    energon = Energon()
    detected_model = energon.detected_model
    energy_metrics = energon.get_energy_metrics()
    cpu_frequency_metrics = energon.get_cpu_frequency_metrics()
    cpu_load_metrics = energon.get_cpu_load_metrics()
    n_proc = energon.n_proc()
    storage_metrics = energon.get_storage_metrics()
    ram_metrics = energon.get_ram_metrics()
    gpu_load = energon.get_gpu_load()
    temperature_metrics = energon.get_temperature_metrics()
    print("detected_model: ", detected_model)
    print("energy_metrics: ", energy_metrics)
    print("cpu_frequency_metrics: ", cpu_frequency_metrics)
    print("cpu_load_metrics: ", cpu_load_metrics)
    print("n_proc: ", n_proc)
    print("storage_metrics: ", storage_metrics)
    print("ram_metrics: ", ram_metrics)
    print("gpu_load: ", gpu_load)
    print("temperature_metrics: ", temperature_metrics)
