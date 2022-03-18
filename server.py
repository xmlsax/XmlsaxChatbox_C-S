import socketserver, sys

msg_list = []

class TalkingTCPServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        conn = self.request
        addr = self.client_address
        while True:
            try:
                recv_data = str(conn.recv(1024), encoding='utf-8')
                print("RECIEVED FROM", addr[0]+':'+str(addr[1]), '->', recv_data, file=logging)
                if recv_data.startswith('\0') or not recv_data:
                    break
                if recv_data.startswith('\x01'):
                    msg_list.append(recv_data[1:])
                    send_data = '\0'
                elif recv_data.startswith('\x02'):
                    send_data = ')'*len(msg_list) and msg_list[-1]
                send_data = bytes(send_data, encoding='utf-8')
                conn.sendall(send_data)
            except (ConnectionAbortedError, ConnectionResetError):
                break
        conn.close()

if __name__ == '__main__':
    try:
        logging = open(sys.argv[1], 'w')
        server = socketserver.ThreadingTCPServer(('127.0.0.1', int(sys.argv[2])), TalkingTCPServer)
        server.serve_forever()
    finally:
        logging.close()
