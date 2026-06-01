#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import random
import os
import subprocess
import platform
import signal

# ─── Codici segreti per interrompere la sperimentazione ──────────────────────
SECRET_CODE_1 = "Leila"
SECRET_CODE_2 = "Theseus-7d"
SECRET_CODE_3 = "Antenne"
# ──────────────────────────────────────────────────────────────────────────────

GREEN        = "\033[92m"
BRIGHT_GREEN = "\033[1;92m"
DIM_GREEN    = "\033[2;92m"
RED          = "\033[91m"
YELLOW       = "\033[93m"
RESET        = "\033[0m"
BLINK        = "\033[5m"


# ─── Suoni via beep (apk add beep) ───────────────────────────────────────────
# Ogni funzione è non-bloccante: viene lanciata in background con & shell
# in modo da non interrompere il flusso visivo.

def _beep(freq, duration_ms, repeat=1, delay_ms=100):
    """Suona un singolo tono. Non bloccante."""
    args = ["beep", "-f", str(freq), "-l", str(duration_ms),
            "-r", str(repeat), "-D", str(delay_ms)]
    try:
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        pass  # beep non installato: silenzio

def _beep_seq(tones):
    """Suona una sequenza di (freq, durata_ms) in background."""
    # Costruisce un singolo comando beep con -n tra i toni
    args = ["beep"]
    for i, (freq, dur) in enumerate(tones):
        if i > 0:
            args.append("-n")
        args += ["-f", str(freq), "-l", str(dur)]
    try:
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        pass

def suono_avvio():
    """Sequenza inquietante all'avvio — toni bassi e lenti."""
    _beep_seq([(220, 400), (196, 300), (174, 500), (155, 800)])

def suono_tick():
    """Tick breve per ogni blocco della loading bar."""
    _beep(1200, 8)

def suono_codice_ok():
    """Tono positivo breve: codice accettato."""
    _beep_seq([(880, 80), (1100, 120)])

def suono_codice_errore():
    """Buzzer basso: codice sbagliato."""
    _beep_seq([(180, 300), (150, 400)])

def suono_blocco():
    """Sequenza di allarme: tentativi esauriti."""
    _beep_seq([(440, 150), (440, 150), (440, 150), (200, 600)])

def suono_successo():
    """Sequenza drammatica di liberazione."""
    _beep_seq([(523, 150), (659, 150), (784, 150), (1047, 400),
               (784, 100), (1047, 600)])

def suono_glitch():
    """Tono statico per il glitch text."""
    _beep(2000, 30)

def suono_psi():
    """Tono strano per il canale PSI — onda discendente."""
    _beep_seq([(600, 200), (500, 200), (400, 200), (350, 400)])

# ──────────────────────────────────────────────────────────────────────────────

def _sigint_handler(sig, frame):
    sys.stdout.write(f"\r{RED}  >> CTRL+C non autorizzato. Usa l'opzione [5] per interrompere.{RESET}\n")
    sys.stdout.flush()

signal.signal(signal.SIGINT, _sigint_handler)


def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")


def slow_print(text, delay=0.03, color=GREEN, newline=True):
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(RESET)
    if newline:
        print()


def instant_print(text, color=GREEN):
    print(f"{color}{text}{RESET}")


def matrix_rain(duration=1.5):
    chars = "アイウエオカキクケコ∆Ω∑∞§01TRIBUTOSEGNALECONTATTO FRECUENZAPSI"
    try:
        cols = os.get_terminal_size().columns
        rows = os.get_terminal_size().lines
    except OSError:
        cols, rows = 80, 24
    end_time = time.time() + duration
    # Riempi tutto lo schermo prima di entrare nel loop
    clear()
    while time.time() < end_time:
        # Stampa tante righe quante ne entra lo schermo, poi torna su
        screen = ""
        for _ in range(rows):
            line = ""
            for _ in range(cols):
                if random.random() > 0.6:
                    line += random.choice(chars)
                else:
                    line += " "
            screen += f"{DIM_GREEN}{line}{RESET}\n"
        # Vai all'inizio della schermata senza fare scroll
        sys.stdout.write("\033[H")   # cursore in alto a sinistra
        sys.stdout.write(screen)
        sys.stdout.flush()
        time.sleep(0.07)
    clear()


