# File: control_palb.py

from p4runtime_lib.switch import ShutdownAllSwitchConnections
from p4runtime_lib.helper import P4InfoHelper
import time

P4INFO_FILE = 'build/palb.p4.p4info.txt'
JSON_FILE = 'build/palb.json'

FLOW_TO_SERVER_REGISTER = 'flow_to_server'
SERVER_WEIGHT_REGISTER = 'server_weights'

MAX_FLOWS = 1024
MAX_SERVERS = 8


def read_flow_mappings(sw, p4info_helper):
    print("\n[*] Flow-to-server Mappings:")
    for i in range(MAX_FLOWS):
        entry = p4info_helper.build_register_read_request(
            register_name=FLOW_TO_SERVER_REGISTER,
            index=i
        )
        value = sw.ReadRegister(entry)
        if value.data[0] > 0:
            print(f"Flow[{i}] => Server {value.data[0]}")


def read_server_weights(sw, p4info_helper):
    print("\n[*] Current Server Weights:")
    for i in range(MAX_SERVERS):
        entry = p4info_helper.build_register_read_request(
            register_name=SERVER_WEIGHT_REGISTER,
            index=i
        )
        value = sw.ReadRegister(entry)
        print(f"Server[{i}] Weight: {value.data[0]}")


def main():
    p4info_helper = P4InfoHelper(P4INFO_FILE)

    try:
        sw = p4info_helper.build_switch_connection(
            name='s1',
            address='127.0.0.1:50051',
            device_id=0,
            proto_dump_file='logs/s1-palb-requests.log')

        sw.MasterArbitrationUpdate()
        sw.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=JSON_FILE)

        print("[*] Connected to switch. Reading mappings and weights...")

        while True:
            read_flow_mappings(sw, p4info_helper)
            read_server_weights(sw, p4info_helper)
            time.sleep(10)

    except KeyboardInterrupt:
        print("[*] Interrupted. Cleaning up...")
    finally:
        ShutdownAllSwitchConnections()


if __name__ == '__main__':
    main()
