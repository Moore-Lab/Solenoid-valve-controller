import time
import serial
import serial.tools.list_ports


class ValveController:
    def __init__(self, port=None, baud_rate=115200, timeout=2):
        if port is None:
            port = self._find_port()
        self.ser = serial.Serial(port, baud_rate, timeout=timeout)
        self._is_open: bool = False

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
        self._is_open = True

    def close(self):
        self.ser.write(b"CLOSE\n")
        response = self.ser.readline().decode().strip()
        if response != "OK:CLOSE":
            raise RuntimeError(f"Unexpected response: {response!r}")
        self._is_open = False

    def pulse(self, duration_s: float) -> None:
        """Open the valve for duration_s seconds, then close it."""
        self.open()
        time.sleep(max(0.0, float(duration_s)))
        self.close()

    def status(self) -> dict:
        """Return local valve state. No hardware query — firmware has no status command."""
        return {"is_open": self._is_open}

    def disconnect(self):
        self.ser.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.disconnect()
