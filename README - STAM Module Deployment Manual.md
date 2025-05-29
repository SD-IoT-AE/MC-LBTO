
# 🔐 STAM: Secure Trusted Adaptive Multi-Control Module

## 📚 Overview

The **STAM module** ensures secure, adaptive coordination between multiple distributed SDN controllers in the MC-LBTO framework for SD-IoT networks. It processes real-time network metrics from the **PDSM** module and enforces adaptive policy actions that dynamically influence **PALB** for traffic distribution.

> **Key Features:**
> - Secure controller authentication  
> - Trusted Communication Channel (TCC) setup  
> - Adaptive controller coordination based on network metrics  
> - Python & Java implementations for flexibility  

---

## 📁 Directory Structure

```
stam/
├── stam_controller.py               # Python-based STAM controller logic
├── STAMController.java              # Java-based STAM controller logic
├── stam_config.json                 # Config for Python controller
├── stam_config_java.properties      # Config for Java controller
└── README.md                        # This file
```

---

## 🐍 Python Deployment

### 🔧 Requirements

- Python 3.6+
- `stam_config.json` in the same directory

### ▶️ To Run

```bash
python3 stam_controller.py
```

### 🧠 Behavior

- Simulates reception of PDSM reports  
- Evaluates controller state (traffic, delay, congestion)  
- Initiates adaptive coordination via TCC (prints simulation of PALB policy updates)  
- Loops with feedback-based performance evaluation  

---

## ☕ Java Deployment

### 🔧 Requirements

- Java 11+
- `stam_config_java.properties` in working directory

### ▶️ To Compile & Run

```bash
javac STAMController.java
java stam.STAMController
```

### 🧠 Behavior

- Initializes with controller ID and key  
- Sets up secure TCC with other controllers  
- Simulates PDSM-driven adaptation  
- Broadcasts policy updates over simulated TCC  

---

## ⚙ Configuration Details

### `stam_config.json` (Python)

```json
{
  "controllers": ["ctrlA", "ctrlB"],
  "shared_keys": {
    "ctrlA": "alpha_secret",
    "ctrlB": "beta_secret"
  },
  "report_interval": 6
}
```

### `stam_config_java.properties` (Java)

```properties
controllers=ctrlA,ctrlB
ctrlA.secret=alpha_secret
ctrlB.secret=beta_secret
report_interval=6
```

---

## 🔄 Integration with MC-LBTO

The STAM module interacts directly with:

- **PDSM**: Consumes reports about link status, delay, and congestion.  
- **PALB**: Coordinates adaptive updates to server weights and flow mappings using TCC messages.  
- **Multi-Controller Topology**: Works in distributed SDN settings where multiple domains are managed.  

---

## 🔁 Dynamic Adaptation Logic

| **Trigger Condition**           | **Adaptive Action**                                |
|-------------------------------|----------------------------------------------------|
| High traffic volume            | Reduce update rate / adjust priorities            |
| Excessive delay                | Coordinate rerouting via PALB                     |
| Congestion alert from PDSM     | Broadcast flow alerts to all controllers          |
| Overloaded controller state    | Sync partial responsibility / rebalance           |

---

## 🧪 Sample Output

```
🔧 STAM Python Controller Starting...
✅ Authenticated: ctrlA
✅ Authenticated: ctrlB
🔗 Establishing Trusted Communication Channels...
📬 Receiving PDSM Report...
📊 Metrics: Traffic=1.1, Delay=0.32, Congestion=True
⚙️  Adaptation Triggered due to: {...}
📨 Disseminating updates to ctrlB via TCC 0x3d9f1e...
```

---

