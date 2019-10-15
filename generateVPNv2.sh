#!/bin/sh
USER="$(whoami)"
GROUP="vpns"

SOCKETFILE="/tmp/socketIPC.s"
SOCKET_DIR="$(dirname ${SOCKETFILE})"

mkdir "${SOCKET_DIR}" || true
chown "${USER}:${GROUP}" "${SOCKET_DIR}"

chmod 750 "${SOCKET_DIR}"

rm -f "${SOCKETFILE}"

change_permission() {
  # Wait for the file creation and then change the permissions.
  while ! test -e $1 ; do
    sleep .3
    echo "File not found sleeping"
  done

  echo "File found, changing permission"
  chmod 660 $1
}

change_permission "${SOCKETFILE}" &

nc -klU "${SOCKETFILE}" | while read USERNAME; do
  if echo "${USERNAME}" | egrep -q '^[a-fA-F0-9]+$'; then
    echo "${USERNAME}"
  fi
done
