import utils

def get_jetson_nano_dev_kit_energy_metrics(energy_metrics):
    out_tot_energy = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_power0_input")
    out_cpu_energy = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_power1_input")
    out_gpu_energy = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_power2_input")
    
    energy_metrics["error"] = out_tot_energy["error"] or out_cpu_energy["error"] or out_gpu_energy["error"]

    print("out_tot_energy", out_tot_energy)

    energy_metrics["total"] = utils.parseToFloat(out_tot_energy["out_value"])
    energy_metrics["cpu"] = utils.parseToFloat(out_cpu_energy["out_value"])
    energy_metrics["gpu"] = utils.parseToFloat(out_gpu_energy["out_value"])
    
    return energy_metrics

def get_jetson_nano_dev_kit_cpu_frequency(cpu_frequency_metrics):
    core_0 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq")
    core_1 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu1/cpufreq/cpuinfo_cur_freq")
    core_2 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_cur_freq")
    core_3 = utils.run_command_and_get_output("cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_cur_freq")

    cpu_frequency_metrics["error"] = core_0["error"] or core_1["error"] or core_2["error"] or core_3["error"]

    cpu_frequency_metrics["total"] = utils.parseToFloat(core_0["out_value"])
    cpu_frequency_metrics["core_0"] = utils.parseToFloat(core_1["out_value"])
    cpu_frequency_metrics["core_1"] = utils.parseToFloat(core_2["out_value"])
    cpu_frequency_metrics["core_2"] = utils.parseToFloat(core_3["out_value"])
    cpu_frequency_metrics["core_3"] = utils.parseToFloat(core_3["out_value"])

    return cpu_frequency_metrics

def get_jetson_nano_dev_kit_n_cpus(n_proc):
    _n_proc = utils.run_command_and_get_output("nproc")
    n_proc["error"] = _n_proc["error"]
    return utils.parseToFloat(_n_proc["out_value"])

def get_jetson_nano_dev_kit_storage_metrics(storage_metrics):
    _storage_metrics = utils.run_command_and_get_output("df -h /")
    storage_metrics["error"] = _storage_metrics["error"]

    if storage_metrics["error"] == True:
        storage_metrics["out_value"] = _storage_metrics["out_value"]
        return storage_metrics
    
    matched_lines = [line for line in _storage_metrics["out_value"].split('\n') if line.startswith("/dev")]
    storage_metrics["devices"] = {}
    storage_metrics["total"] = 0
    storage_metrics["used"] = 0
    storage_metrics["available"] = 0

    for line in matched_lines:
        # keeping track of all storage devices
        storage_metrics["devices"][line.split()[0]] = {}
        storage_metrics["devices"][line.split()[0]]["total"] = utils.parseToFloat(line.split()[1])
        storage_metrics["devices"][line.split()[0]]["used"] = utils.parseToFloat(line.split()[2])
        storage_metrics["devices"][line.split()[0]]["available"] = utils.parseToFloat(line.split()[3])

        # summing up all available storage
        storage_metrics["total"] = storage_metrics["total"] + utils.parseToFloat(line.split()[1])
        storage_metrics["used"] = storage_metrics["used"] + utils.parseToFloat(line.split()[2])
        storage_metrics["available"] = storage_metrics["available"] + utils.parseToFloat(line.split()[3])

    return storage_metrics