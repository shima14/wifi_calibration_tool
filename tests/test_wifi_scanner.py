# tests/test_wifi_scanner.py
from src.wifi_scanner import scan_wifi

def test_scan_wifi():
    wifi_data = scan_wifi()
    assert isinstance(wifi_data, list)
    assert 'ssid' in wifi_data[0]
    assert 'signal' in wifi_data[0]
