# File: server_monitor.py

import time
import random
import json
from p4runtime_lib.switch import ShutdownAllSwitchConnections
from p4runtime_lib.helper import P4InfoHelper

# Sample simulation of server metrics
MAX_SERVERS = 8
P4INFO_PATH = 'build/palb.p4.p4info.txt'
JSON_PATH = 'build/palb.json'
SERVER_WEIGHT_REGISTER = 'server_weights'

# Simulated server metric collector
def simulate_server_metrics():
    # Simulate CPU or queue load as random values
    return [random.randint(10, 100) for _ in range(MAX_SERVERS)]

# Normalize to weights between 1 and 10
def calculate_weights(metrics):
    max_val = max(metrics)
    return [max(1, int(10 * (1 - (m / max_val)))) for m in metrics]  # lower load = higher weight

def main():
    p4info_helper = P4InfoHelper(P4INFO_PATH)

    try:
        sw = p4info_helper.build_switch_connection(
            name='s1',
            address='127.0.0.1:50051',
            device_id=0,
            proto_dump_file='logs/s1-p4runtime-requests.log')

        sw.MasterArbitrationUpdate()
        sw.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=JSON_PATH)

        print("[*] Connected to switch. Starting weight updates...")

        while True:
            metrics = simulate_server_metrics()
            weights = calculate_weights(metrics)
            print(f"[*] Updating server weights: {weights}")
            for i, w in enumerate(weights):
                sw.WriteRegisterEntry(SERVER_WEIGHT_REGISTER, i, w)
            time.sleep(5)

    except KeyboardInterrupt:
        print("[*] Stopping monitor.")
    finally:
        ShutdownAllSwitchConnections()

if __name__ == '__main__':
    main()
