
# P4Runtime Control App (Python)

# File: control.py

from p4runtime_lib.switch import ShutdownAllSwitchConnections
from p4runtime_lib.helper import P4InfoHelper
import time
import grpc

# Path to your P4Info and BMv2 JSON file\p4info_file_path = "build/pdsm.p4.p4info.txt"
bmv2_json_file_path = "build/pdsm.json"

def write_register(sw, reg_name, index, value):
    entry = sw.RegisterEntry()
    entry.register = reg_name
    entry.index = index
    entry.data = [value]
    sw.WriteRegister(entry)

def read_register(sw, reg_name, index):
    entry = sw.RegisterEntry()
    entry.register = reg_name
    entry.index = index
    return sw.ReadRegister(entry).data[0]

def main():
    p4info_helper = P4InfoHelper(p4info_file_path)

    try:
        sw = p4info_helper.build_switch_connection(
            name='s1',
            address='127.0.0.1:50051',
            device_id=0,
            proto_dump_file='logs/s1-p4runtime-requests.log'
        )

        sw.MasterArbitrationUpdate()
        sw.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=bmv2_json_file_path)
        print("Installed P4 Program on the switch.")

        # Periodically read registers
        while True:
            print("\nFlow Statistics:")
            for index in range(1024):
                pkts = read_register(sw, "pkt_count", index)
                bytes_ = read_register(sw, "byte_count", index)
                if pkts > 0:
                    print(f"Flow[{index}] - Packets: {pkts}, Bytes: {bytes_}")
            time.sleep(5)

    except KeyboardInterrupt:
        print(" Shutting down.")
    except grpc.RpcError as e:
        print(f"gRPC Error: {e.details()}")
    finally:
        ShutdownAllSwitchConnections()

if __name__ == '__main__':
    main()
