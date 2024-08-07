<table>
    <tr>
        <td>
            <h1>Energon_Prometheus_exporter</h1>
        </td>
        <td>
            <img style="margin-left:1rem;" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Prometheus_software_logo.svg/1200px-Prometheus_software_logo.svg.png"  width="10%">
        </td>
    </tr>
</table>

Energon is a Prometheus [https://prometheus.io/] compliant system monitoring tools, it focuses on the energy consumption and resource usage in constrained devices but it integrates reporting tools for desktop machine, too.

## Currently supported models:

- Jetson Nano Dev Kit [here](https://developer.nvidia.com/embedded/jetson-nano-developer-kit);
- Jetson Orin Nano Dev Kit [here](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit);
- Jetson Xavier NX Dev Kit [here](https://developer.nvidia.com/embedded/learn/get-started-jetson-xavier-nx-devkit); 
- Jetson Xavier NX Seed Studio [here](https://www.seeedstudio.com/Jetson-20-1-H1-p-5328.html);
- Jetson Orin Dev Kit [here](https://developer.nvidia.com/embedded/learn/jetson-agx-orin-devkit-user-guide/index.html);
- USB Tester UM25C USB Meter Tester [here](https://www.amazon.com/Bluetooth-Voltmeter-Multimeter-Resistance-Impedance/dp/B07PZRSYXD);
- Linux x86 architecture based systems.

### Screenshots:
![Energon Grafana Dashboard](https://raw.githubusercontent.com/MatteoMendula/Energon_Prometheus_exporter/main/images/energon_screen1.png)
![Energon Grafana Dashboard](https://raw.githubusercontent.com/MatteoMendula/Energon_Prometheus_exporter/main/images/energon_screen2.png)

### Usage:

#### From the repository
- Install prometheus [https://prometheus.io/docs/prometheus/latest/installation/];
- Download this repository: ``` git clone git@github.com:MatteoMendula/Energon_Prometheus_exporter.git ```
- Install required python packages: ``` pip3 install -r requirements.txt ```;
- Run: ``` sudo python3 energon.py ``` for running a single metric scan;
- Run: ``` sudo python3 prometheus_exporter.py ``` for running the prometheus exporter on default port 9877;

#### With pip install
- ``` pip3 install Energon-Prometheus-exporter ```;
``` 
from energon_prometheus_exporter.prometheus_exporter import EnergonPrometheusExporter 
server_exporter = EnergonPrometheusExporter(DESIRED_PORT)
server_exporter.run()
```

The application requires sudo privileges to access to some system files.
You can still run the application without sudo privileges but some metrics will not be available.

## Currently supported features:
All metrics names are compliat with prometheus specifications as described in [https://prometheus.io/docs/practices/naming/].

### Energy metrics:
- energon_device_info: device information;
- energon_total_in_power_mW: current total power consumption in milliwatts;
- energon_cpu_in_power_mW: current cpu power consumption in milliwatts;
- energon_gpu_in_power_mW: current gpu power consumption in milliwatts;
- energon_total_in_voltage_mV: current total voltage in millivolts;
- energon_cpu_in_voltage_mV: current cpu voltage in millivolts;
- energon_gpu_in_voltage_mV: current gpu voltage in millivolts;
- energon_battery_percentage: current battery percentage.

### USB Tester UM25C USB Meter Tester metrics:
N.B. Only if real sensor is connected!
- energon_total_actual_watts: total actual power consumption in watts;
- energon_total_actual_volts: total actual voltage in volts;
- energon_total_actual_amps: total actual current in amps.

### Network metrics:
For each interface_name
- energon_network_metrics_[interface_name]_rx_packets: received packets;
- energon_network_metrics_[interface_name]_rx_bytes: received bytes;
- energon_network_metrics_[interface_name]_rx_errors: received errors;
- energon_network_metrics_[interface_name]_rx_dropped: received dropped packets;
- energon_network_metrics_[interface_name]_tx_packets: transmitted packets;
- energon_network_metrics_[interface_name]_tx_bytes: trasmitted bytes;
- energon_network_metrics_[interface_name]_tx_errors: transmitted errors;
- energon_network_metrics_[interface_name]_tx_dropped: transmitted dropped packets.
Mainly for wifi interfaces
- energon_network_quality_[interface_name]_link_quality_x_over_70: link quality x/70 for interface [interface_name];
- energon_network_quality_[interface_name]_signal_level_dBm: signal level in dBm for interface [interface_name];
- energon_network_quality_[interface_name]_bit_rate_Mbs: bit rate in Mbs for interface [interface_name].

### Cpu usage:
For each core_number
- energon_cpu_[core_number]_MHz: cpu frequency in MHz for core [core_number];
- energon_cpu_[core_number]_usage_percentage: CPU usage as % for core [core_number].
Total
- energon_cpu_total_usage_percentage: total CPU usage as %.

### Storage:
For each available [storage_device]
- energon_storage_[storage_device]_total_bytes: total bytes for storage [storage_device];
- energon_storage_[storage_device]_used_bytes: used bytes for storage [storage_device];
- energon_storage_[storage_device]_available_bytes: available bytes for storage [storage_device];
- energon_storage_[storage_device]_percent_used_percentage: storage usage percentage for storage [storage_device].
Total
- energon_storage_total_bytes: total storage in bytes;
- energon_storage_used_bytes: total used storage in bytes;
- energon_storage_available_bytes: total available storage in bytes;
- energon_storage_percent_used_percentage: Storage usage percentage.

### Ram usage:
- energon_ram_total_bytes: total ram in bytes;
- energon_ram_used_bytes: total used ram in bytes;
- energon_ram_available_bytes: total available ram in bytes;
- energon_ram_used_percentage: ram usage percentage.

### GPU metrics:
- energon_gpu_total_usage_percentage: total GPU usage as %.

### Temperature metrics:
For each available [temperature_sensor]
- energon_temperature_[temperature_sensor]_mC: temperature in milliCelsius for sensor [temperature_sensor].



