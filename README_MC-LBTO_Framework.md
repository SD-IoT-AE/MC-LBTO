
# 🧠 MC-LBTO: A State-Aware Multi-Controller Framework for Adaptive Traffic Optimization and Intelligent Load Balancing in SD-IoT

This repository hosts the full deployment guide and implementation breakdown for the **MC-LBTO** framework, which includes three interdependent modules:

- **PDSM**: P4-based Dynamic State Monitoring
- **STAM**: Secure Trusted Adaptive Multi-Control
- **PALB**: P4 Adaptive Load Balancer

---

## 📦 Framework Modules

---

### 🔍 1. PDSM Module – Dynamic Monitoring

**Directory**: `mc-lbto/`  
**Core File**: `pdsm.p4`

#### Overview:
Tracks real-time flow state using in-switch logic and reports to STAM for controller decisions.

#### Deployment:

```bash
sudo apt update
sudo apt install -y mininet iperf python3-pip
pip3 install grpcio grpcio-tools protobuf p4runtime_lib
chmod +x launch_all.sh
sudo ./launch_all.sh
```

#### Topology & Scripts:
- `topo.py`: 1 switch, 2 hosts
- `control.py`: P4Runtime controller
- `stam_listener.py`: Receives digests from switch
- `traffic_generator.py`: Sends test flows

#### Output:
- Runtime logs, flow digests, and register counters

---

### 🔐 2. STAM Module – Secure Trusted Adaptive Multi-Control

**Directory**: `stam/`  
**Core Files**: `stam_controller.py`, `STAMController.java`

#### Overview:
Processes metrics from PDSM and coordinates adaptive control over PALB using secure TCC.

#### Deployment:

**Python:**

```bash
python3 stam_controller.py
```

**Java:**

```bash
javac STAMController.java
java stam.STAMController
```

#### Configuration:

- Python: `stam_config.json`
- Java: `stam_config_java.properties`

#### Dynamic Triggers:

| Condition                 | Action                                 |
|--------------------------|----------------------------------------|
| High traffic             | Throttle update rate                   |
| Delay spikes             | Reroute via PALB                       |
| Congestion alerts        | Broadcast coordination                 |
| Controller overload      | Rebalance load                         |

---

### 🧠 3. PALB Module – Adaptive Load Balancer

**Directory**: `palb/`  
**Core File**: `palb.p4`

#### Overview:
Distributes flows using a P4-based PAWR mechanism with input from STAM and server feedback.

#### Deployment:

```bash
sudo apt install mininet python3-pip
pip3 install grpcio grpcio-tools protobuf
p4c --target bmv2 --arch v1model -o build palb.p4
sudo python3 topo_palb.py
python3 server_monitor.py
python3 control_palb.py
sudo python3 traffic_test_palb.py
```

#### Performance Metrics:

| Metric                   | PALB Value | Baseline |
|--------------------------|------------|----------|
| Avg Request Latency      | 16ms       | 25ms     |
| Network Throughput       | 920 Mbps   | 830 Mbps |
| Load Variance            | 5.5%       | >13%     |
| Packet Loss              | 2.2%       | >6.5%    |

#### Configurable:

- Servers defined in `palb_config.json`

---

## 🔗 Module Interactions

- **PDSM → STAM**: Digest alerts about delay/congestion
- **STAM → PALB**: Policy updates via secure TCC
- **PALB**: Applies flow rerouting and weight changes

---

## 🧪 Test the Full Stack

1. Run `PDSM`: monitors & emits alerts
2. Launch `STAM`: processes alerts, adapts policy
3. Execute `PALB`: load balances based on STAM input

---

## 📞 Contact

For questions, integration advice, or extending the gRPC channels, contact the MC-LBTO authors.

Please refer to the following single README files for the modules in the main repository:

1- README - PDSM Module Deployment Manual
2- README - PALB Module Deployment Manual
3- README - STAM Module Deployment Manual

---

Happy Testing!

---