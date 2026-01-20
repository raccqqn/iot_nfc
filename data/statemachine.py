import time
import random
import logging
from enum import Enum, auto


logging.basicConfig(
    filename="statemachine.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class State(Enum):
    INIT = auto()
    WAIT_FOR_TAG = auto()
    READ_TAG = auto()
    PROCESS = auto()
    SUCCESS = auto()
    ERROR = auto()
    STOP = auto()


def rfid_present():
    """Simuliert, ob ein RFID-Tag noch vorhanden ist"""
    return random.random() > 0.2  # 80 % vorhanden

def read_rfid():
    """Simuliertes RFID-Lesen"""
    if not rfid_present():
        raise RuntimeError("RFID-Tag zu früh entfernt")
    return random.randint(1, 10)

# ------------------------
# State Machine
# ------------------------
class StationStateMachine:
    def __init__(self, name):
        self.name = name
        self.state = State.INIT
        self.bottle_id = None

    def run(self):
        logging.info(f"{self.name}: State-Machine gestartet")

        while self.state != State.STOP:
            try:

