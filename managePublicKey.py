import yaml
import sys


def add_public_key(public_keys_file, telegram_name, public_key):
    found = False
    with open(public_keys_file, 'r') as f:
        try:
            cur_yaml = yaml.safe_load(f)
            for player in cur_yaml['players']:
                if player['telegram_name'] == telegram_name:
                    player['ssh_key'] = public_key
                    found = True
            if not found:
                cur_yaml['players'].append({'name': telegram_name, 'telegram_name': telegram_name, 'ssh_key': public_key})
        except yaml.YAMLError as exc:
            print(exc, file=sys.stderr)
    if cur_yaml:
        with open(public_keys_file, 'w') as f:
            try:
                yaml.safe_dump(cur_yaml, f)
            except yaml.YAMLError as exc:
                print(exc, file=sys.stderr)
