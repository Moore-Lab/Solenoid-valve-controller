import argparse
from valve_controller import ValveController

parser = argparse.ArgumentParser(description="Control solenoid valve via serial.")
parser.add_argument("--port", help="Serial port (e.g. COM3 or /dev/ttyUSB0)")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-open", action="store_true", help="Open the valve (GPIO 33 HIGH)")
group.add_argument("-close", action="store_true", help="Close the valve (GPIO 33 LOW)")
args = parser.parse_args()

with ValveController(port=args.port) as valve:
    if args.open:
        valve.open()
        print("Valve opened.")
    else:
        valve.close()
        print("Valve closed.")
