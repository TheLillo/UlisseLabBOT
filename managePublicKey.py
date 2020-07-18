import yaml
import sys
import subprocess
from os import path


def add_public_key(public_keys_file, telegram_name, public_key):
    found = False
    with open(public_keys_file, 'r') as f:
        try:
            cur_yaml = yaml.safe_load(f)
            for player in cur_yaml['players']:
                if player['telegram_name'] == telegram_name:
                    player['ssh_key'] += public_key
                    found = True
            if not found:
                cur_yaml['players'].append({'name': telegram_name, 'telegram_name': telegram_name, 'ssh_key': (public_key)})
        except yaml.YAMLError as exc:
            print(exc, file=sys.stderr)
    if cur_yaml:
        with open(public_keys_file, 'w') as f:
            try:
                yaml.safe_dump(cur_yaml, f)
            except yaml.YAMLError as exc:
                print(exc, file=sys.stderr)
    try:
        # git_dir = path.dirname(public_keys_file)
        # subprocess.run(["git", "add", "{}".format(public_keys_file)],  cwd=git_dir, check=True)
        # subprocess.run(["git", "commit", "-m 'update players.yaml'"], cwd=git_dir, check=True)
        # subprocess.run(["git", "push"], cwd=git_dir, check=True)
        subprocess.run(["/usr/local/bin/add_user_key.sh", "{}".format(public_key)], check=True)
    except exc:
        print(exc, file=sys.stderr)
