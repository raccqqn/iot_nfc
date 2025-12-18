import logging
import time
from nfc_reader import NFCReader
from db import get_next_free_bottle, mark_bottle_as_tagged

# --------------------------------------------------
# Logging konfigurieren
# --------------------------------------------------
logging.basicConfig(
    filename="station1.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Station 1 started")

    # --------------------------------------------------
    # NFC-Reader initialisieren
    # --------------------------------------------------
    try:
        reader = NFCReader()
        logger.info("NFC reader initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize NFC reader: {e}")
        return

    logger.info("Station 1 running – waiting for RFID tags")

    while True:
        # --------------------------------------------------
        # Auf RFID-Karte warten
        # --------------------------------------------------
        uid = reader.read_passive_target(timeout=0.5)
        if uid is None:
            continue

        uid_bytes = bytes(uid)
        logger.info(f"RFID tag detected: {[hex(i) for i in uid]}")

        # --------------------------------------------------
        # Prüfen, ob Karte schon beschrieben ist
        # --------------------------------------------------
        block_data = reader.read_block(uid_bytes, 2)
        if block_data is not None and block_data[0] != 0x00:
            logger.warning("RFID tag already contains a bottle ID – skipping")
            time.sleep(1)
            continue

        # --------------------------------------------------
        # Nächste freie Flasche aus DB holen
        # --------------------------------------------------
        bottle_id = get_next_free_bottle()

        if bottle_id is None:
            logger.error("No free bottle available in database")
            time.sleep(2)
            continue

        logger.info(f"Next free bottle ID from DB: {bottle_id}")

        # --------------------------------------------------
        # Flaschen-ID auf RFID schreiben
        # Block 2, Byte 0
        # --------------------------------------------------
        data = bytes([bottle_id] + [0x00] * 15)

        success = reader.write_block(
            uid=uid_bytes,
            block_number=2,
            data=data
        )

        if success:
            logger.info(f"Successfully wrote bottle ID {bottle_id} to RFID tag")

            # --------------------------------------------------
            # DB aktualisieren
            # --------------------------------------------------
            mark_bottle_as_tagged(bottle_id)
            logger.info(f"Bottle ID {bottle_id} marked as tagged in database")

        else:
            logger.error(f"Failed to write bottle ID {bottle_id} to RFID tag")

        # Kleine Pause, damit dieselbe Karte nicht sofort erneut erkannt wird
        time.sleep(1)


if __name__ == "__main__":
    main()
