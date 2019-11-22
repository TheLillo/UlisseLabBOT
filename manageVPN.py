from pathlib import Path
# import os
# import time
import socket
import sys
import hashlib
import time

# def check_or_gen_vpn(vpn_dir, temp_dir, first_name):
#     # check if vpn is present in directory else generate
#     vpn_file = '{}{}.conf'.format(vpn_dir, str(first_name))
#     if not Path(temp_dir).is_dir():
#         access_rights = 0o744
#         try:
#             # If the directory already exists, FileExistsError is raised.
#             os.mkdir(temp_dir, access_rights)
#         except OSError:
#             print("Creation of the directory %s failed" % temp_dir)
#             exit(1)
#         else:
#             print("Successfully created the directory %s" % temp_dir)
#
#     if Path(vpn_file).is_file():
#         return vpn_file
#     else:
#         full_path = '{}{}'.format(temp_dir, str(first_name))
#         Path(full_path).touch()
#         time.sleep(5)
#         return vpn_file


def check_or_gen_vpn(socket_address, vpn_dir, username):
    if Path(socket_address).exists():
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(socket_address)
            first_name_as_bytes = username.encode('utf-8')
            name_sha256 = hashlib.sha256()
            name_sha256.update(first_name_as_bytes)
            first_name_hexdigest = name_sha256.hexdigest()
            client.send(first_name_hexdigest.encode('utf-8'))
            client.send("\n".encode('utf-8'))
            # Controllo che sia avvenuta la creazione
            time.sleep(2)
            vpn_file = '{}{}.conf'.format(vpn_dir, str(first_name_hexdigest))
            if Path(vpn_file).is_file():
                return vpn_file
            else:
                print("Could not find VPN file :(", file=sys.stderr)
    else:
        print("Could not connect to the server :(", file=sys.stderr)

