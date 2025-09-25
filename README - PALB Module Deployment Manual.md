
# 🧠 PALB: P4 Adaptive Load Balancer

## 📚 Overview

PALB is the P4-based Adaptive Load Balancing module within the **MC-LBTO** framework, designed for Software-Defined IoT (SD-IoT) networks. It uses real-time network state data and adaptive policies to intelligently distribute traffic among multiple backend servers with fairness, low latency, and high throughput.

- **Module Name:** `PALB`
- **Core Technique:** PAWR (P4 Adaptive Weighted Round-Robin)
- **Dependencies:** Mininet, BMv2, P4Runtime, gRPC

---

## 📁 Directory Structure

```bash
palb/
├── palb.p4                  # P4 program for server selection and forwarding
├── server_monitor.py        # Dynamically monitors servers and updates weights
├── control_palb.py          # CLI tool to read/write P4 registers (flow maps, weights)
├── palb_config.json         # Initial server list, status, and base weights
├── topo_palb.py             # Mininet topology: 1 client, 1 LB switch, N servers
├── traffic_test_palb.py     # Traffic generator to simulate client load
└── README.md                # This documentation
```

---

## 🔧 Setup Instructions

### 1. Install Requirements

```bash
sudo apt install mininet python3-pip
pip3 install grpcio grpcio-tools protobuf
```

Ensure you have P4 toolchain:

```bash
p4c --version  # Should output P4 compiler version
```

### 2. Compile the P4 Program

```bash
p4c --target bmv2 --arch v1model -o build palb.p4
```

### 3. Launch the Topology

```bash
sudo python3 topo_palb.py
```

This creates:

- `h1` (client)
- `s1` (load balancing switch)
- `h2` to `h5` (servers)

---

## 🚦 Runtime Execution

### Start the Server Monitor (updates server weights)

```bash
python3 server_monitor.py
```

This script:

- Simulates resource usage (e.g., CPU, queue depth)
- Updates `server_weights[]` register via gRPC

### Start the Control App (monitor registers)

```bash
python3 control_palb.py
```

Inspect:

- `flow_to_server[]` mapping
- `server_weights[]` register values

### Start the Traffic Generator

```bash
sudo python3 traffic_test_palb.py
```

This:

- Launches `iperf` servers on `h2`–`h5`
- Simulates multiple client sessions from `h1`

---

## 📊 Performance Highlights (from MC-LBTO Paper)

| Metric                   | PALB (PAWR) Value | Baseline Best |
|--------------------------|-------------------|----------------|
| Avg Request Latency      | 16ms              | 25ms (RR)      |
| Network Throughput       | 920 Mbps          | 830 Mbps       |
| Load Distribution Variance | 5.5%           | >13% others    |
| Packet Loss Ratio        | 2.2%              | >6.5% others   |
| Control Plane Overhead   | <1 op/sec         | 5–15 op/sec    |

---

## ⚙ Configuration

Modify `palb_config.json` to adjust:

```json
{
  "servers": [
    {"id": 0, "ip": "10.0.0.2", "mac": "00:00:00:00:00:02", "port": 2},
    {"id": 1, "ip": "10.0.0.3", "mac": "00:00:00:00:00:03", "port": 3}
  ]
}
```

Add more servers as needed. Ensure `server_monitor.py` and `control_palb.py` match this config.

---

## 📌 Notes

- Register arrays used:
  - `server_weights[]` – updated via `server_monitor.py`
  - `flow_to_server[]` – populated dynamically
- Uses hash of client flow ID for fairness
- Digest messaging available for controller alerts (not enabled by default)

---

## 🔐 Part of the MC-LBTO Framework

For full framework benefits (security, multi-controller sync):

- Integrate with **PDSM** (monitoring)
- Connect to **STAM** (secure multi-controller coordination)

---

## 🧪 Testing Tips

From Mininet CLI:

```bash
h1 ping h2
h1 iperf -c 10.0.0.2 -t 10
```

Or run automated:

```bash
sudo python3 traffic_test_palb.py
```

Then monitor flow distribution:

```bash
python3 control_palb.py
```

---

Good Luck!

---