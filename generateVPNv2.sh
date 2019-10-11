#!/bin/sh

if [ "$#" -eq 0 ] && [ -z "$1" ] && [ -z "$2" ]; then
	echo " need user and group the same of UlisseLabBOT"
	exit
fi

USER="$1"
GROUP="$2"

(nc -Ul /tmp/socketIPC.s &) ; sleep 1 && pkill netcat ; chown "$USER":"$GROUP" /tmp/socketIPC.s

while true; do
  USERNAME="$(nc -Ulk -w 10 /tmp/socketIPC.s)"
  ksh $(which generate_certificate.sh) "$USERNAME"
done
