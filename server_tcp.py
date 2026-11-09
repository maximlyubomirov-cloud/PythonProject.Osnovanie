import socket

# from matplot  <-- REMOVED: Incomplete import and not needed for this code

# 1
ip = '127.0.0.1'
port = 9001
end_point = (ip, port)

# сокет сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(end_point)
server.listen(10)

# режим ожидания запросов
print(f'Сервер запущен на IP-{ip}:{port}')
print('Ожидание запроса на соединение')
connection, address = server.accept()

# Обмен данными с клиентами
try:
    # FIXED: changed 'client_address' to 'address' (the variable defined in server.accept())
    print(f'Установлено соединение с клиентом: {address}')
    while True:
        # принимаем сообщение
        client_message = connection.recv(1024).decode(encoding='utf-8')

        # FIXED: Added underscore to 'stop_server' to match previous snippet
        if not client_message or client_message == 'stop_server':
            break

        print(f'Сообщение от клиента: [{client_message}]')

        # отправка сообщения
        server_message = input('Ответ сервера: ')

        # FIXED: Added missing 'c' to 'connection'
        connection.send(server_message.encode(encoding='utf-8'))
        print('Сообщение отправлено!')

# FIXED: Corrected indentation for 'except' (it must align with 'try')
except BaseException as e:
    print(e)
finally:
    connection.close()
    # Optional: also close the main server socket
    # server.close()
    print('Сервер остановлен')