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

    cpu_frequency_metrics["core_0"] = utils.parseToFloat(core_0["out_value"])
    cpu_frequency_metrics["core_1"] = utils.parseToFloat(core_1["out_value"])
    cpu_frequency_metrics["core_2"] = utils.parseToFloat(core_2["out_value"])
    cpu_frequency_metrics["core_3"] = utils.parseToFloat(core_3["out_value"])

    return cpu_frequency_metrics

def get_jetson_nano_dev_kit_cpu_load_percentage(cpu_load_metrics):
    _cpu_load = utils.run_command_and_get_output("cat /proc/stat")
    cpu_load_metrics["error"] = False

    if cpu_load_metrics["error"] == True:
        cpu_load_metrics["out_value"] = _cpu_load["out_value"]
        return cpu_load_metrics
    
    matched_lines = [utils.parseToFloat(line) for line in cpu_load_metrics["out_value"].split('\n') if line.startswith("cpu")]
    cpu_load_metrics_tot = [utils.parseToFloat(amount) for amount in matched_lines[0].split()]
    cpu_load_metrics_core_0 = [utils.parseToFloat(amount) for amount in matched_lines[0].split()]
    cpu_load_metrics_core_1 = [utils.parseToFloat(amount) for amount in matched_lines[1].split()]
    cpu_load_metrics_core_2 = [utils.parseToFloat(amount) for amount in matched_lines[2].split()]
    cpu_load_metrics_core_3 = [utils.parseToFloat(amount) for amount in matched_lines[3].split()]

    cpu_load_metrics["total"] = sum(cpu_load_metrics_tot[2:]) / cpu_load_metrics_tot[5]
    cpu_load_metrics["core_0"] = sum(cpu_load_metrics_core_0[2:]) / cpu_load_metrics_core_0[5]
    cpu_load_metrics["core_1"] = sum(cpu_load_metrics_core_1[2:]) / cpu_load_metrics_core_1[5]
    cpu_load_metrics["core_2"] = sum(cpu_load_metrics_core_2[2:]) / cpu_load_metrics_core_2[5]
    cpu_load_metrics["core_3"] = sum(cpu_load_metrics_core_3[2:]) / cpu_load_metrics_core_3[5]

    return cpu_load_metrics

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

def get_jetson_nano_dev_kit_ram_metrics(ram_metrics):
    _ram_metrics = utils.run_command_and_get_output("cat /proc/meminfo")
    ram_metrics["error"] = _ram_metrics["error"]

    if ram_metrics["error"] == True:
        ram_metrics["out_value"] = _ram_metrics["out_value"]
        return ram_metrics
    
    matched_lines = [line for line in _ram_metrics["out_value"].split('\n') if line.startswith("Mem")]
    ram_metrics["total"] = utils.parseToFloat(matched_lines[0].split()[1])
    ram_metrics["used"] = utils.parseToFloat(matched_lines[1].split()[1])
    ram_metrics["available"] = utils.parseToFloat(matched_lines[2].split()[1])

    return ram_metrics