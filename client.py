import socket
import os
import hashlib

HOST = '127.0.0.1'  # Địa chỉ IP của máy chủ
PORT = 5001         # Cổng của máy chủ

def send_file(filename):
    filesize = os.path.getsize(filename)
    
    # Tính toán checksum
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    checksum = sha256.hexdigest()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Gửi kích thước tên file và tên file
        filename_bytes = filename.encode()
        s.sendall(len(filename_bytes).to_bytes(4, 'big'))
        s.sendall(filename_bytes)

        # Gửi kích thước file
        s.sendall(filesize.to_bytes(8, 'big'))

        # Gửi kích thước checksum và checksum
        checksum_bytes = checksum.encode()
        s.sendall(len(checksum_bytes).to_bytes(4, 'big'))
        s.sendall(checksum_bytes)

        # Gửi dữ liệu file
        with open(filename, 'rb') as f:
            while (chunk := f.read(4096)):
                s.sendall(chunk)

        # Nhận phản hồi từ máy chủ
        response = s.recv(2).decode()
        print(f"Phản hồi từ máy chủ: {response}")

if __name__ == "__main__":
    filename = input("Nhập tên file để gửi: ")
    send_file(filename)
