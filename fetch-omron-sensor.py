import bluetooth._bluetooth as bluez
import struct
import binascii

_SENSOR_MAC_ADDR_ = 'ba3239a85e8d' # MAC address of your USB sensor (like BA:32:39:A8:5E:8D)
_RETRY_ = 100
_BT_DEV_ID_ = 0 # Bluetooth adaptor

def main():
  sock = bluez.hci_open_dev(_BT_DEV_ID_)

  cmd_pkt = struct.pack("<BBBBBBB", 0x01, 0x0, 0x10, 0x0, 0x10, 0x01, 0x00)
  bluez.hci_send_cmd(sock, 0x08, 0x000B, cmd_pkt)

  cmd_pkt = struct.pack("<BB", 0x01, 0x00)
  bluez.hci_send_cmd(sock, 0x08, 0x000C, cmd_pkt)

  flt = bluez.hci_filter_new()
  bluez.hci_filter_all_events(flt)
  bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
  sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, flt)

  for _ in range(_RETRY_):
    pkt = sock.recv(255)
    if (b'\xd5\x02' not in pkt): continue
    if (b'Rbt' not in pkt): continue
    if (_SENSOR_MAC_ADDR_ != binascii.hexlify((pkt[7:13])[::-1]).decode()): continue

    # value = [temperature, relative_humidity, ambient_light, barometric_pressure, sound_noise, etvoc, eco2]
    value = struct.unpack('<hhhlhhh', pkt[23:39])
    print(",".join(map(str, value)))
    break

if __name__ == "__main__":
    main()