def glitch_text(text, iterations=6):
    glitch_chars = "!@#$%^&*░▒▓█▄▀■□▪▫◊◆◇●○"
    suono_glitch()
    for i in range(iterations):
        glitched = ""
        for char in text:
            if random.random() > 0.7 and char != " ":
                glitched += random.choice(glitch_chars)
            else:
                glitched += char
        sys.stdout.write(f"\r{GREEN}{glitched}{RESET}")
        sys.stdout.flush()
        time.sleep(0.07)
    sys.stdout.write(f"\r{BRIGHT_GREEN}{text}{RESET}\n")
    sys.stdout.flush()


def loading_bar(label, duration=1.5, width=40):
    sys.stdout.write(f"{GREEN}{label} [")
    sys.stdout.flush()
    steps = width
    delay = duration / steps
    for i in range(steps):
        sys.stdout.write(f"{BRIGHT_GREEN}█{GREEN}")
        sys.stdout.flush()
        suono_tick()
        time.sleep(delay)
    sys.stdout.write(f"] {BRIGHT_GREEN}OK{RESET}\n")
    sys.stdout.flush()


def divider(char="═", width=60, color=DIM_GREEN):
    print(f"{color}{char * width}{RESET}")


def header():
    clear()
    print()
    divider("▓", 60, BRIGHT_GREEN)
    glitch_text("    ░░░  S I S T E M A   D I   C O N T A T T O  ░░░")
    instant_print("    ██████╗  ██████╗ ███╗   ██╗████████╗███████╗", DIM_GREEN)
    instant_print("    ██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝██╔════╝", GREEN)
    instant_print("    ██████╔╝██║   ██║██╔██╗ ██║   ██║   █████╗  ", DIM_GREEN)
    instant_print("    ██╔═══╝ ██║   ██║██║╚██╗██║   ██║   ██╔══╝  ", GREEN)
    instant_print("    ██║     ╚██████╔╝██║ ╚████║   ██║   ███████╗", DIM_GREEN)
    instant_print("    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝", GREEN)
    print()
    divider("═", 60)
    instant_print("    TERMINALE PERSONALE // RICERCATORE INDIPENDENTE E.S.", DIM_GREEN)
    instant_print("    PROGETTO: PONTE // FASE VII // TRIBUTO IN CORSO", YELLOW)
    instant_print("    REGISTRO ACCESSI NON AUTORIZZATI: ATTIVO", RED)
    divider("▓", 60, BRIGHT_GREEN)
    print()


def menu():
    instant_print("  MODULI:", BRIGHT_GREEN)
    print()
    instant_print("  [1]  ARCHIVIO SEGNALI // PROVE DEL CONTATTO", GREEN)
    instant_print("  [2]  DIARIO DI RICERCA // LOG ESPERIMENTI", GREEN)
    instant_print("  [3]  PROTOCOLLO PREPARAZIONE SOGGETTI", GREEN)
    instant_print("  [4]  TENTATIVO DI CONTATTO PSI // SESSIONE LIVE", GREEN)
    instant_print("  [5]  >>> INTERROMPI SPERIMENTAZIONE <<<", YELLOW)
    print()
    divider("─", 60, DIM_GREEN)
    sys.stdout.write(f"{BRIGHT_GREEN}  > MODULO: {RESET}")
    sys.stdout.flush()


# ─── FUNZIONE 1: Archivio Segnali ────────────────────────────────────────────

