#!/bin/sh

while true; do
  USERNAME="$(nc -Ul -w 10 /tmp/socketIPC.s)"
  ksh $(which generate_certificate.sh) "$USERNAME"
done