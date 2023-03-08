"""import socket

# El modulo struct permite convertir tipos de 
# datos nativos de Python como enteros y cadenas 
# en una cadena de bytes y viceversa.
import struct


import os
import time
from getpass import _raw_input

def calc_checksum(data):
    
    # Si la longitud de los datos es impar, agregue un byte nulo al final
    if len(data) % 2 == 1:
        data += b'\x00'
    
    # Suma cada palabra de 16 bits (2 bytes) en los datos
    s = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i+1]
        s += word
    
    # Suma el acarreo de las palabras de 16 bits
    s = (s >> 16) + (s & 0xffff)
    s += (s >> 16)
    
    # Tome el complemento a uno del resultado y devuelva el valor en formato de 16 bits
    return (~s) & 0xffff


if __name__ == '__main__':

    dst_addr = "127.0.0.1"#_raw_input("Direccion de destino: ")
    print(dst_addr)

    
    # Aqui, AF_INET representa la familia de direcciones 
    # (nombre de host o direccion IP) y SOCK_DGRAM representa 
    # el tipo de socket para el protocolo basado en datagramas (UDP).
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    
    # se ejecuta en s para permitir que otros sockets se conecten 
    # a la misma direccion/puerto.
    
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    

    # se ejecuta en s para establecer el valor de tiempo de vida (TTL) en 20 
    # saltos para los paquetes IP multicast enviados desde este socket.

    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 128)


    #  Se prepara un paquete binario ICMP Echo Request utilizando el metodo struct.pack()
    #  El formato de un paquete de peticion de eco ICMP es: 1 byte para el tipo de mensaje, 
    #  1 byte para el codigo de mensaje, 2 bytes para la suma de comprobacion, 
    #  2 bytes para el identificador y 2 bytes para el numero de secuencia. 
    # 
    #  0                   1                   2                   3
    #  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |     Type(8)   |     Code(0)   |          Checksum             |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |           Identifier          |        Sequence Number        |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #  
    #  1 byte para el tipo de mensaje
    #  1 byte para el codigo de mensaje
    #  2 bytes para la suma de comprobacion.(Checksum)
    #  2 bytes para el identificador
    #  2 bytes para el numero de secuencia.


    #Inicialmente, los valores del paquete se establecen en 8, 0, 0, 0 y 0 respectivamente.
    packet = struct.pack('!BBHHH', 8, 0, 0, 0, 0)
    
    #Se calcula un valor de suma de comprobacion para el paquete utilizando la funcion calc_checksum() 
    checksum = calc_checksum(packet)
    packet = struct.pack('!BBHHH', 8, 0, checksum, 0, 0)
    
    # Utilizando el metodo .sendto() del objeto socket s, el paquete se 
    # transmite a la direccion de destino dada (dst_addr, 0).
    direccion = (dst_addr, 0)
    print(direccion)
    s.sendto(packet, direccion)



    # Usando el metodo .settimeout() del objeto socket s, se establece un tiempo 
    # de espera de 2 segundos para recibir una respuesta de la maquina de destino.
    s.settimeout(3)
    
    try:
        # Cuando se recibe una respuesta, una variable recv_packet almacena 
        # el paquete junto con la informacion de la direccion.
        recv_packet, addr = s.recvfrom(1024)

        ttl = struct.unpack('!BBHHH', recv_packet[:8])[5]

        print('TTL: {}'.format(ttl))

    except socket.timeout:
        print("No se puedo recibir datos del destino")
"""

from scapy.all import *
from getpass import _raw_input
import time

ttls = {
    30 :  ["DC-OSx"],
    32 :  ["Windows 96/98/NT3.51"],
    59 :  ["HPJetDirect"],
    60 :  ["AIX"],
    64 :  ["Red Hat 9", "Linux"],
    128 : ["Windows NT 4.0/2000/XP/2003 server/..."],
    255 : ["Solaris", "Cisco", "Unix"]
}

conf.color_theme = BrightTheme()

# preparar el paquete ICMP:
packet = IP(dst=_raw_input("Direccion de destino: "))/ICMP(type=8, code=0)

# Enviar el paquete ICMP y espera la respuesta durante 1 segundo:
reply = sr1(packet, timeout=1)

if reply:
    
    deducion_ttl = reply.ttl
    
    print(reply.summary())
    reply.show2()
    print("Eñ TTL obtenido es: ", reply.ttl)
    print("tabla de TLL's:")
    
    for ttl in ttls.keys():
        for _os in ttls[ttl]:
            print("TTL: {}, Sistema que emplea este TTL: {}".format(ttl, _os))
    
    ttl_anterior = 0       
    print("\nIntentaremos llegar a alguna conclusion:") 
    for ttl in ttls.keys():
        if deducion_ttl > ttl_anterior and deducion_ttl < ttl:
            print("Podria ser un sistema {} con ttl: {}, o".format(ttls[ttl_anterior], ttl_anterior))
            print("Podria ser un sistema {} con ttl: {}".format(ttls[ttl], ttl))
            print("Pues el ttl:({}) esta en el rango de: ({}-{})".format(deducion_ttl, ttl_anterior, ttl))
            break
        ttl_anterior = ttl