def funzione_1():
    clear()
    print()
    divider("═", 60)
    slow_print("  >> ARCHIVIO SEGNALI // PROVE DEL CONTATTO", 0.04, BRIGHT_GREEN)
    divider("═", 60)
    print()
    slow_print("  Raccolgo prove da 13 anni.", 0.03, DIM_GREEN)
    slow_print("  Nessuno mi crede. Ma i dati non mentono.", 0.03, DIM_GREEN)
    slow_print("  I dati NON mentono.", 0.03, DIM_GREEN)
    slow_print("  I dati NON mentono.", 0.02, DIM_GREEN)
    slow_print("  I dati NON mentono.", 0.02, DIM_GREEN)
    slow_print("  I dati NON mentono.", 0.02, DIM_GREEN)
    print()

    loading_bar("  Caricamento archivio segnali           ", 1.1)
    loading_bar("  Elaborazione spettrogrammi             ", 0.9)
    loading_bar("  Correlazione temporale eventi          ", 1.3)
    print()

    segnali = [
        ("S-001", "14.03.2013", "432.7 Hz", "18m 44s", "PARZIALE",   "Prima ricezione. Non dormivo da 4 giorni."),
        ("S-002", "07.11.2014", "432.7 Hz", "02m 11s", "RUMORE",     "Interferenza. O forse no. Ci penso ancora."),
        ("S-003", "29.06.2016", "432.7 Hz", "41m 03s", "CONFERMATO", "Risposta. Ne sono CERTO. Era una risposta."),
        ("S-004", "12.02.2018", "432.7 Hz", "07m 58s", "PARZIALE",   "Volevano qualcosa. Ho capito dopo."),
        ("S-005", "03.09.2019", "432.7 Hz", "1h 12m",  "CONFERMATO", "Il messaggio era chiaro. TRIBUTO. PONTE."),
        ("S-006", "21.12.2021", "432.7 Hz", "3h 00m",  "CONFERMATO", "Solstizio. Non è un caso. Non è MAI un caso."),
        ("S-007", "??/??/????", "432.7 Hz", "???",     "IN CORSO",   "Stanno aspettando. Il tributo non era giusto."),
    ]

    instant_print("  ID      DATA        FREQ       DURATA   STATO        NOTE", YELLOW)
    divider("─", 60, DIM_GREEN)
    for sid, data, freq, dur, stato, nota in segnali:
        color = BRIGHT_GREEN if stato == "CONFERMATO" else (YELLOW if stato == "IN CORSO" else DIM_GREEN)
        instant_print(f"  {sid}   {data}  {freq}   {dur:<8} {stato:<13}", color)
        slow_print(f'         "{nota}"', 0.012, DIM_GREEN)
        time.sleep(0.1)

    print()
    slow_print("  >> NOTA PERSONALE (aggiunta 14/10/2024):", 0.03, YELLOW)
    slow_print("  La frequenza non cambia mai. 432.7 Hz esatti.", 0.02, DIM_GREEN)
    slow_print("  È la stessa dei cristalli di quarzo naturale.", 0.02, DIM_GREEN)
    slow_print("  È la stessa della risonanza della camera cranica umana.", 0.02, DIM_GREEN)
    slow_print("  Non è una coincidenza.", 0.02, DIM_GREEN)
    slow_print("  Non è MAI una coincidenza.", 0.02, DIM_GREEN)
    print()
    divider("─", 60, DIM_GREEN)
    input(f"{DIM_GREEN}  Premi INVIO per tornare al menu...{RESET}")


# ─── FUNZIONE 2: Diario di Ricerca ───────────────────────────────────────────

def funzione_2():
    clear()
    print()
    divider("═", 60)
    slow_print("  >> DIARIO DI RICERCA // LOG ESPERIMENTI - E.S.", 0.04, BRIGHT_GREEN)
    divider("═", 60)
    print()

    loading_bar("  Caricamento voci diario               ", 1.0)
    print()

    voci = [
        ("14/03/2013",
         "Ho ricevuto il primo segnale stanotte. Le apparecchiature hanno registrato\n"
         "  tutto. Ho provato a mostrarlo al dipartimento. Mi hanno riso in faccia.\n"
         "  Ridete pure. Io so quello che ho sentito."),
        ("22/07/2015",
         "Ho riletto i testi sumeri. DINGIR non significa 'dio'. Significa 'coloro\n"
         "  che vengono dal cielo'. La traduzione ufficiale è sbagliata. O peggio:\n"
         "  è intenzionalmente sbagliata. Qualcuno sa. Qualcuno ha sempre saputo."),
        ("03/09/2019",
         "Il segnale di stanotte era diverso. C'era una struttura. Una richiesta.\n"
         "  Ho impiegato 6 settimane a decodificarla. La parola è AXUM, in proto-\n"
         "  sumero antico: 'portare ciò che è richiesto'. In senso rituale: tributo.\n"
         "  Capisco ora. Capisco cosa vogliono."),
        ("11/01/2020",
         "Primo tentativo con soggetto A. Preparazione: 72 ore. Isolamento sensoriale,\n"
         "  calibrazione frequenza 432.7 Hz. Esposizione prolungata al segnale S-005.\n"
         "  Il soggetto non era adatto. L'esperimento non ha prodotto contatto.\n"
         "  Ho dovuto concludere la fase. Ho smaltito tutto correttamente."),
        ("04/04/2021",
         "Soggetto B. Ho modificato il protocollo. 96 ore di preparazione. Ho aggiunto\n"
         "  la componente vibrazionale: 7.83 Hz (risonanza Schumann) in combinazione\n"
         "  con 432.7 Hz. Il soggetto mostrava risposte neurologiche anomale al giorno 3.\n"
         "  Stava diventando un ponte. Poi ha smesso di rispondere. Troppo presto.\n"
         "  Devo affinare i tempi."),
        ("17/08/2022",
         "Soggetto C e D (tentativo congiunto - teoria della risonanza multipla).\n"
         "  Risultato: negativo. La combinazione amplifica. Non è sufficiente.\n"
         "  Settimane di lavoro sprecate. Sono stanco. Ma sono vicino. LO SENTO.\n"
         "  Loro sanno che sono vicino. Per questo continuano a mandarmi i segnali."),
        ("29/03/2024",
         "Ho affinato il protocollo. Il Progetto PONTE è alla Fase VII.\n"
         "  I soggetti attuali sono i più adatti che abbia mai selezionato.\n"
         "  La finestra di contatto si apre tra pochi giorni. Se anche questa\n"
         "  volta fallisce... non lo so. Non posso fallire ancora.\n"
         "  NON POSSO."),
    ]

    for data, testo in voci:
        print()
        instant_print(f"  ┌─ [{data}]", YELLOW)
        for riga in testo.split("\n"):
            slow_print(f"  │ {riga}", 0.013, DIM_GREEN)
            time.sleep(0.03)
        instant_print("  └─", YELLOW)
        time.sleep(0.3)

    print()
    slow_print("  >> [BOZZA - DATA: ASSENTE]:", 0.03, YELLOW)
    slow_print('  "Questa volta funzionerà. Devono farlo funzionare. Ho dato troppo."', 0.02, DIM_GREEN)
    print()
    divider("─", 60, DIM_GREEN)
    input(f"{DIM_GREEN}  Premi INVIO per tornare al menu...{RESET}")


