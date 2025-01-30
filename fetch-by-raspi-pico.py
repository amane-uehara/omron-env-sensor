import time
import struct
import bluetooth # RPI_PICO_W-20241129-v1.24.1

_SENSOR_MAC_ADDR_ = "ba3239a85e8d" # MAC address of your USB sensor (like BA:32:39:A8:5E:8D)

latest_fetch_data = None

def bt_irq(event, data):
  global latest_fetch_data

  if event != 5: # IRQ_SCAN_RESULT
    return

  addr_type, addr, adv_type, rssi, adv_data = data
  mac_str = "".join("{:02x}".format(b).lower() for b in addr)
  raw_bytes = bytes(adv_data)

  if mac_str != _SENSOR_MAC_ADDR_:
    return

  if "Rtb" not in raw_bytes:
    return

  latest_fetch_data = {
    "time":  time.time(),
    "bytes": raw_bytes,
    "mac":   mac_str,
    "rssi":  rssi
  }

def main():
  global latest_fetch_data
  ble = bluetooth.BLE()
  ble.active(True)
  ble.irq(bt_irq)

  previous_fetch_data = None
  while True:
    ble.gap_scan(1000, 3000, 3000)
    time.sleep(3)
    ble.gap_scan(None)
    if previous_fetch_data != latest_fetch_data:
      print(latest_fetch_data)
      value = struct.unpack("<hhhlhhh", latest_fetch_data["bytes"][9:25])
      print(value)
      previous_fetch_data = latest_fetch_data.copy()

main()
