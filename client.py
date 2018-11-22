import socket
import os

def run(ip="10.0.2.15",port=50505):
    size=os.path.getsize('./test3.mp4')
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:

        s.connect((ip,port))

        s.sendall(str(size).encode('utf-8'))
        #연결 후 파일 크기를 보냄
        resp=s.recv(1024)
        resp=int(resp.decode('utf-8'))
        print(resp)
        # response를 받음, 이때 리스폰드가 1이면 실행, 아니면 에러
        if resp==1:
            with open("./test3.mp4","rb")as f:
                file=f.read()
        else:
            print("error")
        s.sendall(file)




if __name__ == '__main__':
    run()