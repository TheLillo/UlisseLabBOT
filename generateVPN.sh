#!/bin/sh

inotifywait -m /tmp/user_temp -e create -e moved_to |
    while read path action file; do
      ksh $(which generate_certificate.sh) "$file"
      wait
      rm /tmp/user_temp/"$file"
    done

