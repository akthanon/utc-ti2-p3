import logging
import os
import subprocess
import time
import datetime
import threading
import json

logging.basicConfig(level=logging.INFO)

FILES_DIR = "/home/pi/files_nmap"
NOSCAN_FILE = os.path.join(FILES_DIR, "ssid_noscan.txt")
KNOWN_FILE = os.path.join(FILES_DIR, "ssid_known.json")
LOG_DIR = "/home/pi/auto_nmap"

SSID_NOSCAN = []
SSID_KNOWN = {}

scanned_ssids = set()
lock = threading.Lock()
scanning = False

def load_ssid_data():
    global SSID_NOSCAN, SSID_KNOWN

    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

    if not os.path.exists(NOSCAN_FILE):
        with open(NOSCAN_FILE, "w") as f:
            f.write("Club_Totalplay_WiFi\nMegacable Gratis\nCASINO_HERMOSILLO\n")

    if not os.path.exists(KNOWN_FILE):
        with open(KNOWN_FILE, "w") as f:
            f.write("Totalplay-CCCX PASSWORD123\nMiRedCasa123 pa55w0rd\n")

    try:
        with open(NOSCAN_FILE, "r") as f:
            SSID_NOSCAN = [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"No se pudo cargar {NOSCAN_FILE}: {e}")
        SSID_NOSCAN = []

    try:
        SSID_KNOWN = {}
        with open(KNOWN_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    ssid, password = parts
                    SSID_KNOWN[ssid] = password
    except Exception as e:
        logging.error(f"No se pudo cargar {KNOWN_FILE}: {e}")
        SSID_KNOWN = {}

def interface_exists(interface):
    return os.path.exists(f'/sys/class/net/{interface}')

def disconnect(interface="wlan1"):
    logging.info(f"Desconectando {interface}")
    subprocess.run(["dhclient", "-r", interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", f"wpa_supplicant.*{interface}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", interface, "down"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    subprocess.run(["ip", "link", "set", interface, "up"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def connect_to_open_network(ssid, interface="wlan1"):
    if ssid in SSID_NOSCAN:
        return False
    logging.info(f"Conectando a red abierta: {ssid}")
    config = f"""
    network={{
        ssid="{ssid}"
        key_mgmt=NONE
    }}
    """
    with open("/tmp/open.conf", "w") as f:
        f.write(config)

    try:
        subprocess.run(["wpa_supplicant", "-B", "-i", interface, "-c", "/tmp/open.conf"], check=True)
        time.sleep(5)
        subprocess.run(["dhclient", interface], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al conectar a red abierta {ssid}: {e}")
        return False

def connect_to_known_network(ssid, password, interface="wlan1"):
    logging.info(f"Conectando a red conocida: {ssid}")
    config = f"""
    network={{
        ssid="{ssid}"
        psk="{password}"
    }}
    """
    with open("/tmp/known.conf", "w") as f:
        f.write(config)

    try:
        subprocess.run(["wpa_supplicant", "-B", "-i", interface, "-c", "/tmp/known.conf"], check=True)
        time.sleep(5)
        subprocess.run(["dhclient", interface], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al conectar a red conocida {ssid}: {e}")
        return False

def run_nmap_scan(interface="wlan1", ssid="unknown"):
    try:
        ip_output = subprocess.check_output(["ip", "addr", "show", interface]).decode()
        ip_line = [line.strip() for line in ip_output.splitlines() if "inet " in line]
        if not ip_line:
            logging.warning(f"No se pudo obtener IP en {interface}")
            return False
        ip = ip_line[0].split()[1]
        subnet = ip.split('/')[1]
        network = ip.split('/')[0].rsplit('.', 1)[0] + ".0/" + subnet

        os.makedirs(LOG_DIR, exist_ok=True)
        fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ssid_safe = ssid.replace(" ", "_").replace("/", "_")
        log_file = os.path.join(LOG_DIR, f"nmap_scan_{ssid_safe}_{fecha}.log")

        with open(log_file, "w") as f:
            subprocess.run(["nmap", "-T4", "-F", network], stdout=f, stderr=subprocess.STDOUT, check=True)

        logging.info(f"Escaneo guardado en {log_file}")
        return True
    except Exception as e:
        logging.error(f"Error ejecutando nmap: {e}")
        return False

def connect_and_scan(ssid, password=None, is_known=False):
    global scanning
    with lock:
        if scanning:
            return
        scanning = True

    try:
        if is_known:
            if connect_to_known_network(ssid, password):
                run_nmap_scan(ssid=ssid)
        else:
            if connect_to_open_network(ssid):
                run_nmap_scan(ssid=ssid)
        scanned_ssids.add(ssid)
    finally:
        disconnect()
        with lock:
            scanning = False

def scan_networks():
    while True:
        logging.info("Escaneando redes disponibles...")
        try:
            output = subprocess.check_output(["nmcli", "-f", "SSID,SECURITY", "dev", "wifi", "list"]).decode()
            lines = output.strip().split("\n")[1:]
            networks = []
            for line in lines:
                parts = line.strip().split(None, 1)
                if not parts:
                    continue
                ssid = parts[0]
                encryption = parts[1] if len(parts) > 1 else "open"
                networks.append((ssid, encryption.lower()))
        except Exception as e:
            logging.error(f"Error al listar redes: {e}")
            time.sleep(10)
            continue

        for ssid, encryption in networks:
            if not ssid or ssid in scanned_ssids or ssid in SSID_NOSCAN:
                continue

            if ssid in SSID_KNOWN:
                threading.Thread(target=connect_and_scan, args=(ssid, SSID_KNOWN[ssid], True)).start()
                return

            if encryption in ["none", "open", "--"]:
                threading.Thread(target=connect_and_scan, args=(ssid, None, False)).start()
                return

        logging.info("Esperando antes de volver a escanear...")
        time.sleep(30)

if __name__ == "__main__":
    load_ssid_data()
    scan_networks()
