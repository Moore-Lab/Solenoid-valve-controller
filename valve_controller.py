import serial
import serial.tools.list_ports


class ValveController:
    def __init__(self, port=None, baud_rate=115200, timeout=2):
        if port is None:
            port = self._find_port()
        self.ser = serial.Serial(port, baud_rate, timeout=timeout)

    def _find_port(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            desc = p.description or ""
            if any(chip in desc for chip in ("CP210", "CH340", "FTDI", "USB Serial")):
                return p.device
        if ports:
            return ports[0].device
        raise RuntimeError("No serial port found. Pass port= explicitly.")

    def open(self):
        self.ser.write(b"OPEN\n")
        response = self.ser.readline().decode().strip()
        if response != "OK:OPEN":
            raise RuntimeError(f"Unexpected response: {response!r}")

    def close(self):
        self.ser.write(b"CLOSE\n")
        response = self.ser.readline().decode().strip()
        if response != "OK:CLOSE":
            raise RuntimeError(f"Unexpected response: {response!r}")

    def disconnect(self):
        self.ser.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.disconnect()
