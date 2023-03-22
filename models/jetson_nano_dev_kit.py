import utils
import time

def get_jetson_nano_dev_kit_energy_metrics(energy_metrics):
    out_tot_energy = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_power0_input")
    out_cpu_energy = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_power1_input")
    out_gpu_energy = utils.run_command_and_get_output("cat /sys/bus/i2c/drivers/ina3221x/6-0040/iio:device0/in_power2_input")
    
    energy_metrics["error"] = out_tot_energy["error"] or out_cpu_energy["error"] or out_gpu_energy["error"]

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
    
    _cpu_load_1 = utils.run_command_and_get_output("cat /proc/stat")
    cpu_load_metrics["error"] = False
    if cpu_load_metrics["error"] == True:
        cpu_load_metrics["out_value"] = _cpu_load_1["out_value"]
        return cpu_load_metrics

    def get_idle_and_total_cpu_load(proc_stat_out_value):
        matched_lines = [line for line in proc_stat_out_value.split('\n') if line.startswith("cpu")]
        
        cpu_load_metrics_tot = [utils.parseToFloat(amount) for amount in matched_lines[0].split()]
        cpu_load_metrics_core_0 = [utils.parseToFloat(amount) for amount in matched_lines[0].split()]
        cpu_load_metrics_core_1 = [utils.parseToFloat(amount) for amount in matched_lines[1].split()]
        cpu_load_metrics_core_2 = [utils.parseToFloat(amount) for amount in matched_lines[2].split()]
        cpu_load_metrics_core_3 = [utils.parseToFloat(amount) for amount in matched_lines[3].split()]

        idle_tot = cpu_load_metrics_tot[4]
        idle_core_0 = cpu_load_metrics_core_0[4]
        idle_core_1 = cpu_load_metrics_core_1[4]
        idle_core_2 = cpu_load_metrics_core_2[4]
        idle_core_3 = cpu_load_metrics_core_3[4]

        total_tot = sum(cpu_load_metrics_tot[1:])
        total_core_0 = sum(cpu_load_metrics_core_0[1:])
        total_core_1 = sum(cpu_load_metrics_core_1[1:])
        total_core_2 = sum(cpu_load_metrics_core_2[1:])
        total_core_3 = sum(cpu_load_metrics_core_3[1:])

        return {
            "idle": {"total": idle_tot, "core_0": idle_core_0, "core_1": idle_core_1, "core_2": idle_core_2, "core_3": idle_core_3},
            "total": {"total": total_tot, "core_0": total_core_0, "core_1": total_core_1, "core_2": total_core_2, "core_3": total_core_3}
        }
        
    first_read = get_idle_and_total_cpu_load(_cpu_load_1["out_value"])

    time.sleep(1)

    _cpu_load_2 = utils.run_command_and_get_output("cat /proc/stat")
    cpu_load_metrics["error"] = False
    if cpu_load_metrics["error"] == True:
        cpu_load_metrics["out_value"] = _cpu_load_2["out_value"]
        return cpu_load_metrics
    
    second_read = get_idle_and_total_cpu_load(_cpu_load_2["out_value"])

    return {
        "total": (1 - (second_read["idle"]["total"] - first_read["idle"]["total"]) / (second_read["total"]["total"] - first_read["total"]["total"])) * 100,
        "core_0": (1 - (second_read["idle"]["core_0"] - first_read["idle"]["core_0"]) / (second_read["total"]["core_0"] - first_read["total"]["core_0"])) * 100,
        "core_1": (1 - (second_read["idle"]["core_1"] - first_read["idle"]["core_1"]) / (second_read["total"]["core_1"] - first_read["total"]["core_1"])) * 100,
        "core_2": (1 - (second_read["idle"]["core_2"] - first_read["idle"]["core_2"]) / (second_read["total"]["core_2"] - first_read["total"]["core_2"])) * 100,
        "core_3": (1 - (second_read["idle"]["core_3"] - first_read["idle"]["core_3"]) / (second_read["total"]["core_3"] - first_read["total"]["core_3"])) * 100
    }

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
    storage_metrics["usage_percentage"] = 0

    for line in matched_lines:
        # keeping track of all storage devices
        storage_metrics["devices"][line.split()[0]] = {}
        storage_metrics["devices"][line.split()[0]]["total"] = utils.parseToFloat(line.split()[1])
        storage_metrics["devices"][line.split()[0]]["used"] = utils.parseToFloat(line.split()[2])
        storage_metrics["devices"][line.split()[0]]["available"] = utils.parseToFloat(line.split()[3])
        storage_metrics["devices"][line.split()[0]]["usage_percentage"] = (storage_metrics["devices"][line.split()[0]]["used"] / storage_metrics["devices"][line.split()[0]]["total"]) * 100

        # summing up all available storage
        storage_metrics["total"] = storage_metrics["total"] + utils.parseToFloat(line.split()[1])
        storage_metrics["used"] = storage_metrics["used"] + utils.parseToFloat(line.split()[2])
        storage_metrics["available"] = storage_metrics["available"] + utils.parseToFloat(line.split()[3])
        storage_metrics["usage_percentage"] = (storage_metrics["used"] / storage_metrics["total"]) * 100

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
    ram_metrics["usage_percentage"] = (ram_metrics["used"] / ram_metrics["total"]) * 100

    return ram_metrics

