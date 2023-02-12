#!/bin/bash

rojo_luminoso='\033[1;31m'
verde_luminoso='\033[1;32m'
cyan_luminoso='\033[1;36m'
amarillo_luminoso='\033[1;33m'
sin_color='\033[0m'

read -p "Introduce tu IP: " variable

ping -c 1 $variable  > /dev/null

if [ "$(echo $?)" == "0" ]; then
  echo -e "${verde_luminoso}El host está disponible${sin_color}"
  ttl=$(ping -c 1 $variable | grep "ttl=" | awk '{print $7}' | tr -d "ttl=")
  if [ $ttl -gt 60 ] && [ $ttl -lt 90 ]; then
   echo -e "${cyan_luminoso}La máquina es un Linux, porque el TTL es de $ttl${sin_color}" 
  elif [ $ttl -gt 110 ] && [ $ttl -lt 140 ]; then
   echo -e "${cyan_luminoso}La máquina es un Windows, porque el TTL es de $ttl${sin_color}"
  else
   echo -e "${amarillo_luminoso}TTL desconocido, el valor obtenido es $ttl${sin_color}" 
fi

else
  echo -e "${rojo_luminoso}Hubo un error, vuelve a intentarlo${sin_color}"
fi
