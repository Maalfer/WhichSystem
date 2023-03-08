# WhichSystem

----

Script programado en en un directo de Twitch con la comunidad que sirve para detectar el sistema operativo de una dirección IP basándose en el TTL.

----

### Reescrito usando python y el modulo scapy.

Sistemas que se pueden detectar con el script mediante su ttl:

```python
ttls = {
    30 :  ["DC-OSx"],
    32 :  ["Windows 96/98/NT3.51"],
    59 :  ["HPJetDirect"],
    60 :  ["AIX"],
    64 :  ["Red Hat 9", "Linux"],
    128 : ["Windows NT 4.0/2000/XP/2003 server/..."],
    255 : ["Solaris", "Cisco", "Unix"]
}
```

Para intentar hacer una busqueda aproximada del sistema objetivo usamos lo siguiente

```Python
# ....
for ttl in ttls.keys():
    if deducion_ttl > ttl_anterior and deducion_ttl < ttl:
        # ....
    # ....
```

Donde obtenemos cada ttl disponible de la lista, y buscamos por rangos, si el ttl que se recibio, es menor que el cierto ttl en la lista y mayor que otro, se intuye que el sistema sea alguno de los dos, el que mas se aproxima al valor ttl del sistema de la lista.

----
# Instalacion

```batch
sudo apt-get install python3
pip install -r requirements.txt
```
----

# Ejecucion

```batch
python3 script_chulisimo.py
```
Acontinuacion podra usted ingresar la direcion IP version 4 a la que quiere realizar este reconbimiento basico.

## Ejemplo de la Ejecucion:

```python
Direccion de destino: 8.8.8.8
Begin emission:
Finished sending 1 packets.
.*
Received 2 packets, got 1 answers, remaining 0 packets
IP / ICMP 8.8.8.8 > 192.168.6.38 echo-reply 0
###[ IP ]### 
  version   = 4
  ihl       = 5
  tos       = 0x0
  len       = 28
  id        = 0
  flags     = 
  frag      = 0
  ttl       = 114
  proto     = icmp
  chksum    = 0x7203
  src       = 8.8.8.8
  dst       = 192.168.6.38
  \options   \
###[ ICMP ]### 
     type      = echo-reply
     code      = 0
     chksum    = 0x0
     id        = 0x0
     seq       = 0x0
     unused    = ''

Eñ TTL obtenido es:  114
tabla de TLL's:
TTL: 30, Sistema que emplea este TTL: DC-OSx
TTL: 32, Sistema que emplea este TTL: Windows 96/98/NT3.51
TTL: 59, Sistema que emplea este TTL: HPJetDirect
TTL: 60, Sistema que emplea este TTL: AIX
TTL: 64, Sistema que emplea este TTL: Red Hat 9
TTL: 64, Sistema que emplea este TTL: Linux
TTL: 128, Sistema que emplea este TTL: Windows NT 4.0/2000/XP/2003 server/...
TTL: 255, Sistema que emplea este TTL: Solaris
TTL: 255, Sistema que emplea este TTL: Cisco
TTL: 255, Sistema que emplea este TTL: Unix

Intentaremos llegar a alguna conclusion:
Podria ser un sistema ['Red Hat 9', 'Linux'] con ttl: 64, o
Podria ser un sistema ['Windows NT 4.0/2000/XP/2003 server/...'] con ttl: 128
Pues el ttl:(114) esta en el rango de: (64-128)
```
----