# ─── FUNZIONE 3: Protocollo Preparazione ─────────────────────────────────────

def funzione_3():
    clear()
    print()
    divider("═", 60)
    slow_print("  >> PROTOCOLLO PREPARAZIONE // VERSIONE 7.3", 0.04, BRIGHT_GREEN)
    slow_print("  >> DOCUMENTO OPERATIVO - PROGETTO PONTE - E.S.", 0.03, YELLOW)
    divider("═", 60)
    print()

    slow_print("  PREMESSA:", 0.03, BRIGHT_GREEN)
    slow_print("  Il contatto extradimensionale richiede un medium biologico preparato.", 0.02, DIM_GREEN)
    slow_print("  Il soggetto deve essere 'sintonizzato' prima della finestra di contatto.", 0.02, DIM_GREEN)
    slow_print("  La preparazione richiede precisione. Gli errori passati lo dimostrano.", 0.02, DIM_GREEN)
    print()

    loading_bar("  Caricamento protocollo v7.3            ", 1.2)
    print()

    fasi = [
        ("FASE 1", "SELEZIONE", [
            "Soggetti: 3-6 individui. Condizioni di predisposizione ignote.",
            "Nessun legame con forze dell'ordine o enti governativi.",
            "Preferibile: nessun familiare nelle vicinanze immediate.",
            "IMPORTANTE: Test neurologico preliminare: recettività alle frequenze ELF.",
        ]),
        ("FASE 2", "ISOLAMENTO", [
            "Rimozione di tutti i dispositivi elettronici personali.",
            "Privazione graduale di riferimenti temporali (orologi, luce naturale).",
            "Somministrazione farmacologica: eliminazione metalli pesanti, ottimizzazione conduttività.",
            "Durata: Poche ore. Versioni precedenti usavano 96h: controindicato.",
        ]),
        ("FASE 3", "CALIBRAZIONE FREQUENZIALE", [
            "Esposizione continua: 432.7 Hz (frequenza di ricezione confermata).",
            "Sovrapposizione: 7.83 Hz risonanza Schumann (sincronizzazione campo terrestre).",
            "Monitoraggio risposta neurologica ogni 2 ore.",
            "Segnale S-005 in loop: il più completo tra quelli ricevuti.",
            "Obiettivo: il soggetto diventa un'antenna biologica.",
        ]),
        ("FASE 4", "FINESTRA DI CONTATTO", [
            "Apertura canale PSI nelle ultime 6 ore di preparazione.",
            "Il soggetto deve essere sveglio. La coscienza è il canale.",
            "Monitoraggio costante dei parametri vitali.",
            "IMPORTANTE: non interrompere la sessione prima della risposta.",
            "Le interruzioni dei cicli precedenti hanno causato i fallimenti.",
        ]),
        ("FASE 5", "PROTOCOLLO DI CONCLUSIONE", [
            "[TESTO RIMOSSO - versioni 1-6]",
            "[TESTO RIMOSSO - versioni 1-6]",
            "v7.3: la conclusione avviene DOPO il contatto confermato.",
            "Non prima. L'errore delle fasi precedenti era la prematura conclusione.",
            "Attendere sempre la conferma del segnale di risposta.",
        ]),
        ("FASE 6", "PULIZIE", [
            "Eliminare i soggetti fallimentari.",
            "NON LASCIARE PROVE: LORO RUBERANNO LA TUA RICERCA!",
        ]),
    ]

    for cod, nome, passi in fasi:
        print()
        instant_print(f"  ╔═ {cod}: {nome} {'═' * (40 - len(nome))}╗", BRIGHT_GREEN)
        for passo in passi:
            color = RED if "RIMOSSO" in passo else DIM_GREEN
            slow_print(f"  ║  • {passo}", 0.013, color)
            time.sleep(0.05)
        instant_print(f"  ╚{'═' * 50}╝", BRIGHT_GREEN)
        time.sleep(0.2)

    print()
    slow_print("  >> STATO ATTUALE: FASE 4 // FINESTRA DI CONTATTO APERTA", 0.03, YELLOW)
    slow_print("  >> FINESTRA DI CONTATTO: SEGNALE DEBOLE", 0.03, YELLOW)
    slow_print("  >> NOTA: Non toccare le apparecchiature", 0.03, RED)
    print()
    divider("─", 60, DIM_GREEN)
    input(f"{DIM_GREEN}  Premi INVIO per tornare al menu...{RESET}")


