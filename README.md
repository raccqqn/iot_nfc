stateDiagram-v2
    [*] --> Initialisierung

    Initialisierung --> ID_ermitteln
    ID_ermitteln --> RFID_schreiben

    RFID_schreiben --> Erfolg : Schreiben erfolgreich
    RFID_schreiben --> Fehler : Schreiben fehlgeschlagen

    Erfolg --> Log_Erfolg
    Log_Erfolg --> [*]

    Fehler --> Log_Fehler
    Log_Fehler --> Fehlerbehandlung
    Fehlerbehandlung --> [*]