def get_jetson_nano_dev_kit_gpu_metrics(gpu_metrics):

    gpu_load_possible_commands = [ "cat /sys/devices/57000000.gpu/load", "cat /sys/devices/gpu.0/load", "cat /sys/devices/platform/host1x/57000000.gpu/load" ]

    _gpu_command_output = None

    for command in gpu_load_possible_commands:
        _gpu_command_output = utils.run_command_and_get_output(command)
        if _gpu_command_output["error"] == False:
            break

    # if all commands failed, return last error
    gpu_metrics["error"] = _gpu_command_output["error"]
    if gpu_metrics["error"] == True:
        gpu_metrics["usage"] = _gpu_command_output["out_value"]
        return gpu_metrics
    
    gpu_metrics["usage"] = utils.parseToFloat(_gpu_command_output["out_value"])

    return gpu_metrics

def get_jetson_nano_dev_kit_temperature_metrics(temperature_metrics):
    ao = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone0/temp")
    cpu = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone1/temp")
    gpu = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone2/temp")
    pll = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone3/temp")
    pmic = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone4/temp")
    fan = utils.run_command_and_get_output("cat /sys/devices/virtual/thermal/thermal_zone5/temp")

    temperature_metrics["error"] = ao["error"] or cpu["error"] or gpu["error"] or pll["error"] or pmic["error"] or fan["error"]
    
    temperature_metrics["ao"] = utils.parseToFloat(ao["out_value"])
    temperature_metrics["cpu"] = utils.parseToFloat(cpu["out_value"])
    temperature_metrics["gpu"] = utils.parseToFloat(gpu["out_value"])
    temperature_metrics["pll"] = utils.parseToFloat(pll["out_value"])
    temperature_metrics["pmic"] = utils.parseToFloat(pmic["out_value"])
    temperature_metrics["fan"] = utils.parseToFloat(fan["out_value"])

    return temperature_metrics

def get_jetson_nano_dev_kit_network_interfaces(network_interfaces):
    _network_interfaces = utils.run_command_and_get_output("ls /sys/class/net/")

    network_interfaces["error"] = _network_interfaces["error"]
    if network_interfaces["error"] == True:
        network_interfaces["out_value"] = _network_interfaces["out_value"]
        return network_interfaces
    
    network_interfaces["available_networks"] = _network_interfaces["out_value"].split()

    return network_interfaces

def get_jetson_nano_dev_kit_network_metrics(network_metrics, network_interfaces):
    errors_list = []
    for interface in network_interfaces:
        rx_packets = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/rx_packets")
        tx_packets = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/tx_packets")
        rx_bytes = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/rx_bytes")
        tx_bytes = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/tx_bytes")
        rx_errors = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/rx_errors")
        tx_errors = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/tx_errors")
        rx_dropped = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/rx_dropped")
        tx_dropped = utils.run_command_and_get_output("cat /sys/class/net/" + interface + "/statistics/tx_dropped")

        errors_list.append(rx_packets["error"])
        errors_list.append(tx_packets["error"])
        errors_list.append(rx_bytes["error"])
        errors_list.append(tx_bytes["error"])
        errors_list.append(rx_errors["error"])
        errors_list.append(tx_errors["error"])
        errors_list.append(rx_dropped["error"])
        errors_list.append(tx_dropped["error"])

        network_metrics[interface] = {}
        network_metrics[interface]["rx_packets"] = utils.parseToFloat(rx_packets["out_value"])
        network_metrics[interface]["tx_packets"] = utils.parseToFloat(tx_packets["out_value"])
        network_metrics[interface]["rx_bytes"] = utils.parseToFloat(rx_bytes["out_value"])
        network_metrics[interface]["tx_bytes"] = utils.parseToFloat(tx_bytes["out_value"])
        network_metrics[interface]["rx_errors"] = utils.parseToFloat(rx_errors["out_value"])
        network_metrics[interface]["tx_errors"] = utils.parseToFloat(tx_errors["out_value"])
        network_metrics[interface]["rx_dropped"] = utils.parseToFloat(rx_dropped["out_value"])
        network_metrics[interface]["tx_dropped"] = utils.parseToFloat(tx_dropped["out_value"])

    network_metrics["error"] = any(errors_list)

    return network_metrics