# ─── FUNZIONE 4: Tentativo Contatto PSI ──────────────────────────────────────

def funzione_4():
    clear()
    print()
    divider("═", 60)
    slow_print("  >> SESSIONE CONTATTO PSI // CANALE LIVE", 0.04, BRIGHT_GREEN)
    slow_print("  >> FREQUENZA: 432.7 Hz + 7.83 Hz SCHUMANN", 0.03, YELLOW)
    divider("═", 60)
    print()

    slow_print("  Questa è la sessione attiva collegata ai soggetti in preparazione.", 0.02, DIM_GREEN)
    slow_print("  Il canale è bidirezionale. Quello che viene trasmesso, viene ricevuto.", 0.02, DIM_GREEN)
    slow_print("  Quello che loro trasmettono, arriverà qui.", 0.02, DIM_GREEN)
    print()

    loading_bar("  Attivazione emettitore frequenziale    ", 1.3)
    loading_bar("  Sincronizzazione Schumann 7.83 Hz      ", 1.1)
    loading_bar("  Aggancio segnale S-007 (in corso)      ", 1.6)
    loading_bar("  Amplificazione biologica attiva        ", 0.9)
    print()

    slow_print("  >> CANALE APERTO.", 0.04, BRIGHT_GREEN)
    slow_print("  >> IN ATTESA DI RISPOSTA EXTRADIMENSIONALE...", 0.03, DIM_GREEN)
    print()

    for i in range(6):
        sys.stdout.write(f"{DIM_GREEN}  {'.' * (i + 1)}{RESET}   ")
        sys.stdout.flush()
        time.sleep(1.1)
    print("\n")

    slow_print("  >> RILEVATA FLUTTUAZIONE NEL CAMPO ELF...", 0.03, YELLOW)
    time.sleep(0.7)
    slow_print("  >> PATTERN NON CASUALE. ELABORAZIONE...", 0.03, YELLOW)
    time.sleep(0.8)

    glitch_text("  >>>  SEGNALE IN INGRESSO // DECODIFICA IN CORSO  <<<")
    suono_psi()
    print()

    messaggi = [
        "  >> RICONOSCIUTA STRUTTURA AXUM.",
        "  >> RICONOSCIUTA RICHIESTA TRIBUTO.",
        "  >> RICONOSCIUTA FREQUENZA 432.7 Hz.",
        "  >> RICONOSCIUTA RISONANZA SCHUMANN.",
        "  >> RICONOSCIUTA RICHIESTA DI CONTATTO.",
        "  >> RICONOSCIUTA RICHIESTA DI PREPARAZIONE.",
        "  >> RICONOSCIUTA RICHIESTA DI TRIBUTO.",
        "  >> RICONOSCIUTA RICHIESTA DI TRIBUTO.",
        "  >> RICONOSCIUTA RICHIESTA DI TRIBUTO.",
    ]

    for msg in messaggi:
        time.sleep(random.uniform(0.6, 1.4))
        slow_print(msg, 0.025, YELLOW)

    print()
    time.sleep(0.5)
    slow_print("  >> SEGNALE PERSO.", 0.03, RED)
    slow_print("  >> CONTATTO NON STABILITO.", 0.03, RED)
    slow_print("  >> FINE SESSIONE.", 0.03, RED)
    print()
    divider("─", 60, DIM_GREEN)
    input(f"{DIM_GREEN}  Premi INVIO per tornare al menu...{RESET}")


