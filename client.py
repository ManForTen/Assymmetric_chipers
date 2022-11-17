from DH_class import DH_Endpoint
import socket

HOST = 'localhost'
PORT = 8133

sock = socket.socket()
sock.connect((HOST, PORT))
clientDH = DH_Endpoint() # Вызов класса
clientDH.all_of_public_keys() # Создание ключей
keys = str(clientDH.client_public_key)+' '+str(clientDH.server_public_key)
sock.send(keys.encode()) # Отправление публичных ключей серверу
msg = sock.recv(1024).decode()
if msg == "Успешное подключение!":
    print(msg)
    print("Для выхода напишите 'Выход'")
    server_key_partial = int(sock.recv(1024).decode())
    client_partial_key = clientDH.generate_partial_key()
    sock.send(str(client_partial_key).encode())  # Отправка частичного ключа клиента (А) серверу
    clientDH.generate_full_key(server_key_partial)
    while True:
        msg = input("Введите сообщение:")
        if msg == 'Выход' or msg == 'выход':
            sock.send(clientDH.encrypt_message(msg).encode())
            break
        sock.send(clientDH.encrypt_message(msg).encode()) # Отправка закодированного сообщения
    sock.close()
else:
    print("Вы не смогли подключится")
    sock.close()