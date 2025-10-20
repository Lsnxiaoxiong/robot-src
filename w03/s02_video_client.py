import cv2
import socket
import struct
import numpy as np

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 8888))  # 例如 ("127.0.0.1", 8888)

while True:
    # 先接收 4 字节长度
    data_len = client_socket.recv(4)
    if not data_len:
        break

    length = struct.unpack(">I", data_len)[0]

    # 再接收对应长度的数据
    data = b""
    while len(data) < length:
        packet = client_socket.recv(length - len(data))
        if not packet:
            break
        data += packet

    # 解码为图像
    img_array = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # 显示图像
    cv2.imshow("Client", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

client_socket.close()
cv2.destroyAllWindows()
