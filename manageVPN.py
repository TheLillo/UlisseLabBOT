from pathlib import Path
import os
import time


def check_or_gen_vpn(vpn_dir, temp_dir, first_name):
    # check if vpn is present in directory else generate
    vpn_file = '{}{}.conf'.format(vpn_dir, str(first_name))
    if not Path(temp_dir).is_dir():
        access_rights = 0o744
        try:
            # If the directory already exists, FileExistsError is raised.
            os.mkdir(temp_dir, access_rights)
        except OSError:
            print("Creation of the directory %s failed" % temp_dir)
            exit(1)
        else:
            print("Successfully created the directory %s" % temp_dir)

    if Path(vpn_file).is_file():
        return vpn_file
    else:
        full_path = '{}{}'.format(temp_dir, str(first_name))
        Path(full_path).touch()
        time.sleep(5)
        return vpn_file
