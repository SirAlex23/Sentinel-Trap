import requests
import time
import os
from colorama import Fore, init
from dotenv import load_dotenv

init(autoreset=True)
load_dotenv()

# --- TUS DATOS CONFIGURADOS ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LOG_FILE = "logs/attacks.log"

def get_geo_data(ip):
    # Detectar red local o WiFi propia
    if ip == "127.0.0.1" or ip.startswith("192.168."):
        return "Red Interna (Tu Casa/WiFi)", "https://www.google.com/maps?q=39.4699,-0.3763"
    
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,lat,lon", timeout=5).json()
        if res['status'] == 'success':
            loc = f"{res['city']}, {res['country']}"
            map_link = f"https://www.google.com/maps?q={res['lat']},{res['lon']}"
            return loc, map_link
    except:
        pass
    return "Ubicación Externa (No rastreable)", "No disponible"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={'chat_id': CHAT_ID, 'text': msg})
        if r.status_code == 200:
            print(f"{Fore.GREEN}[OK] Alerta enviada a Telegram")
        else:
            print(f"{Fore.RED}[FALLO] Telegram dice: {r.text}")
    except:
        print(f"{Fore.RED}[ERROR] Sin conexión")

def monitor():
    print(f"{Fore.CYAN}=== SENTINEL MONITOR V3 (MAPAS ACTIVOS) ===")
    print("Elige donde quieres que te llegue el mensaje:")
    print("1. Solo Consola")
    print("2. Telegram") # Ahora aparece debajo de la opción 1
    modo = input("Selecciona (1 o 2): ")

    if not os.path.exists(LOG_FILE): 
        if not os.path.exists("logs"): os.makedirs("logs")
        open(LOG_FILE, "w").close()

    # Texto exacto que pediste
    print(f"{Fore.YELLOW}[+] Esperando ataques... (Pulse Ctrl+C para salir)")

    with open(LOG_FILE, "r") as f:
        f.seek(0, 2)
        while True:
            linea = f.readline()
            if linea:
                ip_ataque = "127.0.0.1"
                if "IP:" in linea:
                    partes = linea.split("|")
                    for p in partes:
                        if "IP:" in p: ip_ataque = p.replace("IP:", "").strip()
                
                geo, mapa = get_geo_data(ip_ataque)
                
                mensaje = (f"🚨 ATAQUE DETECTADO\\n\\n"
                           f"📍 Ubicación: {geo}\\n"
                           f"🔗 Mapa: {mapa}\\n"
                           f"📝 Registro: {linea.strip()}")
                
                print(f"{Fore.RED}¡INTRUSIÓN!: {linea.strip()} ({geo})")
                if modo == "2":
                    enviar_telegram(mensaje)
            time.sleep(0.5)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print(f"\\n{Fore.YELLOW}[-] Sistema detenido.")
