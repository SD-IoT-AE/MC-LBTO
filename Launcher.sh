# File: launch_all.sh

#!/bin/bash

# Ensure script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Configurable paths
P4C_BIN="p4c-bm2-ss"
P4SRC="pdsm.p4"
P4JSON="build/pdsm.json"
P4INFO="build/pdsm.p4.p4info.txt"
BMV2_PORT=50051
CONTROLLER_PORT=6653
STAM_PORT=9090

# Create build directory
mkdir -p build logs

# Compile P4 program
echo "[*] Compiling $P4SRC"
$p4c_BIN --target bmv2 --arch v1model -o build $P4SRC

# Launch BMv2 with gRPC
echo "[*] Launching BMv2 switch with $P4JSON"
sudo simple_switch_grpc \
  --device-id 0 \
  -i 0@veth0 \
  $P4JSON \
  -- --grpc-server-addr 127.0.0.1:$BMV2_PORT &
BMV2_PID=$!
sleep 2

# Launch STAM listener
echo "[*] Launching STAM Listener on port $STAM_PORT"
python3 stam_listener.py &
STAM_PID=$!
sleep 1

# Launch Mininet topology
echo "[*] Starting Mininet topology"
sudo python3 topo.py &
TOPO_PID=$!
sleep 3

# Launch control app
echo "[*] Starting P4Runtime controller app"
python3 control.py &
CTRL_PID=$!
sleep 2

# Launch traffic generator
echo "[*] Generating test traffic"
sudo python3 traffic_generator.py

# Cleanup handler
cleanup() {
  echo "[*] Cleaning up..."
  sudo kill $BMV2_PID $STAM_PID $CTRL_PID $TOPO_PID 2>/dev/null
  sudo mn -c
  exit
}

trap cleanup SIGINT

# Keep script running
wait
