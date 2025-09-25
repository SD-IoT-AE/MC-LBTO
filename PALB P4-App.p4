/*************************************************************************
*********************** PALB Module    ***********************************
*************************************************************************/
// File: palb.p4

#include <core.p4>

// Define headers
header ethernet_t {
    mac_addr dstAddr;
    mac_addr srcAddr;
    bit<16> etherType;
}

header ipv4_t {
    bit<4> version;
    bit<4> ihl;
    bit<8> dscp;
    bit<8> ecn;
    bit<16> totalLen;
    bit<16> identification;
    bit<3> flags;
    bit<13> fragOffset;
    bit<8> ttl;
    bit<8> protocol;
    bit<16> hdrChecksum;
    bit<32> srcAddr;
    bit<32> dstAddr;
}

struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
}

struct metadata {
    bit<8> selected_server;
    bit<32> flow_hash;
}

// Parameters
const bit<8> MAX_SERVERS = 8;

// Server pool
const mac_addr server_macs[MAX_SERVERS] = {
    0x00_00_00_00_00_11,
    0x00_00_00_00_00_12,
    0x00_00_00_00_00_13,
    0x00_00_00_00_00_14,
    0x00_00_00_00_00_15,
    0x00_00_00_00_00_16,
    0x00_00_00_00_00_17,
    0x00_00_00_00_00_18
};

const bit<32> server_ips[MAX_SERVERS] = {
    0x0a000002, 0x0a000003, 0x0a000004, 0x0a000005,
    0x0a000006, 0x0a000007, 0x0a000008, 0x0a000009
};

// Registers to store weights and flow-to-server mapping
register<bit<8>>(MAX_SERVERS) server_weights;
register<bit<8>>(1024) flow_to_server;

// Ingress logic
control Ingress(inout headers hdr, inout metadata meta, inout standard_metadata_t smeta) {
    action select_server() {
        meta.flow_hash = hash(meta.flow_hash, HashAlgorithm.crc32, 32w0, {
            hdr.ipv4.srcAddr, hdr.ipv4.dstAddr
        });
        bit<8> selected = meta.flow_hash % MAX_SERVERS;
        meta.selected_server = selected;
        flow_to_server.write(meta.flow_hash % 1024, selected);
    }

    action forward_to_server(bit<8> sid) {
        hdr.ipv4.dstAddr = server_ips[sid];
        hdr.ethernet.dstAddr = server_macs[sid];
    }

    apply {
        select_server();
        forward_to_server(meta.selected_server);
    }
}

control Parser(packet_in pkt, out headers hdr, inout metadata meta, inout standard_metadata_t smeta) {
    state start {
        pkt.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            0x0800: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        pkt.extract(hdr.ipv4);
        transition accept;
    }
}

control Egress(inout headers hdr, inout metadata meta, inout standard_metadata_t smeta) {
    apply { }
}

control Deparser(packet_out pkt, in headers hdr) {
    apply {
        pkt.emit(hdr.ethernet);
        pkt.emit(hdr.ipv4);
    }
}

V1Switch(Parser(), Ingress(), Egress(), Deparser())
