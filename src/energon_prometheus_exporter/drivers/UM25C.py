from bluetooth import *
import datetime

class UM25C(object):
    def __init__(self, addr):
        self.addr = addr
        self.sock = BluetoothSocket(RFCOMM)
        self.sock.connect((addr, 1))

    def __del__(self):
        self.sock.close()     

    def processdata(self, d):
        data = {}

        data["Volts"] = struct.unpack(">h", d[2: 3 + 1])[0] / 1000.0    # volts
        data["Amps"] = struct.unpack(">h", d[4: 5 + 1])[0] / 10000.0    # amps
        data["Watts"] = struct.unpack(">I", d[6: 9 + 1])[0] / 1000.0    # watts
        data["temp_C"] = struct.unpack(">h", d[10: 11 + 1])[0]          # temp in C
        data["temp_F"] = struct.unpack(">h", d[12: 13 + 1])[0]          # temp in F
        data["group"] = struct.unpack(">h", d[14: 15 + 1])[0]           # measurement group
        utc_dt = datetime.datetime.now(datetime.timezone.utc)           # UTC time
        dt = utc_dt.astimezone()                                        # local time
        data["time"] = dt

        g = 0
        for i in range(16, 95, 8):
            ma, mw = struct.unpack(">II", d[i: i + 8])                  # mAh,mWh respectively
            gs = str(g)
            data[gs + "_mAh"] = ma
            data[gs + "_mWh"] = mw
            g += 1

        data["data_line_pos_volt"] = struct.unpack(">h", d[96: 97 + 1])[0] / 100.0
        data["data_line_neg_volt"] = struct.unpack(">h", d[98: 99 + 1])[0] / 100.0
        data["resistance"] = struct.unpack(">I", d[122: 125 + 1])[0] / 10.0             # resistance
        return data

    def query(self):
        d = b""
        while len(d) != 130:
            # Send request to USB meter
            self.sock.send((0xF0).to_bytes(1, byteorder="big"))
            d += self.sock.recv(130)
        data = self.processdata(d)
        return data

# Example usage
if __name__ == "__main__":
    meter = UM25C("00:15:A3:00:55:02")
    print(meter.query())