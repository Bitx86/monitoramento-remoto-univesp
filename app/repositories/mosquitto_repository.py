import subprocess
import os

MOSQUITTO_PASSWD_FILE = "/etc/mosquitto/passwd"
MOSQUITTO_ACL_FILE    = "/etc/mosquitto/acl"

def configure_mosquitto(device_id: str, secret: str, user_id: str):
    # 1. Adiciona o usuário no arquivo de senhas
    # mosquitto_passwd -b <arquivo> <usuario> <senha>
    print("ACL")
    subprocess.run(
        ["sudo", "mosquitto_passwd", "-b", MOSQUITTO_PASSWD_FILE, device_id, secret],
        check=True
    )
    
    # 2. Adiciona a regra de ACL para esse device
    acl_entry = (
        f"\nuser {device_id}\n"
        f"topic readwrite users/{user_id}/devices/{device_id}/#\n"
    )
    with open(MOSQUITTO_ACL_FILE, "a") as f:
        f.write(acl_entry)
    print("Mosquitto Restart")
    # 3. Recarrega o Mosquitto sem derrubar conexões existentes
    #subprocess.run(["sudo", "pkill", "-HUP", "-x", "mosquitto"], check=True)
    subprocess.run(["sudo", "systemctl", "reload", "mosquitto"], check=True)