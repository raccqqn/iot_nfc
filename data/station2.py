import logging

LOGFILE = "station2.log"

# Logging konfigurieren
logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def read_rfid_tag(bottle_id):
    # Simuliertes RFID-Lesen
    return bottle_id

def get_fill_amount(bottle_id):
    # Beispielhafte Regel
    if bottle_id % 2 == 0:
        return 1.0  # Liter
    else:
        return 0.5  # Liter

def process_bottle(bottle_id):
    rfid_id = read_rfid_tag(bottle_id)
    fill_amount = get_fill_amount(rfid_id)

    logging.info(
        f"Flaschen-ID {rfid_id} erkannt – Füllmenge: {fill_amount} Liter"
    )

    print(f"Flasche {rfid_id}: {fill_amount} Liter")

def main():
    logging.info("Station 2 gestartet")

    # Zwei verschiedene Flaschen dokumentieren
    process_bottle(1)
    process_bottle(2)

if __name__ == "__main__":
    main()
