import subprocess
import re


def get_connected_ssid():
    try:
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'interfaces'],
            encoding='utf-8',
            errors='ignore'
        )
    except subprocess.CalledProcessError:
        return None

    ssid = None
    signal = None

    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('SSID'):
            match = re.match(r'SSID\s*:\s(.+)', line)
            if match:
                ssid = match.group(1)
        elif line.startswith('Signal'):
            match = re.match(r'Signal\s*:\s(\d+)%', line)
            if match:
                signal = int(match.group(1))

    if ssid:
        return {'SSID': ssid, 'Signal': signal}
    return None


def scan_wifi():
    try:
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
            encoding='utf-8',
            errors='ignore'
        )
    except subprocess.CalledProcessError as e:
        print("Error running netsh:", e)
        return []

    networks = []
    ssid = None
    signal = None

    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('SSID'):
            match = re.match(r'SSID \d+ : (.+)', line)
            if match:
                ssid = match.group(1)
        elif line.startswith('Signal'):
            match = re.match(r'Signal\s*:\s*(\d+)%', line)
            if match:
                signal = int(match.group(1))
            if ssid:
                networks.append({'SSID': ssid, 'Signal': signal})
                ssid = None
                signal = None

    connected = get_connected_ssid()
    if connected and all(n['SSID'] != connected['SSID'] for n in networks):
        networks.append(connected)

    return networks


if __name__ == "__main__":
    nets = scan_wifi()
    for net in nets:
        print(f"SSID: {net['SSID']}, Signal: {net['Signal']}%")
