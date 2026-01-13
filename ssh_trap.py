import socket
import paramiko
import threading
from colorama import Fore, Style, init

# Inicializamos colorama para los mensajes en la terminal
init(autoreset=True)

# Configuración del puerto
SSH_PORT = 2222 
LOG_FILE = "logs/attacks.log"

class SentinelSSHServer(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        # Captura de credenciales en pantalla
        print(f"{Fore.RED}[!] INTENTO DETECTADO: {Fore.YELLOW}User: {username} | Password: {password}")
        
        # Guardamos en el archivo de log
        with open(LOG_FILE, "a") as f:
            f.write(f"SSH_ATTACK | User: {username} | Pwd: {password}\n")
        
        # Siempre rechazamos para seguir recolectando datos
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

def start_ssh_trap():
    # Generación de la llave RSA para el servidor
    host_key = paramiko.RSAKey.generate(2048)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind(('0.0.0.0', SSH_PORT))
        sock.listen(100)
        print(f"{Fore.CYAN}--- Sentinel-Trap: SSH HoneyPot Activo en puerto {SSH_PORT} ---")
    except Exception as e:
        print(f"{Fore.RED}[-] Error al levantar el servidor: {e}")
        return

    while True:
        client, addr = sock.accept()
        print(f"{Fore.MAGENTA}[+] Conexión entrante desde: {addr[0]}")
        
        transport = paramiko.Transport(client)
        
        # --- SOLUCIÓN DE COMPATIBILIDAD TOTAL ---
        # Añadimos soporte para todos los algoritmos comunes para evitar el "Incompatible peer"
        config = transport.get_security_options()
        config.key_types = [
            'ssh-rsa', 'rsa-sha2-256', 'rsa-sha2-512', 
            'ssh-ed25519', 'ecdsa-sha2-nistp256'
        ]
        config.kex = [
            'diffie-hellman-group14-sha1', 'diffie-hellman-group-exchange-sha256',
            'ecdh-sha2-nistp256', 'curve25519-sha256@libssh.org'
        ]
        # ----------------------------------------
        
        transport.add_server_key(host_key)
        server = SentinelSSHServer()
        
        try:
            transport.start_server(server=server)
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Handshake fallido o conexión cerrada: {e}")

if __name__ == "__main__":
    start_ssh_trap()
