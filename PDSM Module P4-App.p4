/*************************************************************************
*********************** PDSM Module  ***********************************
*************************************************************************/

// File: pdsm.p4

#include <core.p4>

// Define Ethernet, IPv4, TCP headers
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

header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4> dataOffset;
    bit<3> reserved;
    bit<9> flags;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}

// Parsed headers and metadata
struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    tcp_t tcp;
}

struct metadata {
    bit<32> flow_hash;
}

// Registers
const bit<32> MAX_FLOWS = 1024;

register<bit<64>>(MAX_FLOWS) pkt_count;
register<bit<64>>(MAX_FLOWS) byte_count;
register<bit<32>>(MAX_FLOWS) last_seen;

parser Parser(packet_in pkt, out headers hdr, inout metadata meta, inout standard_metadata_t smeta) {
    state start {
        pkt.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            0x0800: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        pkt.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            6: parse_tcp;
            default: accept;
        }
    }

    state parse_tcp {
        pkt.extract(hdr.tcp);
        transition accept;
    }
}

control Ingress(inout headers hdr, inout metadata meta, inout standard_metadata_t smeta) {
    apply {
        // Compute 5-tuple hash as flow ID
        meta.flow_hash = hash(meta.flow_hash, HashAlgorithm.crc32, 32w0, {
            hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, hdr.ipv4.protocol,
            hdr.tcp.srcPort, hdr.tcp.dstPort
        });

        // Read current counters
        bit<64> cur_pkt_cnt;
        bit<64> cur_byte_cnt;
        bit<32> cur_last_seen;

        pkt_count.read(cur_pkt_cnt, meta.flow_hash);
        byte_count.read(cur_byte_cnt, meta.flow_hash);
        last_seen.read(cur_last_seen, meta.flow_hash);

        // Update counts
        pkt_count.write(meta.flow_hash, cur_pkt_cnt + 1);
        byte_count.write(meta.flow_hash, cur_byte_cnt + smeta.packet_length);

        // Optionally trigger reporting if idle time exceeded
        bit<32> now = (bit<32>) standard_metadata.ingress_global_timestamp;
        if ((now - cur_last_seen) > 1000000) { // ~1ms threshold
            // In real P4, we would send digest to controller
            // Placeholder: mark for further processing
        }

        last_seen.write(meta.flow_hash, now);
    }
}

control Egress(inout headers hdr, inout metadata meta, inout standard_metadata_t smeta) {
    apply { }
}

control Deparser(packet_out pkt, in headers hdr) {
    apply {
        pkt.emit(hdr.ethernet);
        pkt.emit(hdr.ipv4);
        pkt.emit(hdr.tcp);
    }
}

V1Switch(Parser(), Ingress(), Egress(), Deparser())
