# MC-LBTO: PDSM Module Deployment Manual

This guide documents the deployment and testing process of the **PDSM (P4-based Dynamic State Monitoring)** module from the MC-LBTO framework. It walks through installation, setup, and execution of a complete emulated environment using Mininet, BMv2, and P4Runtime.

---

## 📁 Directory Structure

```
mc-lbto/
├── pdsm.p4               # P4 program for in-switch monitoring
├── control.py            # P4Runtime control app to read counters & receive digests
├── stam_listener.py      # STAM digest listener service
├── topo.py               # Mininet topology script
├── traffic_generator.py  # Test traffic generator using iperf
├── launch_all.sh         # Unified launcher script
└── build/                # Compiled P4 JSON and p4info files
```

---

## 🛠 Prerequisites

- **Ubuntu 20.04+**
- **P4 toolchain**
  - `p4c`, `p4runtime-shell`, `simple_switch_grpc`
- **Python3 + pip**
  - `mininet`, `grpcio`, `protobuf`, `p4runtime_lib`
- **Mininet + BMv2**
- **iperf** for traffic generation

### 🔧 Install Key Dependencies:
```bash
sudo apt update
sudo apt install -y mininet iperf python3-pip
pip3 install grpcio grpcio-tools protobuf p4runtime_lib
```

---

## 🚀 Deployment Steps

### 1. Make Sure Your Files Are In Place:
```bash
cd mc-lbto/
```

### 2. Run the Unified Launcher
```bash
chmod +x launch_all.sh
sudo ./launch_all.sh
```
This will:
- Compile the P4 source
- Launch the BMv2 switch
- Start the STAM digest listener
- Start the Mininet topology
- Run the control plane app
- Send test TCP/UDP traffic

---

## 🔍 Components Overview

### `pdsm.p4`
Implements:
- Flow state tracking using 5-tuple hashing
- Registers for packet/byte counters and timestamps
- Digest generation for idle flows

### `control.py`
- Uses P4Runtime to connect to the BMv2 switch
- Periodically reads register values
- Handles digest messages from the switch
- Sends flow events to STAM

### `stam_listener.py`
- Listens on TCP port `9090`
- Accepts and logs flow digests in JSON format

### `topo.py`
- Defines a basic 1-switch, 2-host Mininet topology

### `traffic_generator.py`
- Sends UDP and TCP traffic between `h1` and `h2`
- Uses `iperf` for throughput simulation

---

## 📦 Logs & Output
- P4Runtime messages: `logs/s1-p4runtime-requests.log`
- Console: printed flow digests and counters
- Digests: printed in `stam_listener.py` terminal

---

## 🧼 Cleanup
Use `CTRL+C` in the `launch_all.sh` process to shut down everything cleanly. You can also run:
```bash
sudo mn -c
```
to remove Mininet remnants.

---

## 📌 Notes for Extension
- Modify the `digest` threshold in `pdsm.p4` for custom detection logic
- Extend `stam_listener.py` to push events to a database, MQTT, or external controller
- Integrate `PALB` or `STAM` modules for full MC-LBTO stack

---


---

Happy testing!

---

