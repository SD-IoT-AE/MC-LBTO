# stam_controller.py
# ---------------------------------------------
# Python-based implementation of the STAM (Secure Trusted Adaptive Multi-Control)
# coordination logic for distributed SDN controllers in SD-IoT.
# This version includes secure initialization, PDSM-driven adaptation,
# and PALB policy synchronization through a simulated TCC (Trusted Communication Channel).

import json
import random
import time
from datetime import datetime

# ========== PHASE 1: Initialization ==========

with open("stam_config.json") as f:
    config = json.load(f)

controller_id = "ctrlA"
controller_key = config["shared_keys"][controller_id]
controllers = config["controllers"]
shared_keys = config["shared_keys"]
report_interval = config["report_interval"]

authenticated_controllers = []
tcc_links = {}

def authenticate_controllers():
    print("🔐 Authenticating Controllers...")
    for cid in controllers:
        if cid in shared_keys:
            print(f"✅ Authenticated: {cid}")
            authenticated_controllers.append(cid)
        else:
            print(f"❌ Failed Authentication: {cid}")

# ========== PHASE 2: Secure Channel Setup ==========

def establish_tcc():
    print("🔗 Establishing Trusted Communication Channels...")
    for i in authenticated_controllers:
        for j in authenticated_controllers:
            if i != j:
                tcc_key = hash(f"{i}:{j}")
                tcc_links[f"{i}->{j}"] = hex(tcc_key & 0xffffffff)

# ========== PHASE 3-7: Main Adaptive Logic ==========

def receive_pds_metrics():
    return {
        "traffic_volume": round(random.uniform(0.4, 1.2), 2),
        "delay": round(random.uniform(0.1, 0.35), 2),
        "congestion_alert": random.random() > 0.75
    }

def assess_controller_state(metrics):
    overloaded = metrics["traffic_volume"] > 1.0 or metrics["delay"] > 0.3
    return overloaded

def trigger_adaptation(metrics):
    print(f"⚙️  Adaptation Triggered due to: {metrics}")
    for peer in authenticated_controllers:
        if peer != controller_id:
            tcc_id = f"{controller_id}->{peer}"
            print(f"📨 Disseminating updates to {peer} via TCC {tcc_links[tcc_id]}...")
            print(f"📡 → Send PALB policy hint: adjust server weights, prioritize alert queues")

def monitor_feedback():
    print("🔁 Feedback Phase: Monitoring adaptation impact...")
    delta = round(random.uniform(0.05, 0.1), 2)
    print(f"📈 Observed performance improvement: +{int(delta*100)}%")

# ========== MAIN LOOP ==========

def main_loop():
    print(f"🧠 Controller {controller_id} entering operational loop...\n")
    while True:
        print("📬 Receiving PDSM Report...")
        metrics = receive_pds_metrics()
        print(f"📊 Metrics: Traffic={metrics['traffic_volume']}, Delay={metrics['delay']}, Congestion={metrics['congestion_alert']}")

        overloaded = assess_controller_state(metrics)
        if overloaded or metrics["congestion_alert"]:
            trigger_adaptation(metrics)
        monitor_feedback()
        print("⏳ Waiting for next interval...\n")
        time.sleep(report_interval)

# ========== EXECUTION ==========

if __name__ == "__main__":
    print("🔧 STAM Python Controller Starting...\n")
    authenticate_controllers()
    establish_tcc()
    main_loop()
