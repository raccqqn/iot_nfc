import logging
import os
import random

LOGFILE = "station1.log"
USED_IDS_FILE = "used_ids.txt"

# Logging konfigurieren
logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_next_free_id():
    if not os.path.exists(USED_IDS_FILE):
        return 1

    with open(USED_IDS_FILE, "r") as f:
        used_ids = [int(line.strip()) for line in f if line.strip()]

    return max(used_ids) + 1 if used_ids else 1

def write_rfid_tag(bottle_id):
    # Simuliertes RFID-Schreiben (90 % Erfolg)
    return random.random() < 0.9

def save_used_id(bottle_id):
    with open(USED_IDS_FILE, "a") as f:
        f.write(f"{bottle_id}\n")

def main():
    logging.info("Station 1 gestartet")

    bottle_id = get_next_free_id()

    if write_rfid_tag(bottle_id):
        save_used_id(bottle_id)
        logging.info(f"RFID-Tag erfolgreich mit Flaschen-ID {bottle_id} beschrieben")
        print(f"Flaschen-ID {bottle_id} erfolgreich geschrieben")
    else:
        logging.error(f"Fehler beim Schreiben der Flaschen-ID {bottle_id}")
        print("Fehler beim Schreiben des RFID-Tags")

if __name__ == "__main__":
    main()
