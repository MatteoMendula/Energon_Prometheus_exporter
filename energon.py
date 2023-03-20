import utils
import constants

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
            return self.get_jetson_nano_dev_kit_energy_metrics(energy_metrics)
        
    def get_jetson_nano_dev_kit_energy_metrics(energy_metrics):
        out_tot_energy = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_power0_input")
        out_cpu_energy = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_power1_input")
        out_gpu_energy = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_power2_input")
        
        energy_metrics["error"] = out_tot_energy["error"] or out_cpu_energy["error"] or out_gpu_energy["error"]

        energy_metrics["total"] = out_tot_energy["out_value"]
        energy_metrics["cpu"] = out_cpu_energy["out_value"]
        energy_metrics["gpu"] = out_gpu_energy["out_value"]
        
        return energy_metrics



if __name__ == '__main__':
    energon = Energon()
    detected_model = energon.detected_model
    energy_metrics = energon.get_energy_metrics()
    print("detected_model: ", detected_model)
    print("energy_metrics: ", energy_metrics)