# ─── FUNZIONE 5: Interrompi Sperimentazione ───────────────────────────────────

def eject_cd():
    sistema = platform.system()
    try:
        if sistema == "Windows":
            subprocess.run(
                ["powershell", "-Command",
                 '(New-Object -ComObject Shell.Application).Namespace(17).ParseName("D:").InvokeVerb("Eject")'],
                check=False, capture_output=True,
            )
        elif sistema == "Linux":
            subprocess.run(["eject"], check=False, capture_output=True)
        elif sistema == "Darwin":
            subprocess.run(["drutil", "tray", "open"], check=False, capture_output=True)
    except Exception:
        pass


def funzione_5():
    clear()
    print()
    divider("▓", 60, YELLOW)
    slow_print("  >>> INTERRUZIONE SPERIMENTAZIONE <<<", 0.04, YELLOW)
    slow_print("  >>> PROTOCOLLO DI EMERGENZA // ACCESSO ESTERNO <<<", 0.03, RED)
    divider("▓", 60, YELLOW)
    print()
    slow_print("  Questa procedura interrompe il protocollo di preparazione.", 0.03, DIM_GREEN)
    slow_print("  Se confermata, rilascia i soggetti e disattiva le apparecchiature.", 0.03, DIM_GREEN)
    print()
    slow_print("  >> Inserire la sequenza di interruzione in tre parti.", 0.03, YELLOW)
    slow_print("  >> ATTENZIONE: solo 3 tentativi totali prima del blocco.", 0.03, RED)
    print()
    divider("─", 60, DIM_GREEN)
    print()

    tentativi_rimasti = 3

    while tentativi_rimasti > 0:
        instant_print(f"  [Tentativi rimasti: {tentativi_rimasti}]", DIM_GREEN)
        print()

        # ── Codice 1 ──
        sys.stdout.write(f"{BRIGHT_GREEN}  >> CODICE 1: {RESET}")
        sys.stdout.flush()
        code1 = input().strip()

        if code1.lower() != SECRET_CODE_1.lower():
            tentativi_rimasti -= 1
            suono_codice_errore()
            print()
            slow_print("  >> CODICE 1 NON VALIDO.", 0.04, RED)
            if tentativi_rimasti > 0:
                slow_print(f"  >> Sequenza annullata. Tentativi rimasti: {tentativi_rimasti}", 0.03, YELLOW)
                print()
                divider("─", 60, DIM_GREEN)
                print()
            continue

        print()
        suono_codice_ok()
        loading_bar("  Verifica codice 1                     ", 0.9)
        print()

        # ── Codice 2 ──
        sys.stdout.write(f"{BRIGHT_GREEN}  >> CODICE 2: {RESET}")
        sys.stdout.flush()
        code2 = input().strip()

        if code2.lower() != SECRET_CODE_2.lower():
            tentativi_rimasti -= 1
            suono_codice_errore()
            print()
            slow_print("  >> CODICE 2 NON VALIDO.", 0.04, RED)
            if tentativi_rimasti > 0:
                slow_print(f"  >> Sequenza annullata. Tentativi rimasti: {tentativi_rimasti}", 0.03, YELLOW)
                print()
                divider("─", 60, DIM_GREEN)
                print()
            continue

        print()
        suono_codice_ok()
        loading_bar("  Verifica codice 2                     ", 0.9)
        print()

        # ── Codice 3 ──
        sys.stdout.write(f"{BRIGHT_GREEN}  >> CODICE 3: {RESET}")
        sys.stdout.flush()
        code3 = input().strip()

        if code3.lower() != SECRET_CODE_3.lower():
            tentativi_rimasti -= 1
            suono_codice_errore()
            print()
            slow_print("  >> CODICE 3 NON VALIDO.", 0.04, RED)
            if tentativi_rimasti > 0:
                slow_print(f"  >> Sequenza annullata. Tentativi rimasti: {tentativi_rimasti}", 0.03, YELLOW)
                print()
                divider("─", 60, DIM_GREEN)
                print()
            continue

        print()
        suono_codice_ok()
        loading_bar("  Verifica codice 3                     ", 0.9)

        # ── SUCCESSO ──
        print()
        loading_bar("  Verifica sequenza completata          ", 0.8)
        loading_bar("  Autenticazione confermata             ", 1.0)
        loading_bar("  Interruzione protocollo di preparazione", 1.3)
        loading_bar("  Disattivazione emettitori frequenziali ", 1.1)
        loading_bar("  Sblocco accessi fisici                 ", 1.4)
        print()

        divider("▓", 60, BRIGHT_GREEN)
        glitch_text("  >> SPERIMENTAZIONE INTERROTTA.")
        glitch_text("  >> BLOCCHI FISICI: DISATTIVATI.")
        divider("▓", 60, BRIGHT_GREEN)
        print()

        slow_print("  RILASCIO SISTEMI IN CORSO...", 0.04, YELLOW)
        print()
        slow_print("  Spegnimento emettitore 432.7 Hz...", 0.025, GREEN)
        time.sleep(0.6)
        slow_print("  Spegnimento risonatore Schumann...", 0.025, GREEN)
        time.sleep(0.6)
        print()
        glitch_text("  >> DISCO DI SICUREZZA IN ESPULSIONE...")
        suono_successo()
        time.sleep(0.7)

        eject_cd()

        print()
        instant_print("  ╔══════════════════════════════════════════╗", BRIGHT_GREEN)
        instant_print("  ║                                          ║", BRIGHT_GREEN)
        instant_print("  ║   SPERIMENTAZIONE INTERROTTA.            ║", BRIGHT_GREEN)
        instant_print("  ║   DISCO ESPULSO. USALO PER USCIRE.       ║", BRIGHT_GREEN)
        instant_print("  ║                                          ║", BRIGHT_GREEN)
        instant_print("  ╚══════════════════════════════════════════╝", BRIGHT_GREEN)
        print()
        slow_print(f"  {BLINK}>> SIETE LIBERI. FATE IN FRETTA. <<{RESET}", 0.04, YELLOW)
        print()
        divider("─", 60, DIM_GREEN)
        input(f"{DIM_GREEN}  Premi INVIO...{RESET}")
        os.system("shutdown -h now")
        return  # Esce dalla funzione dopo il successo

    # ── BLOCCO TOTALE ──
    print()
    suono_blocco()
    slow_print("  >> TENTATIVI ESAURITI.", 0.04, RED)
    slow_print("  >> SISTEMA BLOCCATO. ANOMALIA REGISTRATA NEL LOG.", 0.04, RED)
    slow_print("  >> AVVISO INVIATO A E.S.", 0.04, RED)
    matrix_rain(1.5)
    print()
    divider("─", 60, DIM_GREEN)
    input(f"{DIM_GREEN}  Premi INVIO per tornare al menu...{RESET}")


# ─── MAIN LOOP ────────────────────────────────────────────────────────────────

def main():
    if platform.system() == "Windows":
        os.system("color")

    matrix_rain(5)
    suono_avvio()
    header()
    slow_print("  >> SISTEMA ATTIVO.", 0.03, DIM_GREEN)
    slow_print("  >> PROGETTO PONTE - FASE VII - IN CORSO.", 0.03, YELLOW)
    slow_print("  >> STATO FINESTRA DI CONTATTO: APERTA", 0.02, RED)
    time.sleep(0.6)

    while True:
        header()
        menu()
        scelta = input().strip()

        if scelta == "1":
            funzione_1()
        elif scelta == "2":
            funzione_2()
        elif scelta == "3":
            funzione_3()
        elif scelta == "4":
            funzione_4()
        elif scelta == "5":
            funzione_5()
        else:
            header()
            slow_print("  >> COMANDO NON RICONOSCIUTO.", 0.04, RED)
            time.sleep(1)


if __name__ == "__main__":
    main()
