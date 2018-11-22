import socket
import threading
import os
from run import process_video

def get_file(conn,addr):
    msg=conn.recv(1024)
    try:
        msg=int(msg.decode('utf-8'))
        conn.sendall("1".encode('utf-8'))
    except:
        conn.sendall("0".encode('utf-8'))
    # 파일 크기를 받음

    file=conn.recv(msg)
    name="./test_d/%s"%(str(addr))

    os.mkdir(os.path.join(name))
    with open(name+"/src.mp4","wb") as f:
        f.write(file)

    print("File_input_success")

    video_handler=process_video(name+"/src.mp4")

    video_handler.video_out_dir=name+"/processed.mp4"

    video_handler.picture_out_dir=name+"/"

    video_handler.processVideo()




    print("session_close")


    conn.close()
#send는 보내진 바이트를 리턴한다.


def run_server(port=50505):
    t=[]
    host=''
    print("server_ready")
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((host,port))
        while True:
            s.listen(1)
            conn,addr=s.accept()
            print("Client_accepted")
            t.append(threading.Thread(target=get_file,args=(conn,addr)))
            t[-1].start()



if __name__ == '__main__':
    run_server()



