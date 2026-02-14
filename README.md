# Ataque y Mitigación: DHCP Starvation, DHCP Spoofing y STP Root Attack

**Robinson De Los Santos Santos**
**Matrícula:** 2024-1252
**Asignatura:** Seguridad de Sistemas Operativos / Redes
**Entorno:** Laboratorio Virtual (GNS3/EVE-ng con Kali Linux y Cisco IOSv)

---

## 1. Objetivo de los Scripts

El propósito de este conjunto de herramientas es demostrar las vulnerabilidades inherentes en la Capa 2 (Enlace de Datos) y en la asignación dinámica de direcciones, explotando la confianza predeterminada de los switches.

* **`dhcp_starvation.py` (Agotamiento de DHCP):**
    * Genera miles de solicitudes DHCP DISCOVER falsas con direcciones MAC aleatorias.
    * **Objetivo:** Agotar la totalidad del *pool* de direcciones IP del servidor legítimo, provocando una Denegación de Servicio (DoS) para los nuevos clientes que intenten conectarse.

* **`dhcp_spoofing.py` (Servidor DHCP Falso / Rogue DHCP):**
    * Actúa como un servidor DHCP no autorizado.
    * Responde a las solicitudes de los clientes (DHCP DISCOVER) antes que el servidor real.
    * **Objetivo:** Asignar a la víctima una configuración de red maliciosa, estableciendo la IP del atacante como la "Puerta de Enlace" (Gateway) para interceptar el tráfico (Man-in-the-Middle).

* **`stp_root_attack.py` (Manipulación de Spanning Tree):**
    * Inyecta tramas BPDU (Bridge Protocol Data Units) falsificadas indicando una prioridad superior (valor numérico más bajo) a la del Root Bridge actual.
    * **Objetivo:** Forzar una reconvergencia de la topología lógica para que el switch del atacante se convierta en el "Root Bridge", atrayendo el tráfico de la red hacia él.

---

## 2. Topología de Red

El laboratorio se ha configurado utilizando el esquema de direccionamiento basado en la matrícula: **24.12.52.0/24**.

<img width="605" height="562" alt="Captura de pantalla 2026-02-13 224743" src="https://github.com/user-attachments/assets/70822da9-8c48-4c04-ae56-cf7e759c1ace" />

### Tabla de Direccionamiento e Interfaces

| Dispositivo | Interfaz | Dirección IP | Rol |
| :--- | :--- | :--- | :--- |
| **R1 (Cisco Router)** | Gi0/0 | `24.12.52.1` | Gateway Legítimo / Servidor DHCP |
| **Switch L2** | Vlan 1 | N/A | Distribución |
| **Kali Linux** | Eth0 | `24.12.52.121` | Atacante (Rogue Server) |
| **PC1 (Víctima)** | Eth0 | DHCP (Recibe `.150`) | Cliente Vulnerable |

---

## 3. 🛠️ Requisitos del Sistema

Para ejecutar estas herramientas se requiere el siguiente entorno:

* **Sistema Operativo:** Kali Linux (o cualquier distribución Linux basada en Debian).
* **Lenguaje:** Python 3.x.
* **Privilegios:** Root / Sudo (necesario para crear sockets raw y manipular interfaces de red).
* **Librerías Python:**
    ```bash
    pip3 install scapy
    ```

---

## 4. Ejecución y Parámetros

### A. Ataque DHCP Starvation (`dhcp_starvation.py`)

Este script utiliza Scapy para inundar la red con peticiones de clientes inexistentes.


<img width="762" height="145" alt="Captura de pantalla 2026-02-13 224814" src="https://github.com/user-attachments/assets/e80835f8-1212-4f15-9ff8-61c51d8e5b72" />

Antes de la ejecucion del script


<img width="469" height="115" alt="Captura de pantalla 2026-02-13 224901" src="https://github.com/user-attachments/assets/80f200b2-4e99-4387-8042-576e66fcba77" />

