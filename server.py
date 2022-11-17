from DH_class import DH_Endpoint
import random
import socket

HOST = 'localhost'
PORT = 8133

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

print('Прослушивается данный порт:',PORT)

def make_keys(conn):
    L = conn.recv(2054).decode()
    L = L.split(' ')
    serverDH = DH_Endpoint(int(L[0]), int(L[1]), random.randint(1, 320))
    return serverDH

def access_check(client_public_key): # Проверка на нахождение в публичного ключа в Keys.txt
    with open('Keys.txt', 'r') as file:
        flag = False
        for line in file:
            if int(line) == client_public_key:
                flag = True
                break
    return flag

serverDH = make_keys(conn)

if access_check(serverDH.client_public_key):
    conn.send("Успешное подключение!".encode())
    server_partial_key = serverDH.generate_partial_key()
    conn.send(str(server_partial_key).encode())
    client_key_partial = int(conn.recv(1024).decode()) # Частичный ключ от клиента
    serverDH.generate_full_key(client_key_partial) # Cоздание полного ключа
    print('----------------------------------------')
    while True:
        msg = conn.recv(2024).decode()
        print('Зашифрованное сообщение:',msg)
        print('Расшифрованное сообщение:',serverDH.decrypt_message(msg))
        print('----------------------------------------')
        if serverDH.decrypt_message(msg) == 'Выход' or serverDH.decrypt_message(msg) == 'выход':
            break
    conn.close()
else:
    conn.close()