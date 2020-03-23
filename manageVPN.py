from pathlib import Path
import os
import socket
import sys
import hashlib
import platform
import select


def check_or_gen_vpn(socket_address, vpn_dir, checker_new_vpn, username):
    if Path(socket_address).exists():
        first_name_as_bytes = username.encode('utf-8')
        name_sha256 = hashlib.sha256()
        name_sha256.update(first_name_as_bytes)
        first_name_hexdigest = name_sha256.hexdigest()
        vpn_file = '{}{}.conf'.format(vpn_dir, str(first_name_hexdigest))
        if Path(vpn_file).is_file():
            return vpn_file
        else:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
                client.connect(socket_address)
                client.send(first_name_hexdigest.encode('utf-8'))
                client.send("\n".encode('utf-8'))
                # Controllo che sia avvenuta la creazione
                if platform.system().casefold() == 'linux'.casefold():
                    #TODO: use Pynotify to check that vpn was create
                    raise NotImplementedError
                elif platform.system().casefold() == 'openbsd'.casefold():
                    kq = select.kqueue()

                    fd = os.open(checker_new_vpn, os.O_DIRECTORY | os.O_RDONLY)

                    ev = [select.kevent(fd,
                                        filter=select.KQ_FILTER_VNODE,
                                        flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE | select.KQ_EV_CLEAR,
                                        fflags=select.KQ_NOTE_WRITE
                                        )]

                    kq.control(ev, 1, None)
                    os.fsync(fd)
                    os.close(fd)
                else:
                    print("This Os is not supported :(", file=sys.stderr)
                    
                if Path(vpn_file).is_file():
                    return vpn_file
                else:
                    print("Could not find VPN file :(", file=sys.stderr)
    else:
        print("Could not connect to the server :(", file=sys.stderr)