Envía paquetes DHCP DISCOVER en bucle con MACs de origen aleatorias (Random MAC).


<img width="726" height="236" alt="Captura de pantalla 2026-02-13 224913" src="https://github.com/user-attachments/assets/c93765b1-d098-40d9-b2e9-ba5d4ff5da35" />

Resultado





### B. Ataque DHCP Spoofing (`dhcp_spoofing.py`)

Este script escucha la red esperando peticiones DHCP y lanza una oferta maliciosa.


<img width="369" height="49" alt="Captura de pantalla 2026-02-13 225021" src="https://github.com/user-attachments/assets/6e08f8a9-89ca-43f8-b39b-ac8ec6c7a26b" />


Como se ve en PC1 antes de su ejecucion


* **Parámetros configurables en el script:**

<img width="416" height="158" alt="Captura de pantalla 2026-02-13 225047" src="https://github.com/user-attachments/assets/4e9a8469-d778-4baf-9afe-5cf8d4f5e6fd" />


* **Evidencia de Ejecución:**
    1.  La víctima solicita una IP (`ip dhcp`).
    2.   El script detecta la petición y envía una "Oferta Unicast".
    3. **Resultado en la Víctima:** Al hacer `ipconfig` o `show ip`, se observa que su Gateway es ahora `24.12.52.121` (el atacante), permitiendo la intercepción de datos.

<img width="416" height="154" alt="Captura de pantalla 2026-02-13 225008" src="https://github.com/user-attachments/assets/e59cd4c8-5cf4-414c-9141-e2ce44ae2086" />

--

<img width="369" height="49" alt="Captura de pantalla 2026-02-13 225021" src="https://github.com/user-attachments/assets/c713e9b7-b4b6-4865-a64d-bd1f61a3bd9b" />

Resultado


### C. Ataque STP Root (`stp_root_attack.py`)


<img width="632" height="540" alt="Captura de pantalla 2026-02-13 225109" src="https://github.com/user-attachments/assets/de00aaa8-9404-4eed-a565-8d00f6d72f2e" />

Como se ve antes


Genera BPDUs de configuración superiores para secuestrar el rol de Root Bridge.

* **Comportamiento:** Envía tramas STP anunciando una prioridad de puente (Bridge Priority) extremadamente baja (ej: 0 o 4096) para ganar la elección de Root.
* **Impacto:**
    * El switch legítimo recibe las BPDUs y recalcula el árbol de expansión.
    * El tráfico de otras VLANs podría empezar a fluir a través del enlace del atacante, permitiendo sniffing o causando inestabilidad en la red.
 
    * 
<img width="588" height="121" alt="Captura de pantalla 2026-02-13 225126" src="https://github.com/user-attachments/assets/587c63f5-f512-40d3-a37a-88d87aea0f58" />

--

<img width="703" height="328" alt="Captura de pantalla 2026-02-13 225136" src="https://github.com/user-attachments/assets/13bd67f3-fd96-4c4f-a6b1-a775588e7ed6" />

Resultado


## 5. Medidas de Mitigación

Para proteger la infraestructura contra estos ataques de Capa 2, se deben implementar las siguientes configuraciones de "Hardening" en los switches Cisco:

### Contra Ataques DHCP (Snooping)

La defensa principal es **DHCP Snooping**. Esto clasifica los puertos en "Trusted" (Confianza) y "Untrusted" (Sin Confianza).

```cisco
! 1. Habilitar DHCP Snooping globalmente
Switch(config)# ip dhcp snooping
Switch(config)# ip dhcp snooping vlan 1

! 2. Configurar el puerto del Router (o DHCP legítimo) como "Trusted"
Switch(config)# interface GigabitEthernet0/0
Switch(config-if)# ip dhcp snooping trust

! 3. (Opcional) Limitar la tasa de paquetes en puertos de acceso para evitar Starvation
Switch(config)# interface GigabitEthernet0/1
Switch(config-if)# ip dhcp snooping limit rate 10
