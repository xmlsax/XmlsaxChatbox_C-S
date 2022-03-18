import socket
import sys
import time
import tkinter as tk
from threading import Thread

win = tk.Tk()
win.title('xmlsax Chatbox - '+sys.argv[2])
serverip = tuple(sys.argv[1].split(':'))
serverip = serverip[0], int(serverip[1])
s = socket.socket()
s.connect(serverip)
msg_list = []

def getnewmsg(serverip):
    s = socket.socket()
    s.connect(serverip)
    while True:
        s.sendall(b'\x02')
        data = str(s.recv(1024), encoding='utf-8')
        if data!=('' if not msg_list else msg_list[-1]): msglistb.insert(len(msg_list), data), msg_list.append(data)
        time.sleep(0.4)
Thread_getnewmsg = Thread(target=getnewmsg, args=(serverip, ), daemon=True)


def sendmsg():
    s.sendall(
        b''.join(
            [
                b'\x01', 
                bytes(
                    sys.argv[2], 
                    encoding='utf-8'
                ), 
                b': ', 
                bytes(
                    inputbox.get(), 
                    encoding='utf-8'
                )
            ]
        )
    )
    s.recv(8)


inputbox = tk.Entry(win)
msglistb = tk.Listbox(win)
msgsend  = tk.Button(win, text='Send', command=sendmsg)
msglistb.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
inputbox.pack(side=tk.LEFT, expand=True, fill=tk.X)
msgsend.pack(side=tk.LEFT)

Thread_getnewmsg.start()
try: win.mainloop()
except Exception: pass
