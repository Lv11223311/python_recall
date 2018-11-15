import threading
import time
import socket

""" 
服务器

和客户端编程相比，服务器编程就要复杂一些。

服务器进程首先要绑定一个端口并监听来自其他客户端的连接。如果某个客户端连接过来了，服务器就与该客户端建立Socket连接，随后的通信就靠这个Socket连接了。

所以，服务器会打开固定端口（比如80）监听，每来一个客户端连接，就创建该Socket连接。由于服务器会有大量来自客户端的连接，所以，服务器要能够区分一个Socket连接是和哪个客户端绑定的。一个Socket依赖4项：服务器地址、服务器端口、客户端地址、客户端端口来唯一确定一个Socket。

但是服务器还需要同时响应多个客户端的请求，所以，每个连接都需要一个新的进程或者新的线程来处理，否则，服务器一次就只能服务一个客户端了。

我们来编写一个简单的服务器程序，它接收客户端连接，把客户端发过来的字符串加上Hello再发回去。 
"""

# 建立基于IPv4和TCP协议的Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 监听窗口：
s.bind(('127.0.0.1', 9999))
# 开始监听端口， 传入的参数指定等待链接的最大数量：
s.listen(5)
print('Waiting for connection...')
# 接下来服务器程序通过一个永久循环来接受来自客户端的连接， accept()会等待并返回一个客户端的连接：
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建一个新线程来处理TCP连接：
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()

# 每个连接都必须创建新线程（进程）来处理，否则，单线程处理过程中， 无法接受其他客户端的连接：
def tcplink(sock, addr):
    print('Accept new connection from %s: %s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s' %addr)

# 要测速这个服务器，还需要写一个客户端程序：
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立链接:
s.connect('127.0.0.1', 9999)
# 接收消息：
print(s.recv(1024).decode('utf-8'))
